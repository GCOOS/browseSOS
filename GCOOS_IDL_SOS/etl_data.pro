pro etl_data,time_series,timestamp,values

;----------------------------------------------------------
; Locate the timestamps in the time_series string
; extract series of 'timestamp,variablename,value' strings
; transform timestamp into IDL Julian day values
; load julian time into timestamp and variable arrays.
; Matthew Howard, circa 2015 
;----------------------------------------------------------

; Use regular expression to find timestamp. 
; Timestamp is defined as 23 characters followed by a Z

pos = strsplit(time_series,'.......................Z',/REGEX,length=len,count=count)

; Adjust the starting position 24 characters ahead and increase the lengths by 24

pos = pos-24 &  len = len+24

; Allocate storage for the timestamp and data arrays

timestamp = dblarr(count)
values    = fltarr(count)

;----------
; Main loop
;----------

for i = 0,count-1 do begin

    result = strmid(time_series,pos(i),len(i))
    tokens = strsplit(result,',',/extract)
    year   = strmid(tokens(0), 0,4)
    month  = strmid(tokens(0), 5,2)
    day    = strmid(tokens(0), 8,2)
    hour   = strmid(tokens(0),11,2)
    minute = strmid(tokens(0),14,2)
    second = strmid(tokens(0),17,6)

    values(i)    = float(tokens(2))
    timestamp(i) = julday(month,day,year,hour,minute,second)

     print,'etl_data: ',year,' ',month,' ',day,' ',hour,' ',minute,' ',second,' ',values(i)
;    print,tokens

endfor
return
end
