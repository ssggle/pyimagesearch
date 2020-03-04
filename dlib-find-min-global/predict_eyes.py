# ------------------------
#   USAGE
# ------------------------
# python predict_eyes.py --shape-predictor best_predictor.dat

# ------------------------
#   IMPORTS
# ------------------------
# Import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")
args = vars(ap.parse_args())

# Initialize dlib's face detector (HOG-based) and then load our trained shape predictor
print("[INFO] Loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# Initialize the video stream and allow the cammera sensor to warmup
print("[INFO] Camera sensor warming up...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Loop over the frames from the video stream
while True:
    # Grab the frame from the video stream, resize it to have a maximum width of 400 pixels, and convert it to grayscale
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    # Loop over the face detections
    for rect in rects:
        # convert the dlib rectangle into an OpenCV bounding box and
        # draw a bounding box surrounding the face
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # use the custom dlib shape predictor to predict the location
        # of the landmark coordinates, then convert the prediction to
        # an easily parsable NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # loop over the (x, y)-coordinates from the dlib shape
        # predictor model draw them on the image
        for (sX, sY) in shape:
            cv2.circle(frame, (sX, sY), 1, (0, 0, 255), -1)

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()