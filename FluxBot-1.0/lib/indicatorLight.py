import pycom
from machine import Timer


class IndicatorLight:
    'Used to change the color of the lopy light'

    heartbeat = True
    BLUE =   0x0000ff
    RED =    0xff0000
    GREEN =  0x00ff00
    PURPLE = 0xff00ff
    YELLOW = 0xffff00
    ORANGE = 0xFF4500
    CYAN = 0x42f4ee
    WHITE = 0xFFFFFF


    def __init__(self, colors, delay, duration):
        pycom.heartbeat(False)
        self.rgb = []
        self.rgb.extend(colors)
        self.currentIndex = 0
        self.delay = delay #in s
        self.pulseDuration = duration
        self.chrono = Timer.Chrono()
        self.chrono.start()
        self.lastPulse = self.chrono.read()
        self.isChanging = False


    def setLightColor(self,colors = []):
        self.rgb = colors

    #Set delay to 0 to have a solid light
    def setDelay(self, seconds):
        self.delay = seconds


    def setPulseDuration(self,seconds):
        self.pulseDuration = seconds

    def stop(self):
        self.pulseDuration = 0

    def on(self):
        pycom.rgbled(self.rgb)
    def off(self):
        pycom.rgbled(0x0)

    def endPulse(self):
        if not self.isChanging and self.lastPulse + self.pulseDuration <= self.chrono.read():
            self.currentIndex = 0
            pycom.rgbled(0x0)
            self.isChanging = True

    def pulse(self):

        #Index changing and timing logic
        if not self.isChanging and self.lastPulse + self.pulseDuration <= self.chrono.read():
            self.currentIndex += 1
            self.isChanging = True

        #Color changing logic
        if self.currentIndex < len(self.rgb):
            if self.isChanging:
                pycom.rgbled(self.rgb[self.currentIndex])
                self.lastPulse = self.chrono.read()
                self.isChanging = False
        else:
            pycom.rgbled(0x0)
            if self.lastPulse + self.delay + self.pulseDuration <= self.chrono.read():
                self.isChanging = False
                self.currentIndex = -1
                self.lastPulse = self.chrono.read()



        '''
        if self.currentIndex != -1 and self.lastPulse + self.duration <= self.chrono.read():
            pycom.rgbled(self.rgb[self.currentIndex])#iterate  each time
            self.currentIndex += 1
            self.lastPulse = self.chrono.read()
            if self.currentIndex > len(self.rgb) - 1:
                self.currentIndex = -1
        elif self.currentIndex == -1 and self.lastPulse + self.delay + self. <= self.chrono.read():
            self.currentIndex = 0


            else:
                #next color is blank
                if self.isOn and self.lastPulse + self.delay +  self.pulseDuration <= self.chrono.read():
                    self.currentIndex = 0
                    self.lastPulse = self.chrono.read()
                    self.isOn = False
                    pycom.rgbled(0x0)



        if len(self.rgb) > self.currentIndex + 1:
            self.currentIndex += 1
            self.lastPulse = self.chrono.read()

        '''


    @staticmethod
    def beating(beating):
        pycom.heartbeat(beating)
