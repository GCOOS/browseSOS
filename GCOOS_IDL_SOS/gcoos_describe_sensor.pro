pro gcoos_describe_sensor,station_name,start_time,end_time
;-----------------------------------------------------------------------------------
; This routine calls the GCOOS SOS Describe Sensor service for a given station name
; It returns a list of start and end times for which data are available.
; The end time of "unknown" means the data are still being collected.
; Station names take on this form station_name = 'urn:ioos:station:nerrs:apaebwq'
;-----------------------------------------------------------------------------------

prefix = 'http://data.gcoos.org:8080/52nSOS/sos/kvp?service=SOS&version=1.0.0&request=DescribeSensor&procedure='
suffix = '&outputFormat=text%2Fxml%3B%20subtype%3D%22sensorML%2F1.0.1%2Fprofiles%2Fioos_sos%2F1.0%22'
infile = prefix+station_name+suffix

hash   = read_xml8(infile)
start_time_key = hash["sml_SensorML","sml_member","sml_System","sml_validTime","gml_TimePeriod","gml_beginPosition"].keys()
start_time     = hash["sml_SensorML","sml_member","sml_System","sml_validTime","gml_TimePeriod","gml_beginPosition",start_time_key(0)]
end_time_key   = hash["sml_SensorML","sml_member","sml_System","sml_validTime","gml_TimePeriod","gml_endPosition"].keys()
end_time   = hash["sml_SensorML","sml_member","sml_System","sml_validTime","gml_TimePeriod","gml_endPosition",end_time_key(0)]
;print,hash["sml_SensorML","sml_member","sml_System","sml_validTime","gml_TimePeriod","gml_beginPosition","_text"]
;print,hash["sml_SensorML","sml_member","sml_System","sml_validTime","gml_TimePeriod","gml_endPosition"]  
return
end
