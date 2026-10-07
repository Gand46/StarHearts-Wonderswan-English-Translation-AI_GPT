local outdir=assert(os.getenv('MESEN_OUTDIR')); local report=assert(os.getenv('MESEN_LUA_REPORT')); local frame=0
local shots={830,860,900,940,980,1020,1060,1100,1140,1180,1220,1260,1300}; local ss={}; for _,v in ipairs(shots) do ss[v]=true end
local ap={200,240,280,320,360,400,440,480,520,560,600,640,680,720,760}
local function hit(list,f,w) for _,s in ipairs(list) do if f>=s and f<s+(w or 3) then return true end end return false end
emu.addEventCallback(function()
 local t={a=hit(ap,frame,3),b=false,start=false,up=false,down=false,left=false,right=false,up2=false,down2=false,left2=false,right2=false}
 if frame>=820 and frame<825 then t.start=true end
 if frame>=880 and frame<910 then t.right=true end
 if frame>=920 and frame<950 then t.down=true end
 if frame>=960 and frame<990 then t.left=true end
 if frame>=1000 and frame<1030 then t.up=true end
 if frame>=1040 and frame<1070 then t.right2=true end
 if frame>=1080 and frame<1110 then t.down2=true end
 if frame>=1120 and frame<1150 then t.left2=true end
 if frame>=1160 and frame<1190 then t.up2=true end
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function() frame=frame+1; if ss[frame] then local f=assert(io.open(string.format('%s/f%04d.png',outdir,frame),'wb')); f:write(emu.takeScreenshot()); f:close() end; if frame==1300 then local f=assert(io.open(report,'w')); f:write('ok\n'); f:close(); emu.stop(0) end end,emu.eventType.endFrame)
