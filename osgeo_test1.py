# from gdal import ogr
import osgeo.ogr as ogr
shapefile = ogr.Open("counties/ctygeom.shp")
numLayers = shapefile.GetLayerCount()
print("Shapefile contains %d layers" % numLayers)
print()
for layerNum in range(numLayers):
    layer = shapefile.GetLayer(layerNum)
    spatialRef = layer.GetSpatialRef().ExportToProj4()
    numFeatures = layer.GetFeatureCount()
    print("Layer %d has spatial reference %s" % (layerNum, spatialRef))
    print("Layer %d has %d features" % (layerNum, numFeatures))
    print()

    for featureNum in range(numFeatures):
        feature = layer.GetFeature(featureNum)
        featureName = feature.GetField("countyname")
        print("Feature %d has name %s" % (featureNum, featureName))