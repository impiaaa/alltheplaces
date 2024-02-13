from postal.parser import parse_address


def parse_address_dict(address, language=None, country=None):
    return dict(item[::-1] for item in parse_address(address, language=language, country=country))


def assign_if(addr, addr_key, item, item_key):
    if addr_key in addr and not item.get(item_key):
        item[item_key] = addr[addr_key]


class ParseAddressPipeline:
    def process_item(self, item, spider):
        if item.get("addr_full") and (
            not item.get("housenumber")
            or not item.get("street")
            or not item.get("city")
            or not item.get("state")
            or not item.get("postcode")
            or not item.get("country")
        ):

            addr = parse_address_dict(item["addr_full"], country=item.get("country") or None)
            assign_if(addr, "house_number", item, "housenumber")
            assign_if(addr, "road", item, "street")
            assign_if(addr, "city", item, "city")
            assign_if(addr, "state", item, "state")
            assign_if(addr, "postcode", item, "postcode")
            assign_if(addr, "country", item, "country")

        if item.get("street_address") and (not item.get("housenumber") or not item.get("street")):

            addr = parse_address_dict(item["street_address"], country=item.get("country") or None)
            assign_if(addr, "house_number", item, "housenumber")
            assign_if(addr, "road", item, "street")

        return item
