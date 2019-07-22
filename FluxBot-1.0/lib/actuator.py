from machine import PWM
import constants as CONSTANTS
import time

class Actuator:
    #Used to control the actuator for opening and closing the lid.

    '''
    the pulse width range they expect is pretty small,
    from 1 ms to 2ms, at a 20ms period, resulting at a
    PWM duty cycle range between 5% and 10%
    '''

    position = CONSTANTS.ACTUATION_EXTENSION_POSITION

    #default state should be closed
    def __init__(self, acuationTime = CONSTANTS.ACTUATION_TIME):
        print("Initializing Actuator")
        Actuator.pwm = PWM(0, frequency = 50)
        Actuator.pwm_pin = Actuator.pwm.channel(0, pin = CONSTANTS.ACTUATOR_PIN, duty_cycle = 0.0)
        Actuator.timeOfOpening = 0
        Actuator.acuationTime = acuationTime

    @staticmethod
    def setPosition(newPosition):
        if not Actuator.position == newPosition:
            Actuator.position = newPosition
            Actuator.update()

    @staticmethod
    def actuatorPosition():
        return Actuator.position

    @staticmethod
    def update():
        Actuator.timeOfOpening = time.time()
        position = Actuator.position
        dutyCycle = Actuator.positionToDuty(position)
        Actuator.pwm_pin = Actuator.pwm.channel(0, pin = CONSTANTS.ACTUATOR_PIN, duty_cycle = 0.05*(position-1)+0.1)

    @staticmethod
    def positionToDuty(position):
        #position is given as a percentage
        #position 1 means fully extended
        #position 0 means fully retracted
        dutyCycle = 0.05*(position - 1) + 0.1
        if dutyCycle < 0:
            return 0.05
        elif dutyCycle > 0.1:
            return 0.1
        else:
            return dutyCycle
