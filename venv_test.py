"""
You can use this file to test if your standard GIS-related imports work.
"""

try:
    import gdal_workaround
    import turtle as t
    from shapely.geometry import mapping
    from shapely.wkt import loads
    import psycopg2
    import psycopg2.extras
    import fiona
    from fiona.crs import from_epsg
    import pyproj
    from osgeo import ogr
    from osgeo import gdal

    print("Didn't see any import errors")

except Exception as e:
    print("{}".format(e))
