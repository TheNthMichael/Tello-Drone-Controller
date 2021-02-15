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


class Exit(DroneState):
    def __init__(self):
        super().__init__()
        self.stateAsString = "Exit"

    def action(self, drone, eventList):
        drone.turnOff()
        return None

    def clean(self, drone):
        pass