__author__ = 'mark'

import fiona
import pyproj

# FILE = ".cache/geonames_pop5000.shp"
# FILE = ".cache/geonames_pop_5000.shp"
FILE = "counties/ctygeom.shp"


def transform_coord_pair(source_srid, target_srid, in_pair):
    in_srid = pyproj.Proj(init="epsg:{}".format(source_srid))
    out_srid = pyproj.Proj(init="epsg:{}".format(target_srid))

    return pyproj.transform(in_srid, out_srid, in_pair[0], in_pair[1])


with fiona.open(FILE, 'r') as source:
    for feature in source:
        print("{} {}"
              .format(feature["properties"]["countyname"],
                      feature["properties"]["total2011"]))

    print("\n{}\n".format("=" * 20))
    print("There are {} features in source.".format(len(source)))
    print("The SRID of source is {}".format(source.crs))
    print("The bounding box of source is \n{}".format(source.bounds))

    target_crs = "4326"
    in_pair_sw = source.bounds[0], source.bounds[1]
    in_pair_ne = source.bounds[2], source.bounds[3]

    print("The bounding box is converted from {} to epsg:{}.\n".format(source.crs, target_crs))
    print("SW: {}".format(transform_coord_pair(source.crs["init"].split(":")[1], target_crs, in_pair_sw)))
    print("NE: {}".format(transform_coord_pair(source.crs["init"].split(":")[1], target_crs, in_pair_ne)))
    # bbox = source.bounds
