from bottle import get, post, run, request, template
from CarControl import Car
import RPi.GPIO as GPIO

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
