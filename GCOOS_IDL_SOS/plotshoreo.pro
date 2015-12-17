PRO plotshoreo,color=color

ic     = 132

isdone = 0
zlon = fltarr(2000)
zlat = fltarr(2000)
npts2 = 0
jseg  = 0
openr,11,'shoredump2.gomi'
while not EOF(11) do begin
   readf,11,npts2,jseg
   for i = 0,npts2-1 do begin
       readf,11,a,b
       if(a gt 180.) then a = a-360.
       zlon(i) = a
       zlat(i) = b
       if(a lt -89. and a gt -91. and b gt 22. and b lt 27. ) then print,jseg
   endfor
   oplot,zlon(0:npts2-1),zlat(0:npts2-1),color=color
endwhile
close,11

return
end
