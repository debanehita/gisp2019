PARAMS = {
    "host": "mf2.dit.ie:8080",
    "layer": "cso:ctygeom",
    "srs_code": 29902,
    "properties": ["countyname", ],
    "geom_field": "geom",
    "filter_property": "countyname",
    "filter_values": ["Cork", "Kerry"]
}

def get_geojson(params):
    """
    This function accepts a dictionary of parameters and returns a GeoJSON representation of the requested layer. This
    takes a format similar to the following example:

    {
        "host": "mf2.dit.ie:8080",
        "layer": "cso:ctygeom",
        "srs_code": 29902,
        "properties": ["countyname", ],
        "geom_field": "geom",
        "filter_property": "countyname",
        "filter_values": ["Cork", "Kerry"]
    }

    You can filter the set of features returned by adjusting "filter_values". This is a list of values that must
    be present in "filter_property". In the above example you'd get the counties of Cork and Kerry plus Cork City.
    Similarly, you can filter the properties returned to reduce their number. If you use this feature, you'll need to
    set "geom_field" to the name of the geometry field. Geoserver can give you this.

    All values in the dictionary are optional except "host" and "layer".

    :param Dictionary as above:
    :return: Parsed GeoJSON or exception as appropriate
    """

    import urllib.parse
    import httplib2
    import os, os.path
    import json
    import xml.etree.ElementTree as etree

    #
    # Check that the parameters exist and/or sensible. Because the filter can contain some 'odd' characters such as '%'
    # and single quotes the filter text needs to be url encoded so that text like "countyname LIKE '%Cork%'" becomes
    # "countyname%20LIKE%20%27%25Cork%25%27" which is safer for URLs
    #
    if "host" not in params:
        raise ValueError("Value for 'host' required")
    if "layer" not in params:
        raise ValueError("Value for 'layer' required")
    if "srs_code" in params and params["srs_code"]:
        srs_text = "&srsName=epsg:{}".format(params["srs_code"])
    else:
        srs_text = ""
    if "properties" in params and params["properties"]:
        item_string = ""
        for item in params["properties"]:
            item_string += str(item) + ","
        if "geom_field" in params and params["geom_field"]:
            item_string += str(params["geom_field"])
        property_text = "&PROPERTYNAME={}".format(item_string)
    else:
        property_text = ""
    if "filter_property" in params and params["filter_property"] and params["filter_values"]:
        filter_text = "{filter_property} LIKE '%{filter_values}%'".format(filter_property=params["filter_property"], filter_values=params["filter_values"][0])
        for item in range(1, len(params["filter_values"])):
            filter_text += "OR {filter_property} LIKE '%{filter_values}%'".format(filter_property=params["filter_property"], filter_values=params["filter_values"][item])
        filter_text = urllib.parse.quote(filter_text)
        filter_text = "&CQL_FILTER=" + filter_text
    else:
        filter_text = ""

    url = "http://{host}/geoserver/ows?" \
          "service=WFS&version=1.0.0&" \
          "request=GetFeature&" \
          "typeName={layer}&" \
          "outputFormat=json".format(host=params["host"], layer=params["layer"])
    url += srs_text
    url += property_text
    url += filter_text

    #
    # Make a directory to hold downloads so that we don't have to repeatedly download them later, i.e. they already
    # exist so we get them from a local directory. This directory is called .httpcache".
    #
    scriptDir = os.path.dirname(__file__)
    cacheDir = os.path.normpath(os.path.join(scriptDir, ".httpcache"))
    if not os.path.exists(cacheDir):
        os.mkdir(cacheDir)

    #
    # Go to the web and attempt to get the resource
    #
    try:
        h = httplib2.Http()
        response_headers, response = h.request(url)
        response = response.decode()

        #
        # Geoserver only sends valid data in the requested format, in our case GeoJSON, so if we get a response back in
        # XML format we know that we have an error. We do minimal parsing on the xml to extract the error text and raise
        # an exception based on it.
        #
        if response[:5] == "<?xml":
            response = etree.fromstring(response)
            xml_error = ""
            for element in response:
                xml_error += element.text
            raise Exception(xml_error)
        else:
            return json.loads(response)

    except httplib2.HttpLib2Error as e:
        print(e)


def main():
    my_data = get_geojson(PARAMS)
    print(my_data)


if __name__ == "__main__":
    main()

