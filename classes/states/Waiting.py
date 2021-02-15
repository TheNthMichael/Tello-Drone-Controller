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


class Waiting(DroneState):
    def __init__(self):
        super().__init__()
        self.stateAsString = "Waiting"

    def action(self, drone, screen, eventList):
        drone.resetSpeed()
        for event in eventList:
            if event.type == pygame.QUIT:
                return self.change(state=States.EXIT)

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                # emergency landing
                if event.key == pygame.K_ESCAPE:
                    return States.EXIT
                elif event.key == pygame.K_SPACE:
                    launch_thread = threading.Thread(
                        target=lambda drone: drone.takeoff(), args=[drone]
                    )
                    launch_thread.start()
                    while launch_thread.is_alive():
                        data = drone.getData()
                        frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
                        cv2.putText(
                            frame,
                            "Launching...",
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
                    launch_thread.join()
                    return States.USER_CONTROL
        data = drone.getData()
        frame = cv2.cvtColor(data.FRAME, cv2.COLOR_BGR2RGB)
        cv2.putText(
            frame,
            "In State Waiting",
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