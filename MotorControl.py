import RPi.GPIO as GPIO

class Motor:
    """
    Class to control a motor using the TB6612FNG driver.

    Attributes:
        GPIO_PWM (int): GPIO pin for PWM control.
        GPIO_IN1 (int): GPIO pin for motor direction control.
        GPIO_IN2 (int): GPIO pin for motor direction control.
        freq (int): Frequency for PWM signal.

    Methods:
        standby(GPIO_STBY, status): Static method to control the standby status of the driver.
        run(speed): Controls the motor speed and direction.
        stop(): Stops the motor.
        cleanup(): Stops the motor and cleans up GPIO settings.
    """

    def __init__(self, GPIO_PWM, GPIO_IN1, GPIO_IN2, freq=300):
        self.GPIO_PWM = GPIO_PWM
        self.GPIO_IN1 = GPIO_IN1
        self.GPIO_IN2 = GPIO_IN2
        self.freq = freq

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PWM, GPIO.OUT)
        GPIO.setup(self.GPIO_IN1, GPIO.OUT)
        GPIO.setup(self.GPIO_IN2, GPIO.OUT)

        self.pwm = GPIO.PWM(self.GPIO_PWM, self.freq)
        self.last_pwm = 0
        self.pwm.start(self.last_pwm)

    @staticmethod
    def standby(GPIO_STBY, status=False):
        """
        Controls the standby status of the TB6612FNG driver.
        Args:
            GPIO_STBY (int): GPIO pin for standby control.
            status (bool): True activates the driver, False sets it to standby.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_STBY, GPIO.OUT)
        GPIO.output(GPIO_STBY, status)

    def __setPWM(self, dc):
        """
        Sets the PWM duty cycle.
        Args:
            dc (int): Duty cycle value between 0 and 100.
        """
        if dc != self.last_pwm:
            self.pwm.ChangeDutyCycle(dc)
            self.last_pwm = dc

    def run(self, speed):
        """
        Runs the motor at a specified speed.
        Args:
            speed (int): Speed value between -100 and 100. Positive for forward, negative for reverse.
        """
        if speed >= 0:
            GPIO.output(self.GPIO_IN1, False)
            GPIO.output(self.GPIO_IN2, True)
        else:
            GPIO.output(self.GPIO_IN1, True)
            GPIO.output(self.GPIO_IN2, False)

        self.__setPWM(abs(speed))

    def stop(self):
        """Stops the motor."""
        GPIO.output(self.GPIO_IN1, False)
        GPIO.output(self.GPIO_IN2, False)
        self.__setPWM(0)

    def cleanup(self):
        """Stops the motor and cleans up the GPIO settings."""
        self.stop()
        self.pwm.stop()

GPIO.setwarnings(False)
