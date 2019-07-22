from indicatorLight import IndicatorLight
from scheduler import Scheduler
from machine import Timer



bootChrono = Timer.Chrono()
bootChrono.start()
bootLight = IndicatorLight(IndicatorLight.BLUE, 0.3, 0.2)


while(bootChrono.read() < 2):
    bootLight.pulse()
    print("Booting")

bootChrono.stop()



Scheduler()
Scheduler.waitForDetonation()
Scheduler.runBurst()
#Scheduler.runBurstTest()
