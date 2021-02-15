import sys, threading, pygame
import cv2
import math
import numpy as np

# Add paths
sys.path.append("../")

# Custom State Classes
from TelloDrone import TelloDrone
from Pid import Pid
from StateEnumeration import *
from DroneState import DroneState


class AutoFaceFocus(DroneState):
    def __init__(self):
        super().__init__()
        # Program Control State has 2 different internal states
        # for searching and tracking
        self.stateAsString = "AutoFaceFocus"
        self._searching = True
        self._face_cascade = cv2.CascadeClassifier(
            "assets/haarcascade_frontalface_default.xml"
        )
        self._tracker = cv2.TrackerKCF_create()
        self._pid = Pid(1, 1, 1, 1.0 / 30, -100, 100)
        self.bbox = (0, 0, 0, 0)

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
            maxXW = self.bbMax(maxXW, x + w)
            maxYH = self.bbMax(maxYH, y + h)
        return (minX, minY, maxXW - minX, maxYH - minY)

    """
    Tries to detect a face
    
    returns a 4 tuple of None if a face is not detected
    otherwise returns the first face found.
    """

    def detectSingleFace(self, frame):
        I = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_cascade.detectMultiScale(I, 1.3, 5)
        for (x, y, w, h) in faces:
            return (x, y, w, h)
        return (None, None, None, None)

    def action(self, drone, screen, eventList):
        for event in eventList:
            drone.resetSpeed()
            if event.type == pygame.QUIT:
                return States.EXIT

            if event.type == pygame.KEYDOWN:
                # emergency landing
                if event.key == pygame.K_ESCAPE:
                    return States.EXIT
                elif event.key == pygame.K_1:
                    return States.USER_CONTROL
                elif event.key == pygame.K_2:
                    return States.USER_CONTROL_PLUS_TEST
                else:
                    drone.key_down(event.key)

            elif event.type == pygame.KEYUP:
                # emergency landing
                if event.key == pygame.K_ESCAPE:
                    return States.EXIT
                else:
                    drone.key_up(event.key)
        data = drone.getData()
        frame = data.FRAME
        if self._searching:
            print("searching")
            cv2.putText(
                frame,
                "Searching For Face",
                (100, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 0, 255),
                2,
            )
            self.bbox = self.detectSingleFace(frame)
            if self.bbox != (None, None, None, None):
                self._tracker = cv2.TrackerKCF_create()
                success = self._tracker.init(frame, self.bbox)
                self._searching = False
        else:
            print("tracking")
            success, self.bbox = self._tracker.update(frame)
            if success:
                cv2.putText(
                    frame,
                    "Tracking Face",
                    (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (0, 0, 255),
                    2,
                )
                # Tracking success
                p1 = (int(self.bbox[0]), int(self.bbox[1]))
                p2 = (
                    int(self.bbox[0] + self.bbox[2]),
                    int(self.bbox[1] + self.bbox[3]),
                )
                cmx = (p2[0] - p1[0]) / 2
                cmy = (p2[1] - p1[1]) / 2
                frame = cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                frame = cv2.circle(frame, (int(cmx), int(cmy)), 15, (200, 20, 20), -1)
                diff = cmx - (drone._width / 2)
                pid_output = self._pid.output(diff)
                if diff < 0:
                    drone.yaw = -1
                else:
                    drone.yaw = 1
                drone.yaw_speed = abs(pid_output)
            else:
                cv2.putText(
                    frame,
                    "Tracking failure detected",
                    (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (0, 0, 255),
                    2,
                )
                drone.yaw = 0
                self.bbox = (None, None, None, None)
                self._tracker = None
                self._failure_count = 0
                self._pid.reset()
                self._searching = True
        drone.moveDrone()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(
            frame,
            "In State AutoFaceFocus",
            (30, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        pygame.display.update()
        return None

    def clean(self, drone):
        drone.resetSpeed()