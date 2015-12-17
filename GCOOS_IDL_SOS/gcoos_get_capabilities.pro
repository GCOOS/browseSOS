pro gcoos_get_capabilities,station_name,station_lon,station_lat,start_time,end_time
;-------------------------------------------------------------------------------
; IDL 8.5 Routine to: 
; 	Send a "GetCapabilities" request to an IOOS SOS end point.
;       List the stations, locations, start/end times, and parameters available 
;       Query the user for a station, parameter, date/range and retrieve data.
;       Send a "GetObservation" call for data to an IOOS SOS end point.
;       Place data into IDL array
;       Do some simple plotting
;       Matthew K. Howard - circa December 2015.
;
;	Edward Shaya (University Maryland) wrote the codes
;       "read_xml8.pro", "idl2xml8.pro", and "str_clear.pro".
;       They are used here with his knowledge and permission.
;       Visit his GitHub site at https://github.com/Small-Bodies-Node/pds4-idl/
;-------------------------------------------------------------------------------

; The input file is the response to a "GetCapabilities" call to an SOS.
; The file can be a file on the local file system.

;infile = 'getcapabilities.xml'

;-----------------------------------------------------------------
; Or the input file can be the response to a remote SOS end point.
;-----------------------------------------------------------------

infile = 'http://data.gcoos.org:8080/52nSOS/sos/kvp?service=SOS&request=GetCapabilities&AcceptVersions=1.0.0'

; --------------------------------------------------------------------------------------------------------------
; Here we Use Ed Shaya's code to pull a GetCapabilities response into a hash composed of lists and other hashes.
; --------------------------------------------------------------------------------------------------------------

print,'Reading into the DOM -- please stand by'
hash = read_xml8(infile)

;-------------------------------------------------------------------------------------------------
; Offerings contain station names, features within each station and a list of available parameters
; Save the offerings into it's own branch for convenience,
; And besides, there's a limit of seven keys when accessing a hash.
;-------------------------------------------------------------------------------------------------

offerings         = hash["sos_Capabilities","sos_Contents","sos_ObservationOfferingList","sos_ObservationOffering"]
num_obs_offerings = n_elements(offerings)

station_name = strarr(num_obs_offerings)
station_lat  = fltarr(num_obs_offerings)
station_lon  = fltarr(num_obs_offerings)
start_time   = strarr(num_obs_offerings)
end_time     = strarr(num_obs_offerings)

;------------------------------------
;             Main loop
;------------------------------------

print,'Here is a list of station names, location, start-stop times followed by the list of available parameters.'
for i = 1,num_obs_offerings-1 do begin
   station_name(i) = offerings[i,"gml_name","_text"]
   position   = strsplit(offerings[i,"gml_boundedBy","gml_Envelope","gml_lowerCorner","_text"],/extract)
   station_lat(i) = float(position(0))
   station_lon(i) = float(position(1))
   gcoos_describe_sensor,station_name(i),starttime,endtime
   start_time(i) = starttime 
   end_time(i)   = endtime 

;--------------------------------------------------------------------------------
; Features of interest are usually a collection of vertical positions where data
; were collected like vertical position of ADCP bins. 
; In other cases, this can turn out to be useless information.
;--------------------------------------------------------------------------------

   n_features = n_elements(offerings[i,"sos_featureOfInterest"])
   fmt = '(i3.3,1x,a42,1x,f7.4,1x,f8.4,1x,a24,1x,a7,1x,i4.4)'
   print,i,station_name(i),station_lat(i),station_lon(i),start_time(i),end_time(i),n_features,format=fmt

;---------------------------------------------------------------------
; Properties are measured parameters expressed in their standard names
; For example;
;   http://mmisw.org/ont/cf/parameter/air_temperature
;   http://mmisw.org/ont/cf/parameter/sea_water_temperature
;   http://mmisw.org/ont/cf/parameter/wind_speed
;---------------------------------------------------------------------

   nproperty  = n_elements(offerings[i,"sos_observedProperty"])
   for k = 1,nproperty-1 do print,i,' ',offerings[i,"sos_observedProperty",k,"xlink_href"]

;   if(n_features eq 1) then begin
;      feature = offerings[i,"sos_featureOfInterest","xlink_href"]
;      print,i," ",0," ",name," ",position," ",start_time," ",end_time," ",feature
;   endif else begin
;      for j = 0,n_features-1 do begin
;         feature    = offerings[i,"sos_featureOfInterest",j,"xlink_href"]
;         print,i," ",j," ",name," ",position," ",start_time," ",end_time," ",feature
;      endfor
;   endelse
endfor

;save,station_lon,station_lat,filename='station_location.wve'
;device,decomposed=0
;plot,[-98.,-80.],[18.,30.5],/nodata,/yno,xstyle=1,ystyle=1,background=255
;oplot,station_lon,station_lat,psym=4,color=0
;plotshoreo

end 
