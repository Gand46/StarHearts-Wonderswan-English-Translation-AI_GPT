local out=assert(os.getenv('MESEN_OUTDIR'));local frame=0
emu.addEventCallback(function()
 local t={}
 if frame>=80 and frame<85 then t.a=true end -- show title menu
 if frame>=180 and frame<185 then t.a=true end -- Continue
 if frame>=360 and frame<380 then t.up2=true end -- Save Drum
 if frame>=530 and frame<535 then t.a=true end -- confirm Yes
 if frame>=700 and frame<705 then t.a=true end
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function() frame=frame+1;if frame>=50 and frame<=850 and frame%25==0 then local f=assert(io.open(string.format('%s/f%04d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close()end;if frame>=880 then emu.stop(0)end end,emu.eventType.endFrame)
