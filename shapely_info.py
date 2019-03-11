"""
This program returns a bunch of characteristics of up to two geometric objects and the relationships between them.

Mark Foley,
March 2019.
"""
try:
    import gdal_workaround
    import fiona
    import shapely.geometry as geo
    import shapely
    from collections import OrderedDict
except ImportError as e:
    print("{}".format(e))
    quit(1)

def geom_info(g1, g2=None):
    """

    :param g1: A 'feature' such as you'd get when you use 'fiona' to iterate through a spatial data file
    :param g2: As above.
    :return: A tuple containing up to 3 dictionaries with info on the first feature, the second feature and the
    relationships between them.

    """
    try:
        if not(g1):
            raise ValueError("1st argument must be present.")
        if "geometry" not in g1:
            raise TypeError("1st argument doesn't look like a feature")
        if not isinstance(geo.shape(g1["geometry"]), shapely.geometry.base.BaseGeometry):
            raise TypeError("1st argument is not a spatial feature")
            quit(1)
        if g2 and "geometry" not in g2:
            raise TypeError("2nd argument doesn't look like a feature")
        if g2 and (not isinstance(geo.shape(g2["geometry"]), shapely.geometry.base.BaseGeometry)):
            raise TypeError("2nd argument is not a spatial feature")
            quit(1)

        g1_data = OrderedDict()
        g2_data = OrderedDict()
        relationship = OrderedDict()

        g1 = geo.shape(g1["geometry"])
        g1_data["area"] = g1.area
        g1_data["bounds"] = g1.bounds
        g1_data["length"] = g1.length
        g1_data["geom_type"] = g1.geom_type
        g1_data["has_z"] = g1.has_z
        # g1_data["is_ccw"] = g1.is_ccw
        g1_data["is_empty"] = g1.is_empty
        g1_data["is_ring"] = g1.is_ring
        g1_data["is_closed"] = g1.is_closed
        g1_data["is_valid"] = g1.is_valid
        g1_data["is_empty"] = g1.is_empty
        g1_data["is_simple"] = g1.is_simple

        if g2:
            g2 = geo.shape(g2["geometry"])
            g2_data["area"] = g2.area
            g2_data["bounds"] = g2.bounds
            g2_data["length"] = g2.length
            g2_data["geom_type"] = g2.geom_type
            g2_data["has_z"] = g2.has_z
            # g2_data["is_ccw"] = g2.is_ccw
            g2_data["is_empty"] = g2.is_empty
            g2_data["is_ring"] = g2.is_ring
            g2_data["is_closed"] = g2.is_closed
            g2_data["is_valid"] = g2.is_valid
            g2_data["is_empty"] = g2.is_empty
            g2_data["is_simple"] = g2.is_simple

            relationship["equals"] = g1.equals(g2)
            relationship["contains"] = g1.contains(g2)
            relationship["crosses"] = g1.crosses(g2)
            relationship["disjoint"] = g1.disjoint(g2)
            relationship["intersects"] = g1.intersects(g2)
            relationship["overlaps"] = g1.overlaps(g2)
            relationship["touches"] = g1.touches(g2)
            relationship["within"] = g1.within(g2)

            relationship["de9im"] = g1.relate(g2)

        return g1_data, g2_data, relationship

    except Exception as e:
        print("{}".format(e))
        quit(1)

if __name__ == "__main__":
    shp = "counties/ctygeom.shp"
    features = []
    with fiona.Env():
        with fiona.open(shp, "r") as fh:
            for feature in fh:
                if "Carlow" in feature["properties"]["countyname"] or\
                        "Kilkenny" in feature["properties"]["countyname"]:
                    features.append(feature)

    result = geom_info(features[0], features[1])
    print("g1 Info\n"+ "-"*20)
    for k, v in result[0].items():
        print("{}: {}".format(k, v))

    if result[1]:
        print("\ng2 Info\n"+ "-"*20)
        for k, v in result[1].items():
            print("{}: {}".format(k, v))

    if result[2]:
        print("\nRelationship Info\n"+ "-"*20)
        for k,v in result[2].items():
            print("{}: {}".format(k,v))
        print(" |i|b|e\n +-+-+-\ni|{0[0]}|{0[1]}|{0[2]}\nb|{0[3]}|{0[4]}|{0[5]}\ne|{0[6]}|{0[7]}|{0[8]}"
              .format(
            tuple([i for i in result[2]["de9im"]])
        ))