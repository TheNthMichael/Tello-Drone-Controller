# Tello-Drone-Controller
A controller application made in python using pygame for events and opencv for image processing.

## Setup
Dependencies:
```
Made using python 3.9.1
```
```
  pip install pygame
  pip install numpy
  pip install djitellopy
  pip install opencv-contrib-python
```
## Running
Ensure you are connected to the drone via wifi on the machine you are using as a controller and run:
```
python App.py
```
This will launch the application and will attempt to setup a udp connection to the drone through the djitellopy library. Wait for two windows to appear.
One is the video feed which is currently using cv2.imshow and the other is a blank pygame window. I will later change this so that the display is shown
only through the pygame window since controls only work when this window is focused. Once these windows open up, press Space to launch the drone. After
the launch is completed, the screen will show that the drone is in the User Control state which allows for the control scheme below:

Forward/Backward: w,s
Left/Right: a,d
Up/Down: spacebar/shift
Rotate Left/Right: q,e
Exit And Land: escape
toggle UserControl/UserControlPlusTest: 1
toggle AutoFaceFocus: 2

## Face Tracking
currently only supports a "focus on face" approach to tracking.
The drone currently only tracks the first face it finds in the camera.
When the face is lost, the drone will look for a new face by turning in the direction the last face was going.
### Methods used
I used a kcf tracker and haar cascades from opencv-contrib-python, we get the original bounding box by a face detector and feed it into the tracker.
Every consecutive frame, we update the tracker to recieve a new bounding box of which we take the center point of and get the error from the center
of the frame. The program uses a PID controller to adjust the yaw for this error.
