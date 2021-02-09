#   Michael Nickerson 12/25/2020
#   Description:
#       Class for handling Tello
#       Drone connections and 
#       controls
import cv2
import numpy
from djitellopy import Tello
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

class TelloDrone(Tello, Controller):
    _instance = None
    def __init__(self):
        if TelloDrone._instance == None:
            super().__init__()
            self._droneData = DroneData()
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
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 0
    
    """
    calls the djitellopy commands
    to turn off the drones stream
    and turn it back on.
    """
    def streamReset(self):
        self.streamoff()
        self.streamon()

    
    """
    Connect to the drone,
    reset the drones speed,
    print the battery, and
    reset the video stream
    """
    def connect(self):
        super(TelloDrone, self).connect()
        self.resetSpeed()
        print(self.get_battery)
        self.streamReset()

    def changeVideoSize(self, width, height):
        self._width = width
        self._height = height

    def updateData(self):
        self._droneData.ACC = (
            self.get_acceleration_x(),
            self.get_acceleration_y(),
            self.get_acceleration_z()
        )
        self._droneData.SPD = (
            self.get_speed_x,
            self.get_speed_y,
            self.get_speed_z
        )
        self._droneData.ROTATION = (
            self.get_pitch(),
            self.get_roll(),
            self.get_yaw()
        )
        self._droneData.BAR_HEIGHT = self.get_barometer()
        self._droneData.HEIGHT = self.get_height()
        self._droneData.BATTERY = self.get_battery()
        self._droneData.DIST_TOF = self.get_distance_tof()
        self._droneData.FLIGHT_TIME = self.get_flight_time()
        # if we fail to get a new frame, use the old one
        tmp_frame = self._droneData.FRAME
        self._droneData.FRAME = self.getFrame()
        if self._droneData.FRAME is None:
            self._droneData.FRAME = tmp_frame

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
        self.send_rc_control(int(self.left_right * self.speed),
                                   int(self.forward_backward * self.speed),
                                   int(self.up_down * self.speed),
                                   int(self.yaw * self.speed))

    """
    Lands the drone and turns off
    the video stream.
    """
    def turnOff(self):
        try:
            self.land()
            self.streamoff()
        except:
            print("drone is already landing")

        
    """
    gets a single video frame from the
    drone and resizes it to the width
    and height parameters set through
    change_video_settings(self, width, height)
    """
    def getFrame(self):
        drone_frame = self.get_frame_read()
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