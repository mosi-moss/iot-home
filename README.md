# IoT Application

A simple IoT application usising the Raspberry Pi 4B with a camera and temperature/humidity sensor.

## Hardware

 - Raspberry Pi Model 4B
 - PiCamera v2
 - Breadboard
 - GPIO Expansion Board
 - Wires
 - DHT11
 - 10K Ohm Resistor

A diagram of how I set up the hardware. Creating using Fritzing.

![SchematicLCD_bb](https://github.com/mosi-moss/iot-home/assets/57157475/5ab063b4-9320-4097-a7c6-55243a4cf9ca)

## Home Assistant

I created this with the intention of connecting to Home Assistant. I did this by adding the following to the `configuration.yaml`.

```yaml
# PiSensors
rest:
- scan_interval: 60
resource: http:/IPADDRESS:PORT/climate
sensor:
  - name: temperature
  value_template: "{{ value_json.temperature }}"
  unit_of_measurement: "°C"
  - name: humidity
  value_template: "{{ value_json.humidity }}"
  unit_of_measurement: "%"
```
