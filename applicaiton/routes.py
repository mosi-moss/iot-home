from flask import render_template, Response, jsonify
from applicaiton import app
from applicaiton.camera import Camera
from applicaiton.sensor import Sensor


@app.route("/")
@app.route("/home")
def home():
    """
    The home route. 

    Response:
        render_template: `home.html`
    """
    temp, humi = Sensor.get_reading()
    return render_template("home.html", temperature=temp, humidity=humi, text=f"PiCamera at {Camera().RESOLUTION[0]}:{Camera().RESOLUTION[1]} / {Camera().FRAMERATE} FPS")


@app.route("/camera_feed")
def camera_feed():
    """
    A route to access the camera feed.

    Response:
        bytes: a multipart byte response for camera frames.
    """
    return Response(Camera.gen_frame(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/climate")
def climate():
    """
    A route to access climate data.

    Response:
        JSON: temperature and humiditiy data.
    """
    temp, humi = Sensor.get_reading()
    return jsonify(temperature=temp, humidity=humi)
