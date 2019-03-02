"""
Read the contents of any geospatial data file. It returns
* Layer info
* For each layer
  - File format
  - Geometry type
  - CRS info
  - Number of features
  - Bounding Box coordinates
  - Number and name of property attributes
  - For each feature
    . Id
    . Geometry type
    . Name and value of each property

This can read any format supported by OGR such as ESRI Shapefile, GeoJSON and Geopackage.
The full list is available on fiona.supported_drivers, a summary of which is printed for
info.

Mark Foley
March 2019
"""
try:
    # Fixes inconsistencies in finding osgeo when run in MS Windows
    import gdal_workaround

    # We import a dictionary of valid file extensions matched with OGR-supported drivers.
    # We will use this to ensure that the file opened is in a valid format.
    import fiona_supported_drivers as fsd

    import fiona
    import os

    # Make a list of valid file extensions
    from collections import OrderedDict
    valid_file_extensions = OrderedDict({k:v for k,v in fsd.file_extensions.items() if v})
    print("="*80, "\nSupported formats")
    for k,v in valid_file_extensions.items():
        print("  {} - {}".format(k,v))
    print("="*80)

    # input_file is any filename as a string. Use "path/to/file.xxx" format. If the file doesn't exist, we raise an error.
    input_file = input("Enter path/to/filename.xxx ")
    if not os.path.isfile(input_file):
        raise IOError("{} is an invalid filename".format(input_file))

    # Check that we have a valid file type
    source_dir = os.path.dirname(input_file)
    source_file = os.path.basename(input_file)
    source_file_ext = source_file.split(".")
    if source_file_ext[-1] not in valid_file_extensions.values():
        raise TypeError("{} is not a valid file extension.".format(source_file_ext[-1]))

    # 'fiona.Env()' probes the GDAL environment to check that config options are set.
    # The discovered options are reinstated when the Fiona environment exits.
    with fiona.Env():

        # Some file formats such as geopackage scan support multiple layers in the same file.
        # Others such as shapefile can have only one layer.
        for lyr in fiona.listlayers(input_file):
            print("=" * 80)
            print("Layers: {} ({})".format(len(fiona.listlayers(input_file)), lyr))

            # Open each layer
            with fiona.open(input_file, 'r', layer=lyr) as source:
                # Print layer info
                print("File fomat: {}".format(source.driver))
                print("Geometry Type: {}".format(source.schema["geometry"]))
                print("CRS: {}\n{}".format(source.crs, source.crs_wkt))
                print("Features: {}".format(len(source)))
                print("Bounds: {}".format(source.bounds))
                print("Num properties: {}".format(len(source.schema["properties"])))
                for k,v in source.schema["properties"].items():
                    print("  {}: {}".format(k,v))
                print("+-"*40)

                for feature in source:

                    # Print info for each feature
                    print("Id: {}".format(feature["id"]))
                    print("Geometry Type: {}".format(feature["geometry"]["type"]))
                    for k,v in feature["properties"].items():
                        print("  {}: {}".format(k,v))
                    print("-"*80)

    print("="*80)
except Exception as e:
    # Handle any errors and end gracefully
    print("=" * 80)
    print("ERROR: {}".format(e))
    print("=" * 80)
    quit(1)