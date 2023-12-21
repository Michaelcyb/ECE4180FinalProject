import RPi.GPIO as GPIO
from MotorControl import Motor
from Distance import Measure

class Car:
    """
    Class to control a car using Raspberry Pi.

    Attributes:
        motor_left (Motor): The left motor of the car.
        motor_right (Motor): The right motor of the car.
        motor_speed (int): The current speed of the car.
        measure (Measure): The distance measuring object.

    Methods:
        set_speed(speed): Sets the speed of the car.
        forward(): Moves the car forward.
        backward(): Moves the car backward.
        turn_left(): Turns the car left.
        turn_right(): Turns the car right.
        stop(): Stops the car.
        get_distance(): Returns the measured distance.
        get_speed(): Returns the current speed of the car.
        cleanup(): Cleans up GPIO settings.
    """

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Motor Pins
        GPIO_STBY = 27
        GPIO.setup(GPIO_STBY, GPIO.OUT)
        Motor.standby(GPIO_STBY, True)

        # Initialize Motors
        self.motor_left = Motor(18, 14, 15)
        self.motor_right = Motor(19, 23, 24)

        # Speed settings
        self.motor_speed = 50

        # HC-SR04 Sonar Module
        self.measure = Measure(5, 6)

    def set_speed(self, speed):
        """Set the speed of the car."""
        speed = max(0, min(100, speed))  # Clamp speed to [0, 100]
        self.motor_speed = speed
        self.motor_left.run(speed)
        self.motor_right.run(speed)

    def forward(self):
        """Move the car forward."""
        self.motor_left.run(self.motor_speed)
        self.motor_right.run(self.motor_speed)

    def backward(self):
        """Move the car backward."""
        self.motor_left.run(-self.motor_speed)
        self.motor_right.run(-self.motor_speed)

    def turn_left(self):
        """Turn the car left."""
        self.motor_left.run(-self.motor_speed)
        self.motor_right.run(self.motor_speed)

    def turn_right(self):
        """Turn the car right."""
        self.motor_left.run(self.motor_speed)
        self.motor_right.run(-self.motor_speed)

    def stop(self):
        """Stop the car."""
        self.motor_left.stop()
        self.motor_right.stop()

    def get_distance(self):
        """Get the distance measured by the sonar."""
        return self.measure.get_distance()

    def get_speed(self):
        """Get the current speed of the car."""
        return self.motor_speed

    def cleanup(self):
        """Clean up GPIO settings."""
        self.motor_left.cleanup()
        self.motor_right.cleanup()
        GPIO.cleanup()


GPIO.setwarnings(False)
