import scrapy

from locations.dict_parser import DictParser


class BlazePizzaSpider(scrapy.Spider):
    name = "blaze_pizza"
    item_attributes = {"brand": "Blaze Pizza", "brand_wikidata": "Q23016666"}
    allowed_domains = ["nomnom-prod-api.blazepizza.com"]
    start_urls = ["https://nomnom-prod-api.blazepizza.com/restaurants"]

    def parse(self, response):
        for location in response.json()["restaurants"]:
            item = DictParser.parse(location)

            yield item
