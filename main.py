import numpy as np
import cv2

def detecting_faces(cap, classifier):
    while True:
        ret, frame = cap.read()
        I = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = classifier.detectMultiScale(I, 1.3, 5)
        # return the first face that occures else repeat until a face is found
        for (x, y, w, h) in faces:
            return (x, y, w, h)

def tracking_face(cap, features, lk, x, y, w, h):
    colors = np.random.randint(0, 255, (100, 3))
    ret, last_frame = cap.read()
    last_I = cv2.cvtColor(last_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(last_I[x: x + w, y: y + h], mask=None, **features)
    mask = np.zeros_like(last_frame)
    while True:
        ret, frame = cap.read()
        I = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        p1, st, err = cv2.calcOpticalFlowPyrLK(last_I, I, p0, None, **lk)

        if p1 is None:
            return True

        good_new = p1[st == 1]
        good_old = p0[st == 1]
        
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), colors[i].tolist(), 2)
            frame = cv2.circle(frame, (int(a), int(b)), 5, colors[i].tolist(), -1)

        img = cv2.add(frame, mask)

        cv2.imshow("Intensity", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        last_I = I.copy()
        p0 = good_new.reshape(-1, 1, 2)
        
    return False
        
def start():
    cap = cv2.VideoCapture(0)

    features = dict(maxCorners=500,
                    qualityLevel=0.3,
                    minDistance=7,
                    blockSize=7)

    lk = dict(winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 0.3))

    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    keep_tracking = True

    while keep_tracking:
        x, y, w, h = detecting_faces(cap, face_classifier)
        keep_tracking = tracking_face(cap, features, lk, x, y, w, h)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start()


