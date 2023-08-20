import io
import time
from threading import Condition, Thread
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class CameraOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class Camera():
    RESOLUTION = (1640, 1232)
    FRAMERATE = 41
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(
        main={"size": (RESOLUTION[0], RESOLUTION[1])},
        controls={"FrameDurationLimits": (
            FRAMERATE * 1000, FRAMERATE * 1000)}
    ))
    output = CameraOutput()
    last_access = 0
    recording = False
    thread = None

    @classmethod
    def start(self):
        self.picam2.start_recording(JpegEncoder(), FileOutput(self.output))
        print("Camera starting")
        self.recording = True

    @classmethod
    def controller_thread(self):
        self.start()
        while True:
            if time.time() - self.last_access > 15:
                break
        self.stop()

    @classmethod
    def start(self):
        self.picam2.start_recording(JpegEncoder(), FileOutput(self.output))
        print("Camera starting")
        self.recording = True

    @classmethod
    def stop(self):
        self.picam2.stop_recording()
        print("Camera stopping")
        self.recording = False

    @classmethod
    def get_frame(self):
        self.last_access = time.time()

        if not self.recording:
            self.thread = Thread(target=self.controller_thread())

        with self.output.condition:
            self.output.condition.wait()
            frame = self.output.frame

        return frame

    @classmethod
    def gen_frame(self):
        while True:
            frame = self.get_frame()
            yield b"--frame\r\n"
            yield b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
