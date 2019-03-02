"""
Sample to read CRS from shapefile and transform coordinates of bounding box.

Mark Foley
Feb. 2019
"""
import gdal_workaround
import fiona
from fiona.crs import from_string, from_epsg, to_string
import pyproj_transformation as pt

# file = ".cache/geonames_pop5000.shp"
# file = ".cache/geonames_pop_5000.shp"
# file = "gageom/gageom_itm.shp"
# file = "data/landuse2.gpkg"

file = input("Enter a shapefile name in the format of path/to/file.shp ")


with fiona.open(file, 'r') as source:
    # for feature in source:
    #     print("{} {}"
    #           .format(feature["properties"]["countyname"],
    #                   feature["properties"]["total2011"]))

    print("\n{}\n".format("=" * 20))
    print("There are {} features in source.".format(len(source)))
    print("The SRID of source is {}".format(to_string(source.crs)))
    print("The bounding box of source is \n{}".format(source.bounds))

    target_crs = "epsg:4326"
    in_pair_sw = source.bounds[0], source.bounds[1]
    in_pair_ne = source.bounds[2], source.bounds[3]

    print("The bounding box is converted from {} to {}.\n".format(to_string(source.crs), target_crs))
    print("SW: {}".format(pt.transform_coordinates(source.crs, target_crs, in_pair_sw)))
    print("NE: {}".format(pt.transform_coordinates(source.crs, target_crs, in_pair_ne)))
    # bbox = source.bounds
