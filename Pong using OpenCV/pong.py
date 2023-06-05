import cv2
import numpy as np

frameWidth = 1080
frameHeight = 9*frameWidth/16
handCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(5, 30)
cap.set(10, 10)
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
while True:
    success, img = cap.read()
    black = np.zeros((int(frameHeight),int(frameWidth),3), np.uint8)
    img = cv2.flip(img, 1)
    cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)
    blur = cv2.GaussianBlur(img,(5,5),0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY) 
    retval2,thresh1 = cv2.threshold(gray,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    hand = handCascade.detectMultiScale(gray, 1.1, 4)
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
    cv2.circle(black, (int(m), int(n)), 4, (255,255,255), 10)
    for (x,y,w,h) in hand:
        cv2.rectangle (black, (0,int((2*y+h)/2)-l), (0, int((2*y+h)/2)+l), (255,255,255), 5)
        if(m-3 <= 30) and ((n+30 >= int((2*y+h)/2)-l) and (n-30 <= int((2*y+h)/2)+l)) and flag == 0:
            t = t+1
            flag = 1
        else:
            # t = 0
            flag = 0

    cv2.putText(black, str(t), (int(frameWidth/2), 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)
    m = m+ux
    n = n+uy
    # cv2.imshow("bts", thresh1)
    cv2.imshow("Result", black)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break