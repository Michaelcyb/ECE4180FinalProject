import RPi.GPIO as GPIO
import time

class Measure:
    """
    Class to handle distance measurements using the HC-SR04 Ultrasonic Sensor.

    Attributes:
        GPIO_TRIG (int): GPIO pin connected to the TRIG pin of the sensor.
        GPIO_ECHO (int): GPIO pin connected to the ECHO pin of the sensor.

    Methods:
        get_distance(): Returns the distance measured by the sensor.
    """

    def __init__(self, GPIO_TRIG, GPIO_ECHO):
        self.GPIO_TRIG = GPIO_TRIG
        self.GPIO_ECHO = GPIO_ECHO

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # Set GPIO pins as IN/OUT
        GPIO.setup(GPIO_TRIG, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)

    def get_distance(self):
        """
        Measures and returns the distance detected by the sensor.
        """

        # Send a 10us pulse to the TRIG pin
        GPIO.output(self.GPIO_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIG, False)

        # Time when the pulse is sent
        while GPIO.input(self.GPIO_ECHO) == 0:
            start_time = time.time()

        # Time when the pulse is returned
        while GPIO.input(self.GPIO_ECHO) == 1:
            end_time = time.time()

        # Calculate the distance: distance = (travel time of sound wave * speed of sound) / 2
        time_elapsed = end_time - start_time
        distance = (time_elapsed * 34300) / 2

        return round(distance, 2)

GPIO.setwarnings(False)
