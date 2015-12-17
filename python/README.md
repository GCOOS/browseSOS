These utilities are a work in progress. They'll be continually updated
 and improved as time allows. 

We now use ConfigParser to build the url for the different services. Not all
RAs are running the same version of SOS so there will be some tweaking required
in both the URL construction and the XML parsing. html.parser isn't the best
parser for this task -- we need to test with lxml. In any case, there will
be differences between RAs, so your mileage may vary. This code is known to
work with the GCOOS-RA SOS server.


