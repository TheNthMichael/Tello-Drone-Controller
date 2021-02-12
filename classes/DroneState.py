import sys, threading, pygame
sys.path.append('./classes')
import cv2
import numpy as np
import math
from TelloDrone import TelloDrone
from Controller import Controller
from Pid import Pid

"""
Class based state machine
"""
class States:
        WAITING = 0
        USER_CONTROL = 1
        USER_CONTROL_PLUS_TEST = 2
        AUTO_FACE_FOCUS = 3
        EXIT = 4

class StateMachine:
    def __init__(self):
        self.state = Waiting()

    def run(self, drone, screen, eventList):
        tmp_state = self.state.action(drone, screen, eventList)
        if tmp_state is not None:
            self.state.clean(drone)
            self.state = tmp_state

    def isNotExit(self):
        return (self.state.state_type != States.EXIT)
    
    def forceExit(self):
        self.state = Exit()
    
"""
base class for all other classes to inherit from
"""
class DroneState:
    def __init__(self):
        super().__init__()
        self.state_type = States.EXIT
        self.state_transition = {
                States.EXIT : lambda : Exit()
            }

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
        self.state_transition =  {
                States.USER_CONTROL : lambda : UserControl(),
                States.AUTO_FACE_FOCUS : lambda : AutoFaceFocus(),
                States.EXIT : lambda : Exit()
            }

    def action(self, drone, screen, eventList):
        drone.resetSpeed()
        for event in eventList:
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
                        frame = pygame.surfarray.make_surface(frame)
                        screen.blit(frame, (0, 0))
                        pygame.display.update()
                    launch_thread.join()
                    return self.change(state=States.USER_CONTROL)
        data = drone.getData()
        frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        pygame.display.update()
        return None

    def change(self, state=States.EXIT):
        return self.state_transition[state]()

    def clean(self, drone):
        drone.resetSpeed()

class UserControl(DroneState):
    def __init__(self):
        super().__init__()
        self.state_type = States.USER_CONTROL
        self.state_transition = {
                States.USER_CONTROL_PLUS_TEST: lambda : UserControlPlusTest(),
                States.AUTO_FACE_FOCUS : lambda : AutoFaceFocus(),
                States.EXIT : lambda : Exit()
            }

    def action(self, drone, screen, eventList):
        for event in eventList:
            drone.resetSpeed()
            if event.type == pygame.QUIT:
                return self.change(state=States.EXIT)

            if event.type == pygame.KEYDOWN:
                # emergency landing
                if event.key == pygame.K_ESCAPE:
                    return self.change(state=States.EXIT)
                elif event.key == pygame.K_1:
                    return self.change(state=States.USER_CONTROL_PLUS_TEST)
                elif event.key == pygame.K_2:
                    return self.change(state=States.AUTO_FACE_FOCUS)
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
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        pygame.display.update()
        return None

    def change(self, state=States.EXIT):
        return self.state_transition[state]()

    def clean(self, drone):
        drone.resetSpeed()


class UserControlPlusTest(DroneState):
    def __init__(self):
        super().__init__()
        self.state_type = States.USER_CONTROL_PLUS_TEST
        self.state_transition = {
                States.AUTO_FACE_FOCUS : lambda : AutoFaceFocus(),
                States.USER_CONTROL : lambda : UserControl(),
                States.EXIT : lambda : Exit()
            }
        
    
    def action(self, drone, screen, eventList):
        for event in eventList:
            drone.resetSpeed()
            if event.type == pygame.QUIT:
                return self.change(state=States.EXIT)

            if event.type == pygame.KEYDOWN:
                # emergency landing
                if event.key == pygame.K_ESCAPE:
                    return self.change(state=States.EXIT)
                elif event.key == pygame.K_1:
                    return self.change(state=States.USER_CONTROL)
                elif event.key == pygame.K_2:
                    return self.change(state=States.AUTO_FACE_FOCUS)
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
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        pygame.display.update()
        return None

    def change(self, state=States.EXIT):
        return self.state_transition[state]()

    def clean(self, drone):
        drone.resetSpeed()


class AutoFaceFocus(DroneState):
    class AFFStates:
        SEARCHING = 0
        TRACKING = 1

    def __init__(self):
        super().__init__()
        self.state_type = States.AUTO_FACE_FOCUS
        self.state_transition = {
                States.USER_CONTROL : lambda : UserControl(),
                States.USER_CONTROL_PLUS_TEST: lambda : UserControlPlusTest(),
                States.EXIT : lambda : Exit()
            }
        # Program Control State has 2 different internal states
        # for searching and tracking
        self._affstate = AFFStates.SEARCHING
        self._face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
        self._tracker = cv2.TrackerKCF_create()
        self._failure_count = 0
        self._failure_needed = 10
        self._pid = Pid(1,1,1, 1.0/30, -100, 100)
        self.bbox = (0,0,0,0)


    """
    bounding box min
    determines the minimum of a and b with a value
    of None as the highest amount.
    """
    def bbMin(self, a, b):
        if a is None:
            return b
        elif b is None:
            return a
        elif a < b:
            return a
        return b

    """
    bounding box max
    determines the maximum of a and b with a value
    of None as the lowest amount.
    """
    def bbMax(self, a, b):
        if a is None:
            return b
        elif b is None:
            return a
        elif a > b:
            return a
        return b
        
        
    """
    Tries to detect a face
    
    returns a 4 tuple of None if no face is detected
    otherwise returns the UNION of all faces found
    """
    def detectFaces(self, frame, classifier):
        I = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_cascade.detectMultiScale(I, 1.3, 5)
        minX = None
        minY = None
        maxXW = None
        maxYH = None
        for (x, y, w, h) in faces:
            minX = self.bbMin(minX, x)
            minY = self.bbMin(minY, y)
            maxXW = self.bbMax(maxXW, x+w)
            maxYH = self.bbMax(maxYH, y+h)
        return (minX, minY, maxXW, maxYH)

    """
    Tries to detect a face
    
    returns a 4 tuple of None if a face is not detected
    otherwise returns the first face found.
    """
    def detectSingleFace(self, frame):
        I = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_cascade.detectMultiScale(I, 1.3, 5)
        for (x, y, w, h) in faces:
            return (x, y, x+w, y+h)
        return (None, None, None, None)

    def action(self, drone, screen, eventList):
        for event in eventList:
            drone.resetSpeed()
            if event.type == pygame.QUIT:
                return self.change(state=States.EXIT)

            if event.type == pygame.KEYDOWN:
                # emergency landing
                if event.key == pygame.K_ESCAPE:
                    return self.change(state=States.EXIT)
                elif event.key == pygame.K_1:
                    return self.change(state=States.USER_CONTROL)
                elif event.key == pygame.K_2:
                    return self.change(state=States.USER_CONTROL_PLUS_TEST)
                else:
                    drone.key_down(event.key)

            elif event.type == pygame.KEYUP:
                # emergency landing
                if event.key == pygame.K_ESCAPE:
                    return self.change(state=States.EXIT)
                else:
                    drone.key_up(event.key)
        data = drone.getData()
        frame = data.FRAME
        if self._affstate == AFFStates.SEARCHING:
            self.bbox = self.detectSingleFace(frame)
            if self.bbox != (None, None, None, None):
                success = self._tracker.init(frame, self.bbox)
                self._affstate == AFFStates.TRACKING
        elif self._affstate == AFFStates.TRACKING:
            success, self.bbox = self._tracker.update(frame)
            if success:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cmx = (p2[0] - p1[0]) / 2
                cmy = (p2[1] - p1[1]) / 2
                frame = cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
                frame = cv2.circle(frame, (cmx, cmy), 15, (200, 20, 20), -1)
                
                diff = cmx - (drone._width / 2)
                pid_output = self._pid.output(diff)
                drone.yaw = pid_output / 100

            else:
                cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
                self._failure_count += 1
                drone.yaw = 0
                if self._failure_count > self._failure_needed:
                    self._failure_count = 0
                    self._pid.reset()
                    self._affstate == AFFStates.SEARCHING
        drone.moveDrone()
        frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        pygame.display.update()
        return None

    def change(self, state=States.EXIT):
        return self.state_transition[state]()

    def clean(self, drone):
        drone.resetSpeed()


class Exit(DroneState):
    def __init__(self):
        super().__init__()
        self.state_type = States.EXIT
        self.state_transition = {
                States.EXIT : lambda : Exit()
            }

    def action(self, drone, eventList):
        drone.turnOff()
        return None

    def change(self, state=States.EXIT):
        return self.state_transition[state]()

    def clean(self, drone):
        pass