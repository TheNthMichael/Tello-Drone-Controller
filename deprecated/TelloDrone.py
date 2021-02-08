#   Michael Nickerson 12/25/2020
#   Description:
#       Class for handling Tello
#       Drone connections and 
#       controls
from djitellopy import Tello
import cv2
import numpy
from Controller import Controller

class DroneData:
    def __init__(self):
        self.ACC = (0, 0, 0)
        self.SPD = (0,0,0)
        self.BAR_HEIGHT = 0
        self.HEIGHT = 0  # in cm
        self.ROTATION = (0,0,0) # pitch, roll, yaw
        self.BATTERY = 0    # 0 - 100
        self.DIST_TOF = 0
        self.FLIGHT_TIME = 0
        self.FRAME = None

class TelloDrone:
    _instance = None
    def __init__(self):
        if TelloDrone._instance == None:
            self._drone = Tello()
            self._controller = Controller()
            self._droneData = DroneData()
            self.connect()
            self._width = 360
            self._height = 240
            TelloDrone._instance = self
        else:
            raise Exception("Error only one instance of TelloDrone is allowed")

    """
    reset the djitellopy drone object's
    velocity, actually rather unsure what
    the importance of this is since I use
    send_rc_control to move
    """
    def resetSpeed(self):
        self._drone.for_back_velocity = 0
        self._drone.left_right_velocity = 0
        self._drone.up_down_velocity = 0
        self._drone.yaw_velocity = 0
        self._drone.speed = 0
    
    """
    calls the djitellopy commands
    to turn off the drones stream
    and turn it back on.
    """
    def streamReset(self):
        self._drone.streamoff()
        self._drone.streamon()

    
    """
    Connect to the drone,
    reset the drones speed,
    print the battery, and
    reset the video stream
    """
    def connect(self):
        self._drone.connect()
        self.resetSpeed()
        print(self._drone.get_battery())
        self.streamReset()

    def changeVideoSize(self, width, height):
        self._width = width
        self._height = height

    def updateData(self):
        self._droneData.ACC = (
            self._drone.get_acceleration_x(),
            self._drone.get_acceleration_y(),
            self._drone.get_acceleration_z()
        )
        self._droneData.SPD = (
            self._drone.get_speed_x,
            self._drone.get_speed_y,
            self._drone.get_speed_z
        )
        self._droneData.ROTATION = (
            self._drone.get_pitch(),
            self._drone.get_roll(),
            self._drone.get_yaw()
        )
        self._droneData.BAR_HEIGHT = self._drone.get_barometer()
        self._droneData.HEIGHT = self._drone.get_height()
        self._droneData.BATTERY = self._drone.get_battery()
        self._droneData.DIST_TOF = self._drone.get_distance_tof()
        self._droneData.FLIGHT_TIME = self._drone.get_flight_time()
        self._droneData.FRAME = self.getFrame()

    def getData(self):
        self.updateData()
        return self._droneData
        

    """
    Moves the drone by using a controller
    object to get the direction of each
    movement axis and multiplied by the
    drones constant speed
    """
    def moveDrone(self):
        self.drone.send_rc_control(int(self.controller.left_right * self.controller.speed),
                                   int(self.controller.forward_backward * self.controller.speed),
                                   int(self.controller.up_down * self.controller.speed),
                                   int(self.controller.yaw * self.controller.speed))

    """
    Lands the drone and turns off
    the video stream.
    """
    def turnOff(self):
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
    def getFrame(self):
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