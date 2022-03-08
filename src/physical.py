import RPi.GPIO as GPIO
import time
import logger

def initServo(pin, debug=True):
    if debug:
        logger.log("GPIO mode set to BCM")
    GPIO.setmode(GPIO.BCM)
    if debug:
        logger.log("GPIO set to GPIO.OUT for pin "+str(pin))
    GPIO.setup(pin, GPIO.OUT)
    if debug:
        logger.log("Creating PWM object")
    return GPIO.PWM(pin, 100)

def cleanGPIO(debug=True):
    if debug:
        logger.log("Cleaning up GPIO exports")
    GPIO.cleanup()

def lock(servo, debug=True):
    if debug:
        logger.log("Unlocking door...")
        logger.log("Setting frequency to 100")
    servo.ChangeFrequency(100)
    if debug:
        logger.log("duty cycle=5")
    servo.start(5)
    time.sleep(1)
    if debug:
        logger.log("Turning servo off...")
    servo.stop()

def unlock(servo, debug=True):
    if debug:
        logger.log("Locking door...")
        logger.log("Setting frequency to 100")
    servo.ChangeFrequency(100)
    if debug:
        logger.log("duty cycle=25")
    servo.start(25)
    time.sleep(1)
    if debug:
        logger.log("Turning servo off")
    servo.stop()

def initReedSwitch(pin, debug=True):
    if debug:
        logger.log("Setting Reed Switch pin")
        logger.log("GPIO mode set to BCM")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def enableDoorEvent(pin, callbackFunction, debug=True):
    if debug:
        logger.log("Enabling GPIO reed switch event detection")

    GPIO.add_event_detect(pin, GPIO.RISING, callback=callbackFunction, bouncetime=1000)

def readDoorStatus(pin, debug=True):
    pinStatus=GPIO.input(pin)
    if pinStatus == 1:
        return True
    else:
        return False

def initDoorButton(pin, debug=True):
    if debug:
        logger.log("Setting door toggle button pin")
        logger.log("GPIO mode set to BCM")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def enableButtonEvent(pin, callbackFunction, debug=True):
    if debug:
        logger.log("Enabling GPIO door button event detection")

    GPIO.add_event_detect(pin, GPIO.RISING, callback=callbackFunction, bouncetime=300)
