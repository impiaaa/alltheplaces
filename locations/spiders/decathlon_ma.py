from chompjs import parse_js_object
from scrapy import Spider

from locations.dict_parser import DictParser
from locations.hours import DAYS, DAYS_FR, OpeningHours
from locations.pipelines.address_clean_up import clean_address
from locations.spiders.decathlon_fr import DecathlonFRSpider


class DecathlonMASpider(Spider):
    name = "decathlon_ma"
    item_attributes = DecathlonFRSpider.item_attributes
    start_urls = ["https://www.decathlon.ma/content/154-filialen-decathlon"]

    def parse(self, response):
        js_blob = response.xpath('//script[contains(text(), ",stores=[{")]/text()').get()

        js_blob_markers = (
            js_blob.split(",store_marker=", 1)[1].split(",store_name=", 1)[0].replace('\\"', "'").replace("\\/", "/")
        )
        markers = parse_js_object(js_blob_markers, unicode_escape=True)
        markers = {marker["store_number"]: marker for marker in markers}

        js_blob_stores = js_blob.split(",stores=", 1)[1].split(",zoom=", 1)[0].replace('\\"', "'").replace("\\/", "/")
        locations = parse_js_object(js_blob_stores, unicode_escape=True)

        for location in locations:
            location["hours"] = parse_js_object(location["hours"])
            location["website"] = markers[location["store_number"]]["link"]
            item = DictParser.parse(location)

            item["ref"] = str(location["store_number"])
            item["street_address"] = clean_address([location["address1"], location["address2"]])

            item["opening_hours"] = OpeningHours()
            for day_number, day_hours in enumerate(location["hours"]):
                for time_range in day_hours:
                    hours_string = time_range.replace("H", ":")
                    item["opening_hours"].add_ranges_from_string(
                        f"{DAYS[day_number]} {hours_string}", days=DAYS_FR, delimiters=["-", "à", "a", ","]
                    )

            yield item
