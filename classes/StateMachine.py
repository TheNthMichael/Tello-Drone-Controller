import sys, threading, multiprocessing
import pygame
import cv2
import math
import numpy as np

# Add paths
sys.path.append("./states")

# Custom Required Classes
from TelloDrone import TelloDrone
from StateEnumeration import *

# Custom State Classes
from Waiting import Waiting
from UserControl import UserControl
from UserControlPlusTest import UserControlPlusTest
from AutoFaceFocus import AutoFaceFocus
from Exit import Exit

class StateMachine:
    def __init__(self):
        self.state = Waiting()
        self._isExit = False
        self.stateTransitions = {
            States.WAITING: {
                States.USER_CONTROL: lambda: UserControl(),
                States.AUTO_FACE_FOCUS: lambda: AutoFaceFocus(),
                States.EXIT: lambda: Exit(),
            },
            States.USER_CONTROL: {
                States.USER_CONTROL_PLUS_TEST: lambda: UserControlPlusTest(),
                States.AUTO_FACE_FOCUS: lambda: AutoFaceFocus(),
                States.EXIT: lambda: Exit(),
            },
            States.USER_CONTROL_PLUS_TEST: {
                States.AUTO_FACE_FOCUS: lambda: AutoFaceFocus(),
                States.USER_CONTROL: lambda: UserControl(),
                States.EXIT: lambda: Exit(),
            },
            States.AUTO_FACE_FOCUS: {
                States.USER_CONTROL: lambda: UserControl(),
                States.USER_CONTROL_PLUS_TEST: lambda: UserControlPlusTest(),
                States.EXIT: lambda: Exit(),
            },
            States.EXIT: {States.EXIT: lambda: Exit()},
        }

    def run(self, drone, screen, eventList):
        tmp_state = self.state.action(drone, screen, eventList)
        if tmp_state is not None:
            self.state.clean(drone)
            self.change(stateTo=tmp_state)

    def change(self, stateTo=States.EXIT):
        if stateTo == States.EXIT:
            self._isExit = True
        self.state = self.stateTransition[self.state][stateTo]()

    def isNotExit(self):
        return not self._isExit

    def forceExit(self):
        self.state = Exit()
        self._isExit = True