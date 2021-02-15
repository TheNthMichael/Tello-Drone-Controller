import sys, threading, pygame
import cv2
import math
import numpy as np

# Add paths
sys.path.append("../")

# Custom State Classes
from TelloDrone import TelloDrone
from StateEnumeration import *
from DroneState import DroneState


class UserControl(DroneState):
    def __init__(self):
        super().__init__()
        self.stateAsString = "UserControl"

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
                    return States.USER_CONTROL_PLUS_TEST
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
        frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
        cv2.putText(
            frame,
            "In State UserControl",
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