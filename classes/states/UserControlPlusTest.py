import sys, pygame
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
from DroneIPC import DroneIPC


class UserControlPlusTest(DroneState):
    def __init__(self):
        super().__init__()
        self.stateAsString = "UserControlPlusTest"
        self.ipc = DroneIPC('127.0.0.1', 5000, 4000)

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
        # self.ipc.data = []
        # DataFormat: 
        #   [accx, accy, accz, du, dv, dw, t]
        self.ipc.data = []
        self.ipc.data.append(droneData.ACC[0])
        self.ipc.data.append(droneData.ACC[1])
        self.ipc.data.append(droneData.ACC[2])
        self.ipc.data.append(math.sin(math.radians(droneData.ROTATION[0])) * math.cos(math.radians(droneData.ROTATION[2])))
        self.ipc.data.append(math.sin(math.radians(droneData.ROTATION[1])) * math.sin(math.radians(droneData.ROTATION[2])))
        self.ipc.data.append(math.cos(math.radians(droneData.ROTATION[2])))
        self.ipc.data.append(droneData.FLIGHT_TIME)

    def drawPoses(self):
        self.ipc.update()

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
            """In State UserControlPlusTest (Battery=""" + str(data.BATTERY) + """)
                Rotation = """ +  + """
            """,
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