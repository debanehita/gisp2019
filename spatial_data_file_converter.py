"""
This prgram converts spatial data from any any format supported by OGR to any other.

Examples of formats supported by OGR are ESRI Shapefile, GeoJSON and Geopackage.
The full list is available on fiona.supported_drivers, a summary of which is printed for
info.


Mark Foley
Feb. 2019
"""
try:
    from shapely.geometry import mapping, shape, Polygon, MultiPolygon, LineString, MultiLineString
    from shapely import wkt

    # Fixes inconsistencies in finding osgeo when run in MS Windows
    import gdal_workaround

    # We import a dictionary of valid file extensions matched with OGR-supported drivers.
    # We will use this to ensure that the file opened is in a valid format.
    import fiona_supported_drivers as fsd

    import fiona
    # from fiona.crs import from_string, from_epsg, to_string
    import os

    # Make a list of valid file extensions
    from collections import OrderedDict

    valid_file_extensions = OrderedDict({k: v for k, v in fsd.file_extensions.items() if v})
    print("=" * 80, "\nSupported formats")
    for k, v in valid_file_extensions.items():
        print("  {} - {}".format(k, v))
    print("=" * 80)

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

    # output is any filename as a string. Use "path/to/file.xxx" format. If the file doesn't exist, we raise an error.
    output_file = input("OUTPUT: Enter path/to/filename.xxx. Leaveblank for default. ")
    if output_file:
        # Check that we have a valid file type
        sink_dir = os.path.dirname(output_file)
        sink_file = os.path.basename(output_file)
        sink_file_ext = sink_file.split(".")
        if sink_file_ext[-1] not in valid_file_extensions.values():
            raise TypeError("OUTPUT {} is not a valid file extension.".format(sink_file_ext[-1]))
        sink_type = sink_file_ext[-1]
    else:
        sink_type = input("INPUT Enter output format suffix e.g 'shp', 'gpkg' or 'json' ")
        # Check that we have a valid output file type
        if sink_type not in valid_file_extensions.values():
            raise TypeError("INPUT {} is not a valid file extension.".format(sink_type))
        sink_dir = source_dir
        sink_file = source_file_ext[0] + ".{}".format(sink_type)
        output_file = os.path.join(sink_dir, sink_file)

    sink_driver = None
    for k, v in valid_file_extensions.items():
        if v == sink_type:
            sink_driver = k
            break
    if not sink_driver:
        raise TypeError("Could not determine output driver")

    # 'fiona.Env()' probes the GDAL environment to check that config options are set.
    # The discovered options are reinstated when the Fiona environment exits.
    with fiona.Env():
        for lyr in fiona.listlayers(input_file):
            # Open each layer
            with fiona.open(input_file, 'r', layer=lyr) as source:
                # Print layer info
                print("\n{}\n".format("=" * 20))
                print("There are {} features in source.".format(len(source)))
                print("CRS: {}\n{}".format(source.crs, source.crs_wkt))
                print("The Geometry type of source is {}".format(source.schema["geometry"]))
                print("The bounding box of source is \n{}".format(source.bounds))

                sink_schema = source.schema
                if source.schema["geometry"] == "Polygon":
                    sink_schema["geometry"] = "MultiPolygon"
                elif source.schema["geometry"] == "LineString":
                    sink_schema["geometry"] = "MultiLineString"
                else:
                    pass

                params = {'crs': source.crs,
                          'crs_wkt': source.crs_wkt,
                          'driver': sink_driver,
                          'schema': sink_schema}
                # We only allow layers with GPKG for the moment
                if sink_driver == "GPKG":
                    params["layer"] = lyr

                print ("\nOpening {} with {}.".format(output_file, params))
                with fiona.open(
                        output_file, 'w',
                        **params,
                ) as sink:
                    for feature in source:
                        # Write out incoming feature to output file

                        # Turn the GeoJSON-formatted geometry into its geometric object
                        # equivalent using Shapely 'shape'.
                        geom = shape(feature['geometry'])

                        # In some instances (shapefile) the input geometry is reported as
                        # LinsSting or Polygon when it should really be MultiLineString or
                        # MultiPolygon. We fix this here.
                        if isinstance(geom, Polygon):
                            geom = wkt.loads(geom.wkt)
                            geom = MultiPolygon([geom])
                        elif isinstance(geom, LineString):
                            geom = wkt.loads(geom.wkt)
                            geom = MultiLineString([geom])

                        # Turn the geometric object back into its GeoJSON-formatted
                        # equivalent using Shapely 'mapping'.
                        feature['geometry'] = mapping(geom)
                        sink.write(feature)


except Exception as e:
    # Handle any errors and end gracefully
    print("=" * 80)
    print("ERROR: {}".format(e))
    print("=" * 80)
    quit(1)
