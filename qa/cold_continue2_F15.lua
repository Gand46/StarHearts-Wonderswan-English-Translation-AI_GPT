local out=assert(os.getenv('MESEN_OUTDIR'));local frame=0
emu.addEventCallback(function() local t={};if frame>=80 and frame<85 then t.a=true end;if frame>=180 and frame<185 then t.a=true end;emu.setInput(t,0) end,emu.eventType.inputPolled)
emu.addEventCallback(function() frame=frame+1;if frame>=50 and frame<=450 and frame%25==0 then local f=assert(io.open(string.format('%s/f%04d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close()end;if frame>=480 then emu.stop(0)end end,emu.eventType.endFrame)
