pro gcoos_get_sos_data

;----------------------------------------------------------------
; gcoos_get_capabilities will list the station names, etc.
; for the holding of the data.gcoos.org data portal.
; Typically, you'd only call this once to see what is available. 
; Then you can hard code calls to get particular station data
;----------------------------------------------------------------
gcoos_get_capabilities,station_name,station_lon,station_lat,start_time,end_time

;---------------------------------------------------------------
; Here we have hard coded the station, parameter and date-range
;---------------------------------------------------------------

station_name = 'urn:ioos:station:disl:bsca1'
parameter    = 'air_temperature'
date_range   = '2014-03-15T00:00:00/2014-05-15T12:00:00'

print,' '
print,'Fetching data from the GCOOS SOS'
print,'Station    = ',station_name
print,'Parameter  = ',parameter
print,'Date_range = ',date_range
print,' '
print,'This can take several minutes for large data requests.'
print,' '

;---------------------------------------------------------------
; gcoos_get_observations will fetch the requested data
;---------------------------------------------------------------

gcoos_get_observation,parameter,station_name,date_range,timestamp,values

;---------------------------------------------------------------
; Now make a couple of simple plots
;---------------------------------------------------------------

device,decomposed=0
background_color=253
plot_color      = 0
   !P.POSITION     = [0.10, 0.25, 0.95, 0.95]
   idummy          = LABEL_DATE(DATE_FORMAT=['%D','%M','%Y'])
   !X.TICKINTERVAL = 5
   !X.MINOR        = 2
   !X.TITLE        = 'Date-Time (UTC)'
   !Y.TITLE        = 'Temperature (Deg-C)'
   !P.CHARSIZE     = 2
    plot,timestamp,values,Background=background_color,title='RA: DISL  STATION: BSCA1 PARAMETER: AIR TEMPERATURE',XTICKFORMAT=['LABEL_DATE','LABEL_DATE','LABEL_DATE'],XTICKUNITS= ['Day','Month','Year'],ytitle='Deg C',color=plot_color

print,'Hit return for next plot'
kbrd = get_kbrd()

plot,[-98.,-80.],[18.,30.5],/nodata,/yno,xstyle=1,ystyle=1,color=0,background=254
plotshoreo,color=10
oplot,station_lon,station_lat,psym=4,color=0,symsize=2,thick=2

end 
