#gcoos_sos_utils.py
A set of simple python routines to demonstrate retrieving data from a SOS server. These utilities are a work in progress. They'll be continually updated and improved as time allows. You will need to modify this code to suit your pupose.

We use ConfigParser to build the url for the different services. Not all RAs are running the same version of SOS so there will be some tweaking required in both the URL construction and the XML parsing. BeautifulSoup's html.parser isn't the best parser for this task -- we need to test with lxml. In any case, there will be differences between RAs, so your mileage may vary. This code is known to work with the GCOOS-RA SOS server. 

Note: We are now using xml.etree.ElementTree as the XML parser in gcoos_get_observations. This provides a much more sane manner of navigating a non-html based XML document. We'll be migrating the other functions to xml.etree.ElementTree in the near future.

###Examples
#####Getting count of all stations in catalog:
    print "Total stations: %d" % len(gcoos_get_all_stations(r_a)) ->

       Total stations: 230

#####gcoos_describe_sensor(r_a, urn):
    gcoos_describe_sensor('gcoos', 'urn:ioos:station:nerrs:apaebwq') ->

        {"geometry": {"coordinates": [-84.8752, 29.7858], "type": "Point"}, "header": {"Description": "East Bay Bottom", "Organization": "National Estuarine Research Reserve System, NOAA", "Sensors": ["Sea Water Practical Salinity", "Sea Water Turbidity", "Mass Concentration Of Oxygen In Sea Water", "Sea Water Temperature"], "Station": "urn:ioos:station:nerrs:apaebwq"}, "properties": {}, "type": "Feature"}

#####Getting all sensors as GeoJSON feature collection:
######The returned feature collection is suitable for dropping into a Leaflet map.
    the_collection = []
    for station in gcoos_get_all_stations('gcoos'):
        the_collection.append(gcoos_describe_sensor('gcoos', station))
    the_fc = FeatureCollection(the_collection)

#####Getting the latest observation:
    gcoos_get_observation('gcoos', 'air_temperature', 'urn:ioos:station:disl:bsca1')->
       2015-12-18T11:30:00.000Z,disl_bsca1_airtemperature,8.64 
