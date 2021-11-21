import json

class SensorHelper():
    def __init__(self):
        self.file_name = "sensors.json"
        self.sensors = self.loadSensors()

    def addSensor(self, sensor):
        self.sensors.add(sensor)
        json_object = json.dumps(sensor, indent = 1)
        with open(self.file_name, "a") as outfile:
            outfile.write(json_object)

    def removeSensor(self, sensor):
        self.sensors.remove(sensor)
        json_object = json.dumps(self.sensor, indent = 1)
        with open(self.file_name, "w") as outfile:
            outfile.write(json_object)

    def editSensor(self, sensor):
        self.sensors[sensor.key] = sensor
        json_object = json.dumps(self.sensor, indent = 1)
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

