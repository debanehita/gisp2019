import osgeo.ogr

shapefile = osgeo.ogr.Open("counties/ctygeom.shp")
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(2)
print("Feature 2 has the following attributes:\n")
attributes = feature.items()
for key, value in attributes.items():
    print(" %s = %s" % (key, value))

geometry = feature.GetGeometryRef()
geometryName = geometry.GetGeometryName()

print("\nFeature's geometry data consists of a %s" % geometryName)
