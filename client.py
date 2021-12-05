import time
import pusher
import random

class Client():
    def __init__(self, device_info):
        self.pusher_client = pusher.Pusher(
        app_id='1312016',
        key='b31701c0130090517616',
        secret='3f50d1ad4816c8e6389d',
        cluster='eu',
        ssl=True
        )
        self.name =  device_info["name"]
        self.delay = 0.1

    def connect(self):
        for i in range(30):
            self.pusher_client.trigger('my-channel', 'my-event', {'message': str(random.randint(1,30))})
            time.sleep(0.5)