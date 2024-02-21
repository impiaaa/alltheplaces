import json

from locations.categories import Categories, apply_category
from locations.linked_data_parser import LinkedDataParser
from locations.structured_data_spider import StructuredDataSpider


class PizzaMyHeartUSSpider(StructuredDataSpider):
    name = "pizza_my_heart_us"
    start_urls = ["https://www.pizzamyheart.com/store-locator/"]
    item_attributes = {"brand": "Pizza My Heart", "brand_wikidata": "Q7199970"}
    wanted_types = ["Organization", "FoodEstablishment"]

    def parse(self, response):
        start = response.text.find("locations: ")
        end = response.text.find(",\n", start)
        self.locations = {l["name"]: l for l in json.loads(response.text[start + len("locations: ") : end])}
        yield from super().parse(response)

    def pre_process_data(self, ld_data, **kwargs):
        if ld_data["name"] in self.locations:
            loc = self.locations[ld_data["name"]]
            ld_data["geo"] = {"latitude": loc["lat"], "longitude": loc["lng"]}

    def post_process_item(self, item, response, ld_data):
        apply_category(Categories.RESTAURANT, item)
        apply_category({"cuisine": "pizza"}, item)
        yield item

    def iter_linked_data(self, response):
        for ld_obj in super().iter_linked_data(response):
            yield ld_obj
            for sub in ld_obj.get("subOrganization", []):
                if not sub.get("@type"):
                    continue

                types = sub["@type"]

                if not isinstance(types, list):
                    types = [types]

                types = [LinkedDataParser.clean_type(t) for t in types]

                for wanted_types in self.wanted_types:
                    if isinstance(wanted_types, list):
                        if all(wanted in types for wanted in wanted_types):
                            yield sub
                    elif wanted_types in types:
                        yield sub
