from scrapy.spiders import CSVFeedSpider

from locations.categories import Categories, Extras, Fuel, PaymentMethods, apply_category, apply_yes_no
from locations.dict_parser import DictParser


class ArcoSpider(CSVFeedSpider):
    name = "arco"
    start_urls = ["https://www.arco.com/img/findstation/MasterArcoStoreLocations.csv"]
    item_attributes = {"brand": "Arco", "brand_wikidata": "Q304769"}

    def parse_row(self, response, row):
        item = DictParser.parse(row)
        apply_category(Categories.FUEL_STATION, item)

        item["street_address"] = item.pop("addr_full")

        apply_yes_no(PaymentMethods.CREDIT_CARDS, item, row["CreditCards"] == "1")
        apply_yes_no(Fuel.DIESEL, item, row["Diesel"] == "1")
        apply_yes_no(Extras.CAR_WASH, item, row["CarWash"] == "1")

        # "Renewable diesel is a fuel made from fats and oils, such as soybean oil or canola oil, and is processed to be chemically the same as petroleum diesel. … Renewable diesel and biodiesel are not the same fuel."
        # https://afdc.energy.gov/fuels/renewable_diesel.html
        apply_yes_no("fuel:renewable_diesel", item, row["RenewableDiesel"] == "1")

        yield item
