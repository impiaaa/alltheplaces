from locations.categories import Categories, apply_category
from locations.json_blob_spider import JSONBlobSpider


class PerspireSaunaUSSpider(JSONBlobSpider):
    name = "perspire_sauna_us"
    item_attributes = {
        "brand": "Perspire Sauna Studio",
    }
    start_urls = ["https://api.perspiresaunastudio.com/collection/69249c468f7a5302cc0ba903?all=true"]
    locations_key = "items"

    def pre_process_data(self, feature: dict) -> None:
        feature.update(feature.pop("fieldData"))

    def post_process_item(self, item, response, location):
        item["street_address"] = item.pop("addr_full", None)
        item["branch"] = item.pop("name")
        item["state"] = location["stateprovcode"]
        item["website"] = f"https://www.perspiresaunastudio.com/locations/{location['slug']}"
        apply_category(Categories.SAUNA, item)
        yield item
