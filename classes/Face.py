import numpy as np
import cv2

"""
For now, this class is just a
data struture for the return
value of the face detector.
This will later be used with
the lk optical flow algorithm
for tracking
"""
class Face:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.p0 = None
        self.colors = None

    def prepare_tracker(self, frame, features):
        try:
            self.colors = np.random.randint(0, 255, (100, 3))
            last_I = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.p0 = cv2.goodFeaturesToTrack(last_I[self.x: self.x + self.w, self.y: self.y + self.h], mask=None, **features)
            #mask = np.zeros_like(frame)
            if not (self.p0 is None):
                return (True, last_I)
            return (False, last_I)
        except:
            raise

    def tracking_face(self, last_I, frame, lk):
        try:
            I = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            p1, st, err = cv2.calcOpticalFlowPyrLK(last_I, I, self.p0, None, **lk)

            if p1 is None:
                return (False, None)

            good_new = p1[st == 1]
            good_old = self.p0[st == 1]

            # compute the average change in velocity
            #       While this should mainly be my face,
            #       cropping the face detection could help
            #       limit incorrect features
            avg_dx = 0
            avg_dy = 0
            count = 0

            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                #mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), colors[i].tolist(), 2)
                #frame = cv2.circle(frame, (int(a), int(b)), 5, colors[i].tolist(), -1)
                avg_dx += a - c
                avg_dy += b - d
                count += 1
            if count != 0:
                avg_dx /= count
                avg_dy /= count
            else:
                avg_dx = 0
                avg_dy = 0

            self.x += avg_dx
            self.y += avg_dy

            #img = cv2.add(frame, mask)
            last_I = I.copy()
            self.p0 = good_new.reshape(-1, 1, 2)
            return (True, last_I)
        except:
            raise