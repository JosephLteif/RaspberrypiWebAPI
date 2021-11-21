from flask import Flask

from helper.sensorHelper import SensorHelper
# import RPi.GPIO as GPIO

jsonHelper = SensorHelper()

app = Flask(__name__)
# GPIO.setmode(GPIO.BOARD)

def outputpin(pinNum):
    GPIO.setup(int(pinNum), GPIO.OUT)

def inputpin(pinNum):
    GPIO.setup(int(pinNum), GPIO.IN)

@app.route('/')
def index():
    return "Hello world!" 

@app.route('/sensor/<pin>')
def getSensor(pin):
    return jsonHelper.getSensor(pin)

@app.route('/sensors')
def getSensors():
    return jsonHelper.getSensors()


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

# @app.route('/<pin>')
# def readSensor(pin):  
#     inputpin(pin)
#     GPIO.output(int(pin), GPIO.LOW)
#     return "Hello From LOW!" 

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")