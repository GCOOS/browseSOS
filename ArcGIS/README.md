Currently IOOS suggests 3 SOS clients    (http://catalog.ioos.us/help/download/) to access SOS to retrieve information and data: Pyoos, the Environmental Data Connector (EDC) and 52n Sensor Web Client.

EDC works well with Data Integration Framework (DIF) SOS. However it doesn’t work with new IOOS-build SOS (IOOS SOS) that GCOOS and other 2 Regional Association have adopted.

This project will provide a python toolbox (pyoos-base) to access IOOS-SOS and create a layer for ArcMap.
Currently, pyoos collects only certain information: <a href="https://gist.github.com/otwn/7aa5ed6e03684edeca73">https://gist.github.com/otwn/7aa5ed6e03684edeca73</a> 

With ArcGIS Server SOS Extension developed by 52North and ESRI, it allows querying of observations, metadata about procedures (= sensors), as well as descriptions of features (of interest) observed by the sensors.


![GCOOS browse SOS ArcGIS](http://data.gcoos.org/documents/browseSOS_ArcGIS.png)
