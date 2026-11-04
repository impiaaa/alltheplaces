from scrapy.spiders import SitemapSpider

from locations.categories import Categories, apply_category
from locations.structured_data_spider import StructuredDataSpider


class PokeHouseUSSpider(SitemapSpider, StructuredDataSpider):
    name = "poke_house_us"
    item_attributes = {
        "brand": "Poké House",
        "brand_wikidata": "Q141990576",
    }
    sitemap_urls = ["https://poke.house/sitemap.xml"]
    sitemap_rules = [
        (r"/locations/", "parse"),
    ]
    search_for_image = False

    def post_process_item(self, item, response, ld_data, **kwargs):
        item["branch"] = item.pop("name").removeprefix("Poke House ")
        apply_category(Categories.FAST_FOOD, item)
        yield item
