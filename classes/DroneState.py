import sys, pygame, threading
import cv2
import numpy as np


class States:
        WAITING = 0
        USER_CONTROL = 1
        USER_CONTROL_PLUS_TEST = 2
        AUTO_FACE_FOCUS = 3
        EXIT = 4


"""
Format:
State -> Transition : StateChange : lambda defining the transition
State -> Action : lambda defining the action

Planned States:
    different forms of SEARCHING and TRACKING
    selecting tracking bounding box and TRACKING
tracking modes:
"""
class StateMachine:
    def __init__(self):
        # drone should initially be waiting
        self.state_object = Waiting()
    
"""
base class for all other classes to inherit from
"""
class DroneState:
    def __init__(self):
        super().__init__()
        self.state_type = States.EXIT

    def action(self, drone, eventList):
        pass

    def change(self, state=States.EXIT):
        transition = self.state_transition[state]
        return transition()

    def clean(self, drone):
        pass

class Waiting(DroneState):
    def __init__(self):
        super().__init__() 
        self.state_type = States.WAITING
        self.state_transition : {
                States.USER_CONTROL : lambda : UserControl(),
                States.AUTO_FACE_FOCUS : lambda : AutoFaceFocus(),
                States.EXIT : lambda : Exit()
            }

    def action(self, drone, eventList):
        for event in pygame.event.get():
                drone.reset_speed()
                if event.type == pygame.QUIT:
                    return self.change(state=States.EXIT)

                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    # emergency landing
                    if event.key == pygame.K_ESCAPE:
                        return self.change(state=States.EXIT)
                    elif event.key == pygame.K_SPACE:
                        launch_thread = threading.Thread(target=lambda drone: drone.takeoff(), args=[drone])
                        launch_thread.start()
                        while launch_thread.is_alive():
                            data = drone.getData()
                            frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
                            frame = np.rot90(frame)
                            frame = np.flipud(frame)
                        launch_thread.join()
        data = drone.getData()
        frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = np.flipud(frame)

    def change(self, state=States.EXIT):
        transition = self.state_transition[state]
        return transition()

    def clean(self, drone):
        pass

class UserControl(DroneState):
    def __init__(self):
        super().__init__()
        self.state_type = States.USER_CONTROL
        self.state_transition : {
                States.USER_CONTROL_PLUS_TEST: lambda : UserControlPlusTest(),
                States.AUTO_FACE_FOCUS : lambda : AutoFaceFocus(),
                States.EXIT : lambda : Exit()
            }

    def action(self, drone, eventList):
        for event in pygame.event.get():
                drone.reset_speed()
                if event.type == pygame.QUIT:
                    return self.change(state=States.EXIT)

                if event.type == pygame.KEYDOWN:
                    # emergency landing
                    if event.key == pygame.K_ESCAPE:
                        return self.change(state=States.EXIT)
                    else:
                        drone.key_down(event.key)

                elif event.type == pygame.KEYUP:
                    # emergency landing
                    if event.key == pygame.K_ESCAPE:
                        return self.change(state=States.EXIT)
                    else:
                        drone.key_up(event.key)
        drone.moveDrone()
        data = drone.getData()
        frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = np.flipud(frame)

    def change(self, state=States.EXIT):
        transition = self.state_transition[state]
        return transition()

    def clean(self, drone):
        pass


class UserControlPlusTest(DroneState):
    def __init__(self):
        super().__init__()
        self.state_type = States.USER_CONTROL_PLUS_TEST
        self.state_transition : {
                States.AUTO_FACE_FOCUS : lambda : AutoFaceFocus(),
                States.USER_CONTROL : lambda : UserControl(),
                States.EXIT : lambda : Exit()
            }
        
    
    def action(self, drone, eventList):
        for event in pygame.event.get():
                drone.reset_speed()
                if event.type == pygame.QUIT:
                    return self.change(state=States.EXIT)

                if event.type == pygame.KEYDOWN:
                    # emergency landing
                    if event.key == pygame.K_ESCAPE:
                        return self.change(state=States.EXIT)
                    else:
                        drone.key_down(event.key)

                elif event.type == pygame.KEYUP:
                    # emergency landing
                    if event.key == pygame.K_ESCAPE:
                        return self.change(state=States.EXIT)
                    else:
                        drone.key_up(event.key)
        drone.moveDrone()
        data = drone.getData()
        frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = np.flipud(frame)

    def change(self, state=States.EXIT):
        transition = self.state_transition[state]
        return transition()

    def clean(self, drone):
        pass


class AutoFaceFocus(DroneState):
    def __init__(self):
        super().__init__()
        self.state_type = States.AUTO_FACE_FOCUS
        self.state_transition : {
                States.USER_CONTROL : lambda : UserControl(),
                States.USER_CONTROL_PLUS_TEST: lambda : UserControlPlusTest(),
                States.EXIT : lambda : Exit()
            }
    
    """
    Creates a face object to be tracked
    """
    def detecting_face(self, frame, classifier):
        I = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = classifier.detectMultiScale(I, 1.3, 5)
        # return the first face that occures else return failure
        scaling = 8
        for (x, y, w, h) in faces:
            return (True, Face( int(x + w//scaling), int(y + h//scaling), int(w - w//scaling), (h-h//scaling) ))
        return (False, None)

    def action(self, drone, eventList):
        pass

    def change(self, state=States.EXIT):
        transition = self.state_transition[state]
        return transition()

    def clean(self, drone):
        pass


class Exit(DroneState):
    def __init__(self):
        super().__init__()
        self.state_type = States.EXIT
        self.state_transition : {
                States.EXIT : lambda : Exit()
            }

    def action(self, drone, eventList):
        drone.turnOff()

    def change(self, state=States.EXIT):
        transition = self.state_transition[state]
        return transition()

    def clean(self, drone):
        pass