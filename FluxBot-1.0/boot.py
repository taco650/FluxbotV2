from indicatorLight import IndicatorLight
from scheduler import Scheduler
import pycom
import utime

pycom.heartbeat(False)
bootLight = IndicatorLight(IndicatorLight.BLUE, 0.3, 0.2)
bootTime = utime.ticks_ms()
while (bootTime + 2*1000 >= utime.ticks_ms()):
    bootLight.pulse()
    print("Booting")

Scheduler()
#Scheduler.run()
Scheduler.runBurst()   