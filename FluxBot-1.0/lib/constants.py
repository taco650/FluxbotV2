#Pin that actuator signal uses
ACTUATOR_PIN = 'P19'
#Sec required to fully extend actuator
ACTUATION_TIME = 6
#Position of the actuator when it is fully retracted
ACTUATION_RETRACTION_POSITION = 0
#Position of the actuator when it is fully extended
ACTUATION_EXTENSION_POSITION = 1
#Name that is put on the CSV
DEVICE_NAME = "Test"
#Seconds unresponsive until device resets
WATCHDOG_TIMEOUT = 7
#Time in seconds for each measurement cycle
CYCLE_PERIOD = 12
#Time for cycle (seconds for measurement process with cloesd lid)
CYCLE_LENGTH = 30
#Measurement freq in closed box (Hz)
MEASUREMENT_CLOSED_BOX_FRQ = 50
#Measurement freq w/ open box
MEASUREMENT_OPEN_BOX_FRQ = 21