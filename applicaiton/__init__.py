from flask import Flask
from applicaiton.camera import Camera
from applicaiton.sensor import Sensor

# initialise app
app = Flask(__name__)
app.debug = True

Camera.start()
Sensor.start_thread()

from applicaiton import routes