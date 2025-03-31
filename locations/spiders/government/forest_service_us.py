from locations.categories import apply_category
from locations.storefinders.arcgis_feature_server import ArcGISFeatureServerSpider


class ForestServiceUSSpider(ArcGISFeatureServerSpider):
    name = "forest_service_us"
    item_attributes = {
        "operator": "United States Forest Service",
        "operator_wikidata": "Q1891156",
    }
    download_timeout = 30
    host = "apps.fs.usda.gov"
    context_path = "fsgisx05"
    service_id = "wo_nfs_gtac/GTAC_IVMQuery_01"
    server_type = "MapServer"
    layer_id = "4"
    max_record_count = 9
    extra_parameters = "geometryPrecision=4"

    def post_process_item(self, item, response, location):
        apply_category({"boundary": "protected_area"}, item)
        del item["state"]
        item["ref"] = location["OBJECTID"]
        item["name"] = location["COMMONNAME"]
        yield item
