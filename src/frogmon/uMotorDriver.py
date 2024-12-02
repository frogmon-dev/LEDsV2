import RPi.GPIO as GPIO

class MOTORDRIVER():   
    def __init__(self, dirPin, brakePin):
        self.IN1_PIN = dirPin  # Direction pin
        self.IN2_PIN = brakePin  # Brake pin
        GPIO.setmode(GPIO.BCM)  # Set the GPIO mode
        GPIO.setup(self.IN1_PIN, GPIO.OUT)  # Setup Direction pin
        GPIO.setup(self.IN2_PIN, GPIO.OUT)  # Setup Brake pin

    def onForward(self):
        GPIO.output(self.IN1_PIN, GPIO.HIGH)
        GPIO.output(self.IN2_PIN, GPIO.LOW)
        print('Forward!')

    def onBackward(self):
        GPIO.output(self.IN1_PIN, GPIO.LOW)
        GPIO.output(self.IN2_PIN, GPIO.HIGH)
        print('Backward')

    def onStop(self):
        GPIO.output(self.IN1_PIN, GPIO.LOW)
        GPIO.output(self.IN2_PIN, GPIO.LOW)
        print('Stop')

    def cleanup(self):
        GPIO.cleanup()  # Cleanup the GPIO pins when done