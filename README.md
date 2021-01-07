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
  pip install opencv-python
```
## Running
Ensure you are connected to the drone via wifi on the machine you are using as a controller and run:
```
python TelloEdu.py
```
This will launch the application and will attempt to setup a udp connection to the drone through the djitellopy library. Wait for two windows to appear.
One is the video feed which is currently using cv2.imshow and the other is a blank pygame window. I will later change this so that the display is shown
only through the pygame window since controls only work when this window is focused. Once these windows open up, press L to launch the drone. The video
feed will be down during the launch - I most likely need to call the takeoff function in a separate thread to fix this issue. Once the feed comes back,
you will be able to control the drone with the control scheme below.

Forward/Backward: w,s
Left/Right: a,d
Up/Down: spacebar/shift
Rotate Left/Right: q,e
Exit And Land: escape
Toggle Face Tracking: p -> Note while face tracking, you will lose control of the rotate left/right controls as those are used to focus on the targets face

## Face Tracking
currently only supports a "focus on face" approach to tracking.
The drone currently only tracks the first face it finds in the camera.
When the face is lost, the drone will look for a new face by turning in the direction the last face was going.
### Methods used
I used LK Optical Flow and a face Cascade Classifier using OpenCV.
My approach was to find a face and then pass the subimage around the face into cv2.goodFeaturesToTrack(). I then use those features in cv2.calcOpticalFlowPyrLK() to track
where they go, I take the average velocity of these points and update the position of the tracked face. There are currently issues with the tracked points moving away from
the detected face which I plan to fix by removing velocities that are outliers and also checking every few frames for if there exists a face that is a bounding box to the
tracking points.
