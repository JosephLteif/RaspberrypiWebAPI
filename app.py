from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
@app.route('/')
def index():
    return "Hello world!" 


@app.route('/HIGH')
def HIGH():
    GPIO.output(15, GPIO.HIGH)
    return "Hello From HIGH!" 

@app.route('/LOW')
def LOW():  
    GPIO.output(15, GPIO.LOW)
    return "Hello From LOW!" 

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")