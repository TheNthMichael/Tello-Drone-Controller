import sys, threading, pygame
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

# Add paths
sys.path.append("../")

# Custom State Classes
from TelloDrone import TelloDrone
from StateEnumeration import *
from DroneState import DroneState


class UserControlPlusTest(DroneState):
    def __init__(self):
        super().__init__()
        self.stateAsString = "UserControlPlusTest"
        """
        self.figure = plt.figure()
        self.ax = self.figure.gca(projection='3d')
        self.figure.show()
        """
        self.previousEstimatedPoses = {
            "x": [0],
            "y": [0],
            "z": [0],
            "u": [0],
            "v": [0],
            "w": [0],
            "t": [0],
        }

    """
    Adds an estimated pose to previous poses based on drone sensor telemetry.
    """

    def addPose(self, droneData):
        """
        self.ACC = (0, 0, 0)
        self.SPD = (0,0,0)
        self.BAR_HEIGHT = 0
        self.HEIGHT = 0  # in cm
        self.ROTATION = (0,0,0) # pitch, roll, yaw
        self.BATTERY = 0    # 0 - 100
        self.DIST_TOF = 0
        self.FLIGHT_TIME = 0
        self.FRAME = None
        """
        dt = droneData.FLIGHT_TIME - self.previousEstimatedPoses["t"][-1]
        self.previousEstimatedPoses["x"].append(
            self.previousEstimatedPoses["x"][-1]
            + droneData.SPD[0]
            + (droneData.ACC[0] * dt * dt) / 2
        )
        self.previousEstimatedPoses["y"].append(
            self.previousEstimatedPoses["y"][-1]
            + droneData.SPD[1]
            + (droneData.ACC[1] * dt * dt) / 2
        )
        self.previousEstimatedPoses["z"].append(
            self.previousEstimatedPoses["z"][-1]
            + droneData.SPD[2]
            + (droneData.ACC[2] * dt * dt) / 2
        )
        # convert rotation vector from degree to radian
        droneData.ROTATION = (
            math.radians(droneData.ROTATION[0]),
            math.radians(droneData.ROTATION[1]),
            math.radians(droneData.ROTATION[2]),
        )
        self.previousEstimatedPoses["u"].append(
            math.sin(droneData.ROTATION[1]) * math.cos(droneData.ROTATION[2]),
        )
        self.previousEstimatedPoses["v"].append(
            math.sin(droneData.ROTATION[1]) * math.sin(droneData.ROTATION[2]),
        )
        self.previousEstimatedPoses["w"].append(math.cos(droneData.ROTATION[2]))
        self.previousEstimatedPoses["t"].append(droneData.FLIGHT_TIME)

    def drawPoses(self):
        pass
        """self.ax.quiver(
            self.previousEstimatedPoses["x"],
            self.previousEstimatedPoses["y"],
            self.previousEstimatedPoses["z"],
            self.previousEstimatedPoses["u"],
            self.previousEstimatedPoses["v"],
            self.previousEstimatedPoses["w"],
            color='b'
        )
        self.figure.canvas.draw()"""

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
                    return States.AUTO_FACE_FOCUS
                else:
                    drone.key_down(event.key)

            elif event.type == pygame.KEYUP:
                # emergency landing
                if event.key == pygame.K_ESCAPE:
                    return States.EXIT
                else:
                    drone.key_up(event.key)
        drone.moveDrone()
        data = drone.getData()
        self.addPose(data)
        self.drawPoses()
        frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
        cv2.putText(
            frame,
            "In State UserControlPlusTest",
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