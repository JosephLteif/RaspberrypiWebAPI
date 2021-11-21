from flask import Flask
import RPi.GPIO as GPIO


app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)

def outputpin(pinNum):
    GPIO.setup(int(pinNum), GPIO.OUT)

def inputpin(pinNum):
    GPIO.setup(int(pinNum), GPIO.IN)

@app.route('/')
def index():
    return "Hello world!" 

@app.route('/<id>')
def test(id):
    return id

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