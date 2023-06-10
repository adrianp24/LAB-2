import time
from Model import Model, TIMEOUT, BTN1_PRESS
from Button import Button
from CompositeLights import TrafficLight, GreenLight, YellowLight, RedLight
from Displays import LCDDisplay
from Buzzer import ActiveBuzzer
from MotionSensor import MotionSensor

class TrafficLightController:
    def __init__(self):
        # Instantiate
        self.firstLight = TrafficLight(GreenLight(16), YellowLight(18), RedLight(19))
        self.secondLight = TrafficLight(GreenLight(11), YellowLight(12), RedLight(13))
        
        # Instantiate the pedestrian button and set the handler to self
        self.button = Button(4, "PEDESTRIAN CLICKED", buttonhandler=self)
        
        # Instantiate the LCD display
        self.mainDisplay = LCDDisplay(sda=0, scl=1, i2cid=0)
        
        # Instantiate the model with 5 states and set self as the handler
        self.stateModel = Model(5, self, debug=True)

        self.activeBuzzer = ActiveBuzzer(15)

        self.motionSensor = MotionSensor(28)
        
        # Add the button to the model
        self.stateModel.addButton(self.button)
        
        # Define the transitions between states

        self.stateModel.addTransition(0, TIMEOUT, 1)
        self.stateModel.addTransition(1, TIMEOUT, 2)
        self.stateModel.addTransition(2, TIMEOUT, 3)
        self.stateModel.addTransition(3, TIMEOUT, 0)
        self.stateModel.addTransition(4, TIMEOUT, 0)

        self.stateModel.addTransition(0, BTN1_PRESS, 4)
        self.stateModel.addTransition(1, BTN1_PRESS, 4)
        self.stateModel.addTransition(2, BTN1_PRESS, 4)
        self.stateModel.addTransition(3, BTN1_PRESS, 4)


    
    def run(self):
        # Run the model
        self.stateModel.run()
    
    def stateDo(self, state):
        if state in [0, 1, 2, 3]:
            # Check if motion is detected
            if self.motionSensor.motionDetected():
                self.stateModel.gotoState(4)

    def stateEntered(self, state):
        # Perform actions when entering a state
        if state == 0:
            # Start the main light on green
            self.mainDisplay.reset()
            self.firstLight.onlyGreenOn()
            self.secondLight.onlyRedOff()
            self.mainDisplay.showCounterText("STOP WALKING")
            time.sleep(4)
            self.timeout()  # Call the timeout method after 5 seconds
        elif state == 1:
            # Start the main light on yellow
            self.firstLight.onlyYellowOn()
            self.secondLight.onlyRedOff()
            self.mainDisplay.showCounterText("STOP WALKING")
            time.sleep(3)
            self.timeout()  # Call the timeout method after 2 seconds
        elif state == 2:
            # Green
            self.mainDisplay.reset()
            self.firstLight.onlyRedOn()
            self.secondLight.onlyGreenOn()
            self.mainDisplay.showCounterText("STOP WALKING")
            time.sleep(4)
            self.timeout()  # Call the timeout method after 5 seconds
        elif state == 3:
            # yellow
            self.mainDisplay.reset()
            self.firstLight.onlyRedOff()
            self.secondLight.onlyYellowOn()
            self.mainDisplay.showCounterText("STOP WALKING")
            time.sleep(4)
            self.timeout()  # Call the timeout method after 2 seconds
        elif state == 4:
            # walk
            self.activeBuzzer.play()
            self.activeBuzzer.stop()
            self.mainDisplay.reset()
            self.firstLight.onlyRedOff()
            self.secondLight.onlyRedOff()
            
            countdown = 10  
            while countdown >= 0:
                self.mainDisplay.showCounterText("Walk: {:02d}".format(countdown))
                time.sleep(1)
                countdown -= 1

            self.timeout()  
    
    
    def stateLeft(self, state):
        # Perform actions when leaving a state
        pass
    
    def buttonPressed(self, name):
        # Handle the button press event
        if self.stateModel.getState() != 4:
            # Transition to state 4 on button press
            self.stateModel.gotoState(4)
    
    def buttonReleased(self, name):
        # Handle the button release event
        pass
    
    def timeout(self):
        self.stateModel.processEvent(TIMEOUT)

if __name__ == '__main__':
    # Create an instance of the TrafficLightController and run it
    TrafficLightController().run()
