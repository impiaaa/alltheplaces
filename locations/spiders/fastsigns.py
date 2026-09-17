from urllib.parse import urljoin

from scrapy import Request

from locations.json_blob_spider import JSONBlobSpider
from locations.pipelines.address_clean_up import merge_address_lines


class FastsignsSpider(JSONBlobSpider):
    name = "fastsigns"
    item_attributes = {"brand": "Fastsigns", "brand_wikidata": "Q5437127"}
    # Not covered: Dominican Republic, Grand Cayman, Malta
    start_urls = [
        "https://www.fastsigns.com/Systems-Advanced-Map.svc?action=GetMapData",  # covers CA, PR, US
        "https://www.fastsigns.co.uk/Systems-Advanced-Map.svc?action=GetMapData",
        "https://www.fastsigns.cl/locales/?CallAjax=GetLocationsUSC3",
        "https://www.signwave.com.au/Systems-Advanced-Map.svc?action=GetMapData",
    ]

    async def start(self):
        for url in self.start_urls:
            yield Request(url, headers={"x-request-from": urljoin(url, "/locations/")})

    def extract_json(self, response):
        json_data = response.json()
        if localities := json_data.get("Localities"):
            return localities
        else:
            return json_data["Locations"]

    def post_process_item(self, item, response, location):
        item.pop("name")
        item["street_address"] = merge_address_lines([location["Address1"], location["Address2"]])
        item["unit"] = location["Address2"]
        item["ref"] = location["FranchiseLocationID"]
        item["branch"] = location["FriendlyName"]
        item["website"] = response.urljoin(location["Path"])

        if location["StorefrontImage"]:
            item["image"] = response.urljoin(location["StorefrontImage"])

        if location["Country"] == "AUS":
            item["name"] = item["brand"] = "Signwave"
            item["brand_wikidata"] = "Q136850122"

        yield item
