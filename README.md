# ECE4180FinalProject
Georgia Tech Fall 2023 Final Project
# ECE4180 Final Project - Indoor Delivery Car

### Team Members: Xiuyuan Sun, Yubo Cheng

Watch our project demo on Youtube: [ECE 4180 Final Project Demo - YouTube](https://www.youtube.com/shorts/NgoWwHDYPSY)

## Project Idea

An indoor delivery car is designed for the situation where your roommates want something for you, but you are lazy to walk to their room by foot. It has several advantages including low cost, simple circuit structure and easy programming.

The central control unit is Raspberry Pi 3. Our deliver car is driven by two wheels, with each driven by a DC motor. It can change direction by modulating the speed of each wheel. There is a camera module on the car to provide vision. There is a sonar sensor in the front of the car where it can tell you the distance between the car and the obstacle in case of camera lagging. This car can be controlled by our keyboard or simply by clicking the button on the website that we created.

## Parts List

1. Raspberry Pi 3 Model B
2. Raspberry Pi NoIR Camera V2
3. HC-SR04 Sonar Module
4. Dual H-Bridge (TB6612FNG)
5. 2 Motors
6. 2 Wheels
7. Jump wires
8. Power Bank

## Wiring

| Raspberry Pi 3 | Dual H-Bridge | Motor         |
| -------------- | ------------- | ------------- |
| 3.3V           | Vm            |               |
| 5V             | VCC           |               |
| GPIO 18        | PWMA          |               |
| GPIO 14        | AIN1          |               |
| GPIO 15        | AIN2          |               |
| GPIO 19        | PWMB          |               |
| GPIO 23        | BIN1          |               |
| GPIO 24        | BIN2          |               |
| GND            | GND           |               |
|                | AO1           | Left Motor -  |
|                | AO2           | Left Motor +  |
|                | BO1           | Right Motor + |
|                | BO2           | Right Motor - |

| Raspberry Pi 3 | HC-SR04 Sonar Module |
| -------------- | -------------------- |
| 5V             | Vcc                  |
| GND            | Gnd                  |
| GPIO 5         | Trig                 |
| GPIO 6         | Echo                 |

## Pictures of Project

### Car from different angles

#### Top

![image](https://github.com/Michaelcyb/ECE4180FinalProject/blob/main/Pictures/Top.jpg)

#### Front

![<img src="E:\Georgia Tech\ECE 4180 Embedded Systems Design\Final Project\Front.jpg" alt="Front" style="zoom:10%;" />](https://github.com/Michaelcyb/ECE4180FinalProject/blob/main/Pictures/Front.jpg)

#### Back

![<img src="E:\Georgia Tech\ECE 4180 Embedded Systems Design\Final Project\Back.jpg" alt="Back" style="zoom:10%;" />](https://github.com/Michaelcyb/ECE4180FinalProject/blob/main/Pictures/Back.jpg)

#### Left

![<img src="E:\Georgia Tech\ECE 4180 Embedded Systems Design\Final Project\Left.jpg" alt="Left" style="zoom:10%;" />](https://github.com/Michaelcyb/ECE4180FinalProject/blob/main/Pictures/Left.jpg)

#### Right

![<img src="E:\Georgia Tech\ECE 4180 Embedded Systems Design\Final Project\Right.jpg" alt="Right" style="zoom:10%;" />
](https://github.com/Michaelcyb/ECE4180FinalProject/blob/main/Pictures/Right.jpg)
### Control and Information Page

![<img src="https://github.com/Michaelcyb/ECE4180FinalProject/blob/main/Pictures/ControlPage.png />](https://github.com/Michaelcyb/ECE4180FinalProject/blob/main/Pictures/ControlPage.png)

## Source Code

### CarControl.py

```python
from Distance import Measure
from MotorControl import Motor
import RPi.GPIO as GPIO

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
```

### Distance.py

```python
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
```

### MotorControl.py

```python
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
```

### info.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="1"> <!-- Refresh every second -->
    <title>Information</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }

        p {
            margin-left: 20px;
        }
    </style>
</head>
<body>
    <p>Speed: {{speed}}</p>
    <p>Distance: {{distance}} cm</p>
</body>
</html>
```

### index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raspberry Car Control Panel</title>
    <link href="http://cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js"></script>
    <style type="text/css">
        #front {
            margin-left: 55px;
            margin-bottom: 3px;
        }
        #rear {
            margin-top: 3px;
            margin-left: 55px;
        }
        .btn {
            background: #62559f;
        }
    </style>
</head>
<body>
    <div class="row">
        <div class="col-xs-12 col-sm-6 col-md-7">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Real-Time Display</h3>
                </div>
                <div class="panel-body">
                    <iframe src="http://172.20.10.3:8081/" width="820" height="620" frameborder="1" name="name" scrolling="auto"></iframe>
                </div>
            </div>                      
        </div>

        <div class="col-xs-6 col-md-4">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Car Information</h3>
                </div>
                <div class="panel-body">
                    <iframe id="car-info" width="320" height="195" src="http://172.20.10.3:8088/info"></iframe>
                </div>
            </div>

            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Control Panel</h3>
                </div>
                <div class="panel-body" style="margin: 10px;margin-left: 10px">
                    <!-- Control Buttons -->
                    <div class="row">
                        <div class="col-md-2"></div>
                        <div class="col-md-2">
                            <button id="forward" class="btn btn-large btn-primary" type="button">
                                <span class="glyphicon glyphicon-triangle-top" aria-hidden="true"></span><br/>Forward
                            </button>
                        </div>
                        <div class="col-md-2"></div>
                    </div>
                    <br/>
                    <div class="row">
                        <div class="col-md-2">
                            <button id="turnLeft" class="btn btn-large btn-primary" type="button">
                                <span class="glyphicon glyphicon-triangle-left" aria-hidden="true"></span><br/>Turn Left
                            </button>
                        </div>
                        <div class="col-md-2">
                            <button id="backward" class="btn btn-large btn-primary" type="button">
                                <span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span><br/>Backward
                            </button>
                        </div>
                        <div class="col-md-2">
                            <button id="turnRight" class="btn btn-large btn-primary" type="button">
                                <span class="glyphicon glyphicon-triangle-right" aria-hidden="true"></span><br/>Turn Right
                            </button>
                        </div>
                    </div>
                    <br/>
                </div>
            </div>
        </div>
    </div>

    <script>
        $(function() {
            // Button Mouse Events
            $("button").mousedown(function() {
                console.log(this.id + " mouse down");
                $.post("/cmd", this.id, function(data, status) {});
            });

            $("button").mouseup(function() {
                console.log(this.id + " mouse up");
                $.post("/cmd", "stop", function(data, status) {});
            });

            // Keyboard Controls
            $(document).keydown(function(event) {
                switch (event.keyCode) {
                    case 87: // W
                        console.log("press W");
                        $.post("/cmd", "forward", function(data, status) {});
                        break;
                    case 83: // S
                        console.log("press S");
                        $.post("/cmd", "backward", function(data, status) {});
                        break;
                    case 65: // A
                        console.log("press A");
                        $.post("/cmd", "turnLeft", function(data, status) {});
                        break;
                    case 68: // D
                        console.log("press D");
                        $.post("/cmd", "turnRight", function(data, status) {});
                        break;
                }
            });

            $(document).keyup(function(event) {
                switch (event.keyCode) {
                    case 87: // W
                    case 83: // S
                    case 65: // A
                    case 68: // D
                        console.log("key up");
                        $.post("/cmd", "stop", function(data, status) {});
                        break;
                }
            });
        });
    </script>
</body>
</html>
```
### Start.py

```python
from bottle import template, get, run, post, request
import RPi.GPIO as GPIO
from CarControl import Car

car = Car()

def handle_event(status):
    """
    Handles car control events based on the given status.
    Args:
        status (str): The command to control the car.
    """
    print(f"Event: {status}")
    if status == "forward":
        car.forward()
    elif status == "backward":
        car.backward()
    elif status == "turnLeft":
        car.turn_left()
    elif status == "turnRight":
        car.turn_right()
    elif status == "stop":
        car.stop()

@get("/")
def index():
    """
    Serves the index page.
    """
    print("Requesting index.html")
    return template("index.html")

@post("/cmd")
def cmd():
    """
    Handles POST requests to control the car.
    """
    command = request.body.read().decode()
    handle_event(command)
    return "OK"

@get("/info")
def info():
    """
    Serves the car information page.
    """
    print("Updating status information")
    return template("info.html", speed=car.get_speed(), distance=car.get_distance())

# Start the web server
try:
    run(host='172.20.10.3', port=8088, debug=False)
finally:
    car.cleanup()
    GPIO.setwarnings(False)

```

## Future Improvements

1. Be able to drive by itself to the destination

2. Be able to calculate the shorted path

3. Informs the person when it’s arrived

## Reference

> [Obstacles Avoiding Smart Car Using Arduino - Hackster.io](https://www.hackster.io/1NextPCB/obstacles-avoiding-smart-car-using-arduino-34e2bb)
