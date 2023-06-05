import cv2
import numpy as np

# Setting a custom frame width
frameWidth = 1080
frameHeight = 9*frameWidth/16

# Using Cascade Classifier to detect objects (Face) in the video stream
faceCascade = cv2.CascadeClassifier("Pong using OpenCV\haarcascade_frontalface_alt.xml")

# Capturing video from webcam
cap = cv2.VideoCapture(0)

# Setting certain properties for the video capture
#   3: frameWidth
#   4: frameHeight
#   5: frameRate
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(5, 30)

# Setting initial parameters for the ball
#   m: Current x-coordinate
#   n: Current y-coordinate
#   ux: Horizontal velocity
#   uy: Vertical velocity
#   t: Point Counter (Not Time)
#   flagx, flagy and flag: Flags
#   l: Half the length of the "racket"
#   ax: Horizontal acceleration
#   ay: Vertical acceleration
m = 100
n = 100
ux = 100
uy = 50
t = 0
flagx = 0
flagy = 0
flag = 0
l = 120
# ax = 2
# ay = 2

# while loop to make sure the frame is refreshed regularly
while True:
    success, img = cap.read()
    # Creating a canvas and initializing its colour to a shade of blue
    canvas = np.zeros((int(frameHeight),int(frameWidth),3), np.uint8)
    canvas[:] = (50, 30, 30)

    # Flipping the image read by the webcam so all the movement is mirrored
    img = cv2.flip(img, 1)

    # Converting the image to greyscale for later use in face recognition
    blur = cv2.GaussianBlur(img,(5,5),0)
    grey = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    # Detecting all the faces in the image
    face = faceCascade.detectMultiScale(grey, 1.1, 4)
    # Specifying boundary conditions so that the ball stays in the canvas
    if((m+3 >= frameWidth - 30) or (m-3 <= 30)) and flagx == 0:
        ux = -ux
        flagx = 1
    else:
        flagx = 0
    if((n+3 >= frameHeight - 30) or (n-3 <= 30)) and flagy == 0:
        uy = -uy
        flagy = 1
    else:
        flagy = 0

    # Creating the ball and updating its position with each iteration
    cv2.circle(canvas, (int(m), int(n)), 4, (255,255,255), 10)
    if(face == ()):
        cv2.putText(canvas, "Face not detected: Point counter paused", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,200,200), 3, cv2.LINE_AA)

    # Used to create a "racket" for each face recognized
    for (x,y,w,h) in face:
        cv2.rectangle (canvas, (0,int((2*y+h)/2)-l), (3, int((2*y+h)/2)+l), (255,255,255), 5)

        # Increment the points if the ball hits the racket, otherwise set to 0
        if(m-3 <= 30) and ((n+10 >= int((2*y+h)/2)-l) and (n-10 <= int((2*y+h)/2)+l)) and flag == 0:
            t = t+1
            flag = 1 
        elif(m-3 <= 30) and flag == 0:
            t = 0
            flag = 1
        else:
            flag = 0

    # Displaying the points
    cv2.putText(canvas, str(t), (int(frameWidth/2), 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)

    # Updating coordinates of ball
    m = m+ux
    n = n+uy

    # Rendering the frame
    cv2.imshow("Pong", canvas)
    if cv2.waitKey(3) & 0xFF == ord('q'):
        break