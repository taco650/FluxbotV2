#Pin that actuator signal uses
ACTUATOR_PIN = 'P19'
#Sec required to fully extend actuator
ACTUATION_TIME = 13
#Position of the actuator when it is fully retracted
ACTUATION_RETRACTION_POSITION = 0
#Position of the actuator when it is fully extended
ACTUATION_EXTENSION_POSITION = 0.9
#Name that is put on the CSV
DEVICE_NAME = "Test"
#ms unresponsive until device resets
WATCHDOG_TIMEOUT = 7*1000
#Time in seconds for each measurement cycle (Start every 58 mins)
CYCLE_PERIOD = 1*60*55
#Time for cycle (seconds for measurement process with cloesd lid)(2 min)
CYCLE_LENGTH = 1*60
#Measurement freq in closed box (Hz)
MEASUREMENT_CLOSED_BOX_FRQ = 1
#Measurement freq w/ open box
MEASUREMENT_OPEN_BOX_FRQ = 21
#Time between open bursts in secs
BURST_PERIOD = 18*60
#Num of Points in Open Box Burst
OPEN_BURST_POINTS = 3
#Delay (ms) Between open box burst points
OPEN_BURST_DELAY = 1000

CLOSED_BURST_POINTS = 60*5
#Delay (ms) Between open box burst points
#twofreshmeasurementspersecond
CLOSED_BURST_DELAY = 1000

BURST_DELAY_AFTER_OPEN = 18 * 60
