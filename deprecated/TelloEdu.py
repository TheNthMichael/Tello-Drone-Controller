import sys, pygame
sys.path.append('./classes')
import cv2
import numpy
import math
from TelloDrone import TelloDrone
from Controller import Controller
from DroneState import States, StateMachine
from Face import Face
from Pid import Pid


def myExp(x):
    return -1 * math.exp(-x/60) + 1

def run_app():
    drone = TelloDrone()
    drone.change_video_settings(720, 600)

    controller = Controller()
    controller.yaw_speed = 70

    state_machine = StateMachine()

    pid = Pid(1,1,1, 1.0/30)

    pygame.init()
    size = width, height = 720, 600
    screen = pygame.display.set_mode((size))
    img = pygame.Surface((width, height))

    features = dict(maxCorners=500,
                    qualityLevel=0.3,
                    minDistance=7,
                    blockSize=7)

    lk = dict(winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 0.3))

    face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')

    print(drone.drone.query_battery())

    myFace = None
    last_I = None

    while state_machine.state != States.EXIT:
            # check for pygame events
            for event in pygame.event.get():
                drone.reset_speed()
                if event.type == pygame.QUIT:
                    state_machine.state_change(2)
                    drone.turn_off()
                    break

                if event.type == pygame.KEYDOWN:
                    # emergency landing
                    if event.key == pygame.K_ESCAPE:
                        print('turning off')
                        state_machine.state_change(2)
                        drone.turn_off()
                        break
                    elif event.key == pygame.K_l and state_machine.state == States.WAITING:
                        state_machine.state_change(0)
                        drone.drone.takeoff()
                    elif event.key == pygame.K_p and state_machine.state == States.USER_CONTROL:
                        state_machine.state_change(0)
                    elif event.key == pygame.K_p and state_machine.auto == True:
                        state_machine.state_change(1)
                    else:
                        controller.key_down(event.key)

                elif event.type == pygame.KEYUP:
                    controller.key_up(event.key)
        
            # deal with states
            if (state_machine.state == States.WAITING):
                print('waiting for takeoff')
                drone_frame = drone.get_frame()
                if drone_frame is not None:
                    img = cv2.resize(drone_frame, (width, height))
                    cv2.imshow('Camera', img)
        
            elif (state_machine.state == States.USER_CONTROL):
                drone.move_drone(controller)
                drone_frame = drone.get_frame()
                if drone_frame is not None:
                    img = cv2.resize(drone_frame, (width, height))
                    cv2.imshow('Camera', img)
            
            elif (state_machine.state == States.SEARCHING):
                try:
                    drone.move_drone(controller)
                    drone_frame = drone.get_frame()
                    if drone_frame is not None:
                        img = cv2.resize(drone_frame, (width, height))
                        ret, myFace = detecting_face(img, face_cascade)
                        if ret:
                            ret, last_I = myFace.prepare_tracker(img, features)
                            if ret:
                                state_machine.state_change(0)
                        cv2.imshow('Camera', img)
                except:
                    print('-- SEARCHING FAILED --')
                    state_machine.state_change(2)
                    raise
            elif (state_machine.state == States.TRACKING):
                try:
                    drone_frame = drone.get_frame()
                    if drone_frame is not None:
                        img = cv2.resize(drone_frame, (width, height))
                        ret, last_I = myFace.tracking_face(last_I, img, lk)
                        cmx = int(myFace.x + myFace.w / 2)
                        cmy = int(myFace.y + myFace.h / 2)
                        img = cv2.circle(img, ( cmx, cmy), 15, myFace.colors[0].tolist(), -1)
                        img = cv2.rectangle(img, (int(myFace.x),int(myFace.y) ), (int(myFace.x + myFace.w), int(myFace.y + myFace.h) ), (255,100,100), 2)
                        diff = cmx - (width // 2)
                        # sign = diff / abs(diff)
                        output = pid.output(diff)
                        if abs(diff) > 50:
                            sign = 1
                            if output != 0:
                                sign = output / abs(output)
                            controller.yaw = sign * myExp(abs(output))
                        else:
                            controller.yaw = 0
                        if not ret:
                            state_machine.state_change(0)
                        drone.move_drone(controller)
                        cv2.imshow('Camera', img)
                except:
                    print('-- TRACKING FAILED --')
                    state_machine.state_change(2)
                    raise
    drone.turn_off()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_app()