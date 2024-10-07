from scrapy import Spider
from scrapy.http import JsonRequest

from locations.items import Feature


class LamarUSSpider(Spider):
    name = "lamar_us"
    item_attributes = {"operator": "Lamar Advertising", "operator_wikidata": "Q3216588"}

    def start_requests(self):
        yield JsonRequest(
            "https://ib.lamar.com/service/api/Inventory/Filtered",
            data={
                "current": {
                    "points": [
                        # Bounding box of the contiguous US
                        {"lat": 50, "long": -70},
                        {"lat": 25, "long": -70},
                        {"lat": 25, "long": -125},
                        {"lat": 50, "long": -125},
                    ]
                },
                "exclusionShapes": [],
            },
        )

    def parse(self, response):
        for structure in response.json()["structures"]:
            item = Feature()
            item["lat"] = structure["latitude"]
            item["lon"] = structure["longitude"]
            item["ref"] = structure["id"]
            item["extras"] = {
                "bulletins": {"advertising": "billboard"},
                "posters": {"advertising": "billboard"},
                "digital": {"advertising": "screen"},
                "jr posters": {"advertising": "billboard"},
                "wallscapes": {"advertising": "tarp"},
                "benches": {"amenity": "bench"},
                "shelters": {"amenity": "shelter"},
                "bus/rail routes": {},
                "airports": {},
            }[structure["panels"][0]["productType"].lower()]
            item["extras"]["sides"] = len(structure["panels"])
            item["extras"]["direction"] = structure["panels"][0]["heading"]
            yield item
