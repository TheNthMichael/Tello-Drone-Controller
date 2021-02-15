## State Machine
[] Add states for every form of tracking
[] Add states for takeoff
[] Add states for video failure
[] Add states for general failure
[] Add states for turning the drone off but not quitting the application


## SEARCHING and TRACKING
[] Find a better method than lk optical flow
[] Find a better face detection algo than haar cascade classifiers -> look into yolo
[] Add "Focus on me" Tracking
[] Add depth and pan tracking -> look into either using pose estimation, a better face detector, or calcOpticalFlowFarneback which is a dense optical flow algorithm.
    -   Dense optical flow is mainly used for getting rid of backgrounds, but by finding the area of the
        detected object
[] Actually take time to tune the PID controller rather than just using 1 for every constant

## GUI Events
[] Install pygui for GUI elements
[] Add takeoff button
[] Add tracking toggle and a list of tracking modes
[] Add a visualization of the battery

## Pygame showing h264 video format
[] Find a way to display the h264 video frames on a pygame surface
[] Use different threads for sending drone commands and displaying
    the video feed to get rid of delay.

## Testing
[] Write 10 tests for every standalone function or class that has been written so far
[] Continue doing that :^)