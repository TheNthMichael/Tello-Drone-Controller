#   Michael Nickerson 12/25/2020
#   Description:
#       Class for handling Tello
#       Drone connections and 
#       controls
from djitellopy import Tello
import cv2
import numpy
from Controller import Controller

class TelloDrone:
    instance = None
    def __init__(self):
        if TelloDrone.instance == None:
            self.drone = Tello()
            self.myConnect()
            self.width = 360
            self.height = 240
            TelloDrone.instance = self
        else:
            raise Exception("Error only one instance of TelloDrone is allowed")

    """
    reset the djitellopy drone object's
    velocity, actually rather unsure what
    the importance of this is since I use
    send_rc_control to move
    """
    def reset_speed(self):
        self.drone.for_back_velocity = 0
        self.drone.left_right_velocity = 0
        self.drone.up_down_velocity = 0
        self.drone.yaw_velocity = 0
        self.drone.speed = 0
    
    """
    calls the djitellopy commands
    to turn off the drones stream
    and turn it back on.
    """
    def stream_reset(self):
        self.drone.streamoff()
        self.drone.streamon()

    
    """
    Connedct to the drone,
    reset the drones speed,
    print the battery, and
    reset the video stream
    """
    def myConnect(self):
        self.drone.connect()
        self.reset_speed()
        print(self.drone.get_battery())
        self.stream_reset()

    def change_video_settings(self, width, height):
        self.width = width
        self.height = height

    """
    Moves the drone by using a controller
    object to get the direction of each
    movement axis and multiplied by the
    drones constant speed
    """
    def move_drone(self, controller):
        self.drone.send_rc_control(controller.left_right * controller.speed,
                                   controller.forward_backward * controller.speed,
                                   controller.up_down * controller.speed,
                                   controller.yaw * controller.speed)

    """
    Lands the drone and turns off
    the video stream.
    """
    def turn_off(self):
        try:
            self.drone.land()
            self.drone.streamoff()
        except:
            print("drone is already landing")

        
    """
    gets a single video frame from the
    drone and resizes it to the width
    and height parameters set through
    change_video_settings(self, width, height)
    """
    def get_frame(self):
        drone_frame = self.drone.get_frame_read()
        drone_frame = drone_frame.frame
        img = cv2.resize(drone_frame, (self.width, self.height))
        return img

    """
    trying to turn a drone frame into a surface
    to be displayed on a pygame screen.
    """
    def frame2surface(self, surface, arr):
        tmp = surface.get_buffer()
        tmp.write(arr.tostring(), 0)