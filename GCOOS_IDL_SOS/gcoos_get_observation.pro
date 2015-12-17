pro gcoos_get_observation,parameter,station_name,date_range,timestamp,values
;--------------------------------------------------------------------------
; IDL routine to pull data from a SOS getObservation service
; Inputs are parameter, station_name, and date_range.
; Routine returns an array of timestamps and values.
; Subroutine etl_data extract-transform-loads timestamps and values
; from string versions into Julian Day and floating point numbers
;--------------------------------------------------------------------------

; Input variables are string like these 

;date_range   = '2014-03-15T00:00:00/2014-05-15T12:00:00'
;parameter    = 'air_temperature'
;station_name = 'urn:ioos:station:disl:bsca1'

prefix0 = 'http://data.gcoos.org:8080/52nSOS/sos/kvp?service=SOS&version=1.0.0&request=GetObservation&offering=urn:ioos:network:gcoos:all&observedProperty=http%3A%2F%2Fmmisw.org%2Font%2Fcf%2Fparameter%2F'
prefix1 = '&procedure='
prefix2 = '&responseFormat=text%2Fxml%3B%20subtype%3D%22om%2F1.0.0%2Fprofiles%2Fioos_sos%2F1.0%22&eventtime='
infile  = prefix0+parameter+prefix1+station_name+prefix2+date_range

hash = read_xml8(infile)
om_member = hash["om_ObservationCollection","om_member"]
observation_data = om_member["om_Observation","om_result","swe2_DataRecord","swe2_field",1]
time_series = observation_data["swe2_DataArray","swe2_values","_text"]
etl_data,time_series,timestamp,values

return
end
