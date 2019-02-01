"""
Added a docstring
"""
import gdal_workaround
import shapely
from shapely.geometry import Polygon, MultiPolygon, shape
import fiona

SEARCH_STRING = "ongford"
SEARCH_PROPERTY = "countyname"
SOURCE = "counties/ctygeom.shp"

with fiona.open(SOURCE) as source:
    for feature in source:
        if SEARCH_STRING in feature["properties"][SEARCH_PROPERTY]:
            search_feature = feature
            search_feature_type = type(shape(search_feature["geometry"]))
            search_poly = search_feature_type(shape(search_feature["geometry"]))
            break

with fiona.open(SOURCE) as source:
    for feature in source:
        feature_type = type(shape(feature["geometry"]))
        feature_poly = feature_type(shape(feature["geometry"]))
        if feature_poly.touches(search_poly):
            print(feature["properties"][SEARCH_PROPERTY])



