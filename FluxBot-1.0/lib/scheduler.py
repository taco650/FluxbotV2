import time
from machine import WDT
from indicatorLight import IndicatorLight 
from actuator import Actuator



class Scheduler:
    running = True


    def __init__(self):
        Actuator()



        Scheduler.running = True
        Scheduler.time = time.time()
        Scheduler.wdt = WDT(timeout=7000)
        Scheduler.light = IndicatorLight(0xFFFF00, 2, 1)
    
    
        #TODO: find pin number
        #Scheduler.actuator = Actuator(2000, )
    
    def init(self):
        Scheduler.light.beating(False)
        

    #Once ran, continuously runs until running is False 
    @staticmethod  
    def run():
        while Scheduler.running:
            Scheduler.update()
            Actuator.setPosition(0.5)
            time.sleep(5)
            Actuator.setPosition(1)
            time.sleep(5)


    #Houskeeping functions
    @staticmethod
    def update():
        Scheduler.wdt.feed()
        Scheduler.light.pulse()