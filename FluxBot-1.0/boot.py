from indicatorLight import IndicatorLight
from scheduler import Scheduler
from pcf8523 import PCF8523
from machine import I2C
from machine import RTC
import pycom
import utime
import time

pycom.heartbeat(False)
bootLight = IndicatorLight(IndicatorLight.BLUE, 0.3, 0.2)
bootTime = utime.ticks_ms()
while (bootTime + 2*1000 >= utime.ticks_ms()):
    bootLight.pulse()
    print("Booting")




Scheduler()
#Scheduler.waitForDetonation()
Scheduler.runBurst()   