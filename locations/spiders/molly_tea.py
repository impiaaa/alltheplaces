from locations.categories import Categories, apply_category
from locations.storefinders.agile_store_locator import AgileStoreLocatorSpider


class MollyTeaSpider(AgileStoreLocatorSpider):
    name = "molly_tea"
    allowed_domains = ["usa.mollytea.com"]
    item_attributes = {
        "brand": "Molly Tea",
        "brand_wikidata": "Q137167825",
    }

    def post_process_item(self, item, response, feature):
        item["branch"] = item.pop("name").removeprefix("Molly Tea").strip(" ()")
        apply_category(Categories.CAFE, item)
        apply_category({"cuisine": "bubble_tea"}, item)
        yield item
