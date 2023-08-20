import time
import board
import adafruit_dht
from threading import Thread
from rpi_lcd import LCD


class Sensor():
    thread = None
    dht = adafruit_dht.DHT11(board.D17)

    @classmethod
    def get_reading(self):
        temp = None
        humi = None

        while (temp == None or humi == None):
            try:
                # Print the values to the serial port
                temp = self.dht.temperature
                humi = self.dht.humidity

            except RuntimeError:
                # print(error)
                temp = None
                humi = None
                time.sleep(2.0)

        return (temp, humi)

    @classmethod
    def gen_reading(self):
        while True:
            yield self.get_reading()

    @classmethod
    def display_thread(self):
        while True:
            temp, humi = self.get_reading()
            display.set_text("Temp: {} C".format(temp), 1)
            display.set_text("Humi: {}%".format(humi), 2)
            time.sleep(1)

    @classmethod
    def start_thread(self):
        self.thread = Thread(target=self.display_thread)
        self.thread.start()


class display():

    lcd = LCD()

    @classmethod
    def set_text(self, text, line):
        self.lcd.text(text, line)
