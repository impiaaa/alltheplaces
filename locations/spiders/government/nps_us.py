from locations.categories import apply_category
from locations.json_blob_spider import JSONBlobSpider


class NpsUSSpider(JSONBlobSpider):
    name = "nps_us"
    item_attributes = {
        "operator": "National Park Service",
        "operator_wikidata": "Q308439",
    }
    start_urls = [
        "https://central.nps.gov/units/api/v1/parks/findapark?pagesize=1000&sort=name+asc&apikey=CfJDEBe7xKJ8v6xZOMkh7AaUGF70dBe3"
    ]

    def post_process_item(self, item, response, location):
        apply_category({"boundary": "national_park"}, item)
        item["image"] = "https://www.nps.gov" + location["image"]["data"]["src"]
        item["website"] = f"https://www.nps.gov/{location['parkCode']}/index.htm"
        yield item
