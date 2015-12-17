#gcoos_sos_utils.py
A set of simple python routines to demonstrate retrieving data from a SOS server. These utilities are a work in progress. They'll be continually updated and improved as time allows. You will need to modify this code to suit your pupose.

We use ConfigParser to build the url for the different services. Not all RAs are running the same version of SOS so there will be some tweaking required in both the URL construction and the XML parsing. BeautifulSoup's html.parser isn't the best parser for this task -- we need to test with lxml. In any case, there will be differences between RAs, so your mileage may vary. This code is known to work with the GCOOS-RA SOS server.

###Examples
######Getting all stations in catalog:
    print "Total stations: %d" % len(gcoos_get_all_stations(r_a)) ->

       Total stations: 230

######gcoos_describe_sensor(r_a, urn):
    gcoos_describe_sensor('gcoos', 'urn:ioos:station:nerrs:apaebwq') ->

    GeoJSON output:
