import time
import pusher
import random
import threading

class Client():
    def __init__(self, device_info,sensor_info, func):
        self.pusher_client = pusher.Pusher(
        app_id='1312016',
        key='b31701c0130090517616',
        secret='3f50d1ad4816c8e6389d',
        cluster='eu',
        ssl=True
        )
        self.sensor_info = sensor_info
        self.func = func
        self.name = device_info["name"]
        self.delay = 0.1
        self.main_channel_name = "SensorsValueChannel"
        
    # def state(self, channels):
    #     while(True):
    #         for channel in channels:
    #             if(self.pusher_client.channel_info(channels[channel])["occupied"]):
    #                 threading.Thread(target=self.connect, args=(channels[channel],)).start()

    #         time.sleep(5)

    # def invoke_state(self):
    #     x = threading.Thread(target=self.state)
    #     x.start()

    def start_connection(self,channel_name,pin):
        threading.Thread(target=self.connect, args=(channel_name,pin)).start()

    def connect(self,channel_name,pin):
        time.sleep(2)
        while(self.pusher_client.channel_info(channel_name)["occupied"]):
            print("sending values")
            self.pusher_client.trigger(channel_name, 'my-event', {'message': str(self.func(pin))})
            # self.pusher_client.trigger(channel_name, channel_name, {'message': str(pin)})
            time.sleep(0.3)

    def start_main_connection(self):
        threading.Thread(target=self.main_connection).start()

    def main_connection(self):
        time.sleep(2)
        while(self.pusher_client.channel_info(self.main_channel_name)["occupied"]):
            print("sending to main")
            dict_request = {}
            for sensor in self.sensor_info:
                # dict_request[str(sensor)+"_value"] =str(self.func(sensor))
                if(self.func(sensor) == 0):
                    dict_request[str(sensor)+"_status"] = "OFF"
                    dict_request[str(sensor)+"_value"] ="---"
                else:
                    dict_request[str(sensor)+"_status"] = "ON"
                    dict_request[str(sensor)+"_value"] =str(self.func(sensor))
                    
            self.pusher_client.trigger(self.main_channel_name, 'my-event', dict_request)
            time.sleep(5)

