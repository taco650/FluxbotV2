import time
import pycom


class IndicatorLight:
    'Used to change the color of the lopy light'
    
    heartbeat = True
    

    def __init__(self, color, delay, duration):
        self.rgb = color
        self.delay = delay
        self.pulseDuration = duration
        self.delay = 0 #in s
        self.pulseDuration = 0
        self.lastPulse = 0

        
    def setLightColor(self, color):
        self.rgb = color

    #Set delay to 0 to have a solid light
    def setDelay(self, seconds):
        self.delay = seconds
    
    def setPulseDuration(self, seconds):
        self.pulseDuration = seconds
    
    def stop(self):
        self.pulseDuration = 0

    def pulse(self):
        if  not IndicatorLight.heartbeat and time.time() > self.lastPulse + self.delay:
            pycom.rgbled(rgb)
            if(time.time() > self.lastPulse + self.delay + self.pulseDuration):
                self.lastPulse = time.time()
                pycom.rgbled(0x0)
        
    def beating(self, beating):
        pycom.heartbeat(beating)
