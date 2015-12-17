#gcoos_sos_utils.py
A set of simple python routines to demonstrate retrieving data from a SOS server. These utilities are a work in progress. They'll be continually updated and improved as time allows. You will need to modify this code to suit your pupose.

We use ConfigParser to build the url for the different services. Not all RAs are running the same version of SOS so there will be some tweaking required in both the URL construction and the XML parsing. BeautifulSoup's html.parser isn't the best parser for this task -- we need to test with lxml. In any case, there will be differences between RAs, so your mileage may vary. This code is known to work with the GCOOS-RA SOS server.

###Examples
######Getting count of all stations in catalog:
    print "Total stations: %d" % len(gcoos_get_all_stations(r_a)) ->

       Total stations: 230

######gcoos_describe_sensor(r_a, urn):
    gcoos_describe_sensor('gcoos', 'urn:ioos:station:nerrs:apaebwq') ->

        {"geometry": {"coordinates": [-84.8752, 29.7858], "type": "Point"}, "header": {"Description": "East Bay Bottom", "Organization": "National Estuarine Research Reserve System, NOAA", "Sensors": ["Sea Water Practical Salinity", "Sea Water Turbidity", "Mass Concentration Of Oxygen In Sea Water", "Sea Water Temperature"], "Station": "urn:ioos:station:nerrs:apaebwq"}, "properties": {}, "type": "Feature"}

#####Getting all sensors as GeoJSON feature collection:
    the_collection = []
    for station in gcoos_get_all_stations('gcoos'):
        the_collection.append(gcoos_describe_sensor('gcoos', station))
    the_fc = FeatureCollection(the_collection)

###Architecture
![GCOOS browse SOS python](http://data.gcoos.org/documents/browseSOS_python.png)
