import sys, pygame
sys.path.append('./classes')
import cv2
import numpy
import math
from TelloDrone import TelloDrone
from Controller import Controller
from DroneState
from Face import Face
from Pid import Pid

if __name__ == "__main__":
    start()

def start():
    drone = TelloDrone()
    drone.changeVideoSettings(720, 600)

    stateMachine = StateMachine()

    pygame.init()
    size = width, height = 720, 600
    screen = pygame.display.set_mode((size))
    img = pygame.Surface((width, height))

    print(drone.query_battery())

    if (drone.query_battery() < 10):
        print('Error Battery Too Low...')
        raise Exception('Error Battery Too Low')

    while stateMachine.isNotExit():
        # check for pygame events
        eventList = pygame.event.get()
        try:
            stateMachine.run(drone, eventList)
        except:
            print('-- TRACKING FAILED --')
            drone._spd = 0
            stateMachine.forceExit()
            drone.turnOff()
            raise
    drone.turnOff()
    cv2.destroyAllWindows()