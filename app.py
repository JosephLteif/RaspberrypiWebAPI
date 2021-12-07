from flask import Flask, request

from helper.sensorHelper import SensorHelper
from client import Client
# import RPi.GPIO as GPIO

jsonHelper = SensorHelper()

client = Client(jsonHelper.device)
# to start listening do:
# client.connect()
#to stop it send from the laravel server "stop"

app = Flask(__name__)
# GPIO.setmode(GPIO.BOARD)

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
    sensor,pin=jsonHelper.request_to_sensor(request)
    jsonHelper.addSensor(sensor,pin)
    return ('', 204)

@app.route('/sensors/<pin>', methods=['Put'])
def updateSensor(pin):
    sensor,pin2=jsonHelper.request_to_sensor(request)
    jsonHelper.editSensor(sensor,pin)
    return jsonHelper.getSensor(pin)

@app.route('/sensors/<pin>', methods=['Delete'])
def deleteSensor(pin):
    jsonHelper.removeSensor(pin)
    return ('', 204)


@app.route('/<pin>/HIGH')
def HIGH(pin):
    outputpin(pin)
    GPIO.output(int(pin), GPIO.HIGH)
    return "Hello From HIGH!" 

@app.route('/<pin>/LOW')
def LOW(pin):  
    outputpin(pin)
    GPIO.output(int(pin), GPIO.LOW)
    return "Hello From LOW!" 


@app.route('/aa', methods=['GET'])
def getSensor2(pin):
    client.connect()
    return ('', 204)

# @app.route('/<pin>')
# def readSensor(pin):  
#     inputpin(pin)
#     GPIO.output(int(pin), GPIO.LOW)
#     return "Hello From LOW!" 

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")