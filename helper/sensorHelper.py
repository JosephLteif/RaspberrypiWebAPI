import json
from os import name
from models.sensor import Sensor
class SensorHelper():
    def __init__(self):
        self.file_name = "sensors.json"
        self.sensors = self.loadSensors()

    def json_to_sensor(self, sensor_json, pin):
        return Sensor(
            name = sensor_json["name"],
            pin = pin,
            category = sensor_json["category"],
            value = sensor_json["value"],
            status = sensor_json["status"]
        )

    def request_to_sensor(self,request):
        return {
            "name" : request.form.get("name"),
            "category" : request.form.get("category"),
            "value" : request.form.get("value"),
            "status" : request.form.get("status")
        },request.form.get("pin")


    def addSensor(self, sensor, pin):
        print(sensor)
        self.sensors[pin] = sensor
        json_object = json.dumps(self.sensors, indent = 1)
        with open(self.file_name, "w") as outfile:
            outfile.write(json_object)

    def removeSensor(self, pin):
        del self.sensors[pin]
        json_object = json.dumps(self.sensors, indent = 1)
        with open(self.file_name, "w") as outfile:
            outfile.write(json_object)

    def editSensor(self, sensor, pin):
        self.sensors[pin] = sensor
        json_object = json.dumps(self.sensors, indent = 1)
        with open(self.file_name, "w") as outfile:
            outfile.write(json_object)

    def loadSensors(self):
        with open(self.file_name, 'r') as openfile:
            json_object = json.load(openfile)
        return json_object

    def getSensor(self, pin):
        return self.sensors[pin]

    def getSensors(self):
        return self.sensors
