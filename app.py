from flask import Flask, request
from flask_ngrok import run_with_ngrok
from helper.sensorHelper import SensorHelper
from client import Client
import random
import threading
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)


def get_value_from_sensor(pin):
    inputpin(pin)
    result = str(GPIO.input(int(pin)))
    outputpin(pin)
    if result == '1':
        GPIO.output(int(pin), GPIO.HIGH)
    else:
        GPIO.output(int(pin), GPIO.LOW)
    return result
    
    return random.randint(0,50)


jsonHelper = SensorHelper()

client = Client(jsonHelper.device, jsonHelper.sensors, get_value_from_sensor)
# client.invoke_state()
# to start listening do:
# client.connect()
# to stop it send from the laravel server "stop"

app = Flask(__name__)


def outputpin(pinNum):
    GPIO.setup(int(pinNum), GPIO.OUT)


def inputpin(pinNum):
    GPIO.setup(int(pinNum), GPIO.IN)


@app.route('/')
def index():
    return "Hello world!"


@app.route('/device', methods=['GET'])
def getDevices():
    return jsonHelper.getDevice()


@app.route('/sensors', methods=['GET'])
def getSensors():
    return jsonHelper.getSensors()


@app.route('/sensors/<pin>', methods=['GET'])
def getSensor(pin):
    return jsonHelper.getSensor(pin)


@app.route('/sensors', methods=['Post'])
def addSensor():
    sensor, pin = jsonHelper.request_to_sensor(request)
    jsonHelper.addSensor(sensor, pin)
    return ('', 204)


@app.route('/sensors/<pin>', methods=['Put'])
def updateSensor(pin):
    sensor, pin2 = jsonHelper.request_to_sensor(request)
    jsonHelper.editSensor(sensor, pin)
    return jsonHelper.getSensor(pin)


@app.route('/sensors/<pin>', methods=['Delete'])
def deleteSensor(pin):
    jsonHelper.removeSensor(pin)
    return ('', 204)


@app.route('/ChangeState', methods=['Post'])
def status():
    print('in status')
    pin = request.form.get("pin")
    print('starting in')
    status = request.form.get("status")
    print(status)
    if(status == "OFF"):
        outputpin(pin)
        GPIO.output(int(pin), GPIO.HIGH)
        jsonHelper.changeSensorStatus(int(pin), "ON", 1)

    else:
        outputpin(pin)
        GPIO.output(int(pin), GPIO.LOW)
        jsonHelper.changeSensorStatus(int(pin), "OFF", 0)

    return ('', 204)


@app.route('/<pin>/<channel>')
def getValueOfSensor(pin, channel):
    threading.Thread(target=client.start_connection_v2).start()
    # client.start_connection_v2()
    # if(channel == "SensorsValueChannel"):
    #     client.start_main_connection()
    # else:
    #     client.start_connection(channel, pin)
    return ('', 204)


# @app.route('/aa', methods=['GET'])
# def getSensor2(pin):
#     client.connect()
#     return ('', 204)
# @app.route('/<pin>')
# def readSensor(pin):
#     inputpin(pin)
#     GPIO.output(int(pin), GPIO.LOW)
#     return "Hello From LOW!"
# run_with_ngrok(app)
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
    # app.run()
