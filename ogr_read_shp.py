import osgeo.ogr
shp = osgeo.ogr.Open("counties/ctygeom.shp")
num_layers = shp.GetLayerCount()

print("Shapefile contains {} layers".format(num_layers))

for lyr_num in range(num_layers):
    lyr = shp.GetLayer(lyr_num)
    srs = lyr.GetSpatialRef().ExportToProj4()
    num_features = lyr.GetFeatureCount()

    print("Layer {} has SRS {} and {} features.".format(lyr_num, srs, num_features))

    for feature_num in range(num_features):
        feature = lyr.GetFeature(feature_num)
        feature_name = feature.GetField("COUNTYNAME")
        print("\nFeature Id {} has name {}".format(feature_num, feature_name))

        attributes = feature.items()
        for key, value in attributes.items():
            try:
                print("    Key {} has value {}".format(key, value))
            except Exception as e:
                print("Error {}".format(str(e)))
                pass
