from Sensors import *

class MotionSensor(DigitalSensor):

    def __init__(self, pin):
        super().__init__(pin, lowactive=False)

    def motionDetected(self):
        return self.tripped()