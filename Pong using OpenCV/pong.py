import cv2
import numpy as np
import mediapipe as mp
import math

#Single Player Screen
def single_player(m, n, ux, uy, flagx, flagy, flag, l, cap):

    # Point counter for the player
    t = 0
        # while loop to make sure the frame is refreshed regularly
    while True:
        success, img = cap.read()
        img = img[0:int(frameHeight), 0:int(frameWidth)]
        
        # Flipping the image read by the webcam so all the movement is mirrored
        img = cv2.flip(img, 1)

        # Creating a canvas and initializing its colour to a shade of blue
        canvas = np.zeros((int(frameHeight),int(frameWidth),3), np.uint8)
        canvas[:] = (50, 30, 30)
        canvas = cv2.addWeighted(canvas,0.8,img,0.2,0,canvas)

        # Process the image for hand detection
        results = hands.process(img)
        cy = -500
        # Draw landmarks on the image
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    if(id == 9):
                        h = img.shape[0]

                        # Finding the coordinates of each landmark
                        cy = int(lm.y * h)

                        # Drawing the landmark connections
                        cv2.rectangle (canvas, (0,int(cy-l)), (3, int(cy+l)), (255,255,255), 5)

        # Increment the points if the ball hits the racket, otherwise set to 0
        if(m-3 <= 30) and ((n+20 >= int(cy-l)) and (n-20 <= int(cy+l)) )and flag == 0:
            t = t+1
            flag = 1 
        elif(m-3 <= 30) and flag == 0:
            t = 0
            flag = 1
        else:
            flag = 0

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

        # Displaying the points and pausing the point counter if no face is detected
        cv2.putText(canvas, str(t), (int(frameWidth/2-40), 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)

        # Updating coordinates of ball
        m = m+ux
        n = n+uy
        # Rendering the frame
        cv2.imshow("Pong", canvas)

        # Game is paused if 'p' is pressed and it terminates if 'q' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('p'):
            canvas1 = canvas
            cv2.putText(canvas1, "PAUSED", (int(frameWidth/2-200), int(frameHeight/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (150,150,150), 4, cv2.LINE_AA)
            cv2.imshow("Pong", canvas1)
            while(cv2.waitKey(1) & 0xFF != ord('p')):
                temp = 1
        elif key == ord('q'):
            break

#Local Multiplayer Screen
def local_multi_player(m, n, ux, uy, flagx, flagy, flag, l, cap):

    # Point counters for the respective players
    t1 = 0
    t2 = 0
    # while loop to make sure the frame is refreshed regularly
    while True:
        success, img = cap.read()
        img = img[0:int(frameHeight), 0:int(frameWidth)]
        # Flipping the image read by the webcam so all the movement is mirrored
        img = cv2.flip(img, 1)        

        # Creating a canvas and initializing its colour to a shade of blue
        canvas = np.zeros((int(frameHeight),int(frameWidth),3), np.uint8)
        canvas[:] = (50, 30, 30)
        canvas = cv2.addWeighted(canvas,0.8,img,0.2,0,canvas)

        # Process the image for hand detection
        results = hands.process(img)
        cy1 = -500
        cy2 = -500
        # Draw landmarks on the image
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    if(id == 9):
                        h, w, c = img.shape

                        # Finding the coordinates of each landmark
                        cx, cy =int(lm.x *w), int(lm.y * h)

                        # Drawing the landmark connections
                        if cx <= int(frameWidth//2):
                            cy1 = cy
                            cv2.rectangle (canvas, (0,int(cy-l)), (3, int(cy+l)), (255,255,255), 5)
                        elif cx > int(frameWidth//2):
                            cy2 = cy
                            cv2.rectangle (canvas, (frameWidth,int(cy-l)), (frameWidth-3, int(cy+l)), (255,255,255), 5)
    
        # Increment the points of other player if the ball misses
        if(m+3 >= frameWidth-30) and ((n+30 >= int(cy2-l)) and (n-30 <= int(cy2+l))) and flag == 0:
            flag = 1 
        elif(m+3 >= frameWidth-30) and flag == 0:
            t1 +=1
            flag = 1
        elif(m+3 <= 30) and ((n+30 >= int(cy1-l)) and (n-30 <= int(cy1+l))) and flag == 0:
            flag = 1 
        elif(m+3 <= 30) and flag == 0:
            t2 +=1
            flag = 1
        else:
            flag = 0
                            
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
        cv2.line(canvas, (int(frameWidth//2), 0), (int(frameWidth//2), int(frameHeight)), (255,255,255), 1)

        # Displaying the points and pausing the point counter if no face is detected
        cv2.putText(canvas, str(t1), (int(frameWidth/2-140), 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)
        cv2.putText(canvas, str(t2), (int(frameWidth/2+120), 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)

        # Updating coordinates of ball
        m = m+ux
        n = n+uy

        # Rendering the frame
        cv2.imshow("Pong", canvas)

        # Game is paused if 'p' is pressed and it terminates if 'q' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('p'):
            canvas1 = canvas
            cv2.putText(canvas1, "PAUSED", (int(frameWidth/2-200), int(frameHeight/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (150,150,150), 4, cv2.LINE_AA)
            cv2.imshow("Pong", canvas1)
            while(cv2.waitKey(1) & 0xFF != ord('p')):
                temp = 1
        elif key == ord('q'):
            break

#Input Screen
def inp(var, text, cap):
    # var1 is the variable in which we shall store the input
    var1 = 0
    
    while True:
        success, img = cap.read()
        img = img[0:int(frameHeight), 0:int(frameWidth)]
        
        # Flipping the image read by the webcam so all the movement is mirrored
        img = cv2.flip(img, 1)

        # Creating a canvas and initializing its colour to a shade of blue
        canvas = np.zeros((int(frameHeight),int(frameWidth),3), np.uint8)
        canvas[:] = (50, 30, 30)
        canvas = cv2.addWeighted(canvas,0.8,img,0.2,0,canvas)

        # Calculating the number of digits in the input
        digits = int(math.log10(var1+0.5))+1

        # Displaying the controls on the top left of the screen
        cv2.putText(canvas, "Spacebar: Confirm", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)
        cv2.putText(canvas, "W: Up", (20,85), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)
        cv2.putText(canvas, "S: Down", (20,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)

        # Displaying the input currently entered
        cv2.putText(canvas, text, (20,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(canvas, str(var1), (int(frameWidth/2)-20*digits,int(frameHeight/2)-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)

        # key1 is used to record keyboard inputs
        key1 = cv2.waitKey(1) & 0xFF

        # Checks whether keyboard input is a number or not
        if key1 > 47 and key1 < 58: 
            var1 = var1*10+key1-48
        # Checks for the keyboard input for backspace
        elif key1 == 8:
            var1 = int(var1/10)
        # Confirm the input if spacebar is pressed
        elif key1 == 32: 
            if var1 != 0:
                if var1 > 300:
                    var1 = 300
                var = var1
            break
        # Rendering the frame
        cv2.imshow("Pong", canvas)
    return var

#Options Screen
def opt(ux, l, cap):

    cursor = 0
        
    while True:
        success, img = cap.read()
        img = img[0:int(frameHeight), 0:int(frameWidth)]
        
        # Flipping the image read by the webcam so all the movement is mirrored
        img = cv2.flip(img, 1)

        # Creating a canvas and initializing its colour to a shade of blue
        canvas = np.zeros((int(frameHeight),int(frameWidth),3), np.uint8)
        canvas[:] = (50, 30, 30)
        canvas = cv2.addWeighted(canvas,0.8,img,0.2,0,canvas)

        # Displaying the controls on the top left
        cv2.putText(canvas, "Spacebar: Confirm", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)
        cv2.putText(canvas, "W: Up", (20,85), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)
        cv2.putText(canvas, "S: Down", (20,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)
        
        # This variable will be used to record keyboard inputs
        key = cv2.waitKey(1) & 0xFF

        # Highlight the currently selected option
        if cursor == 0:
            cv2.putText(canvas, "Configure Speed", (20,int(frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Configure Bar Length", (20,int(frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Quit", (20,int(frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
        elif cursor == 1:
            cv2.putText(canvas, "Configure Speed", (20,int(frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Configure Bar Length", (20,int(frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Quit", (20,int(frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
        elif cursor == 2:
            cv2.putText(canvas, "Configure Speed", (20,int(frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Configure Bar Length", (20,int(frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Quit", (20,int(frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
  
        # If 'w' is pressed, cursor goes up
        if key == ord('w') and cursor != 0:
            cursor -= 1
        # If 's' is pressed, cursor goes down
        elif key == ord('s') and cursor != 2:
            cursor += 1
        # If spacebar is pressed, current option is selected
        elif key == 32:
            if cursor == 0:
                text = "Input the ball speed (Current: "+str(ux)+")"
                ux = inp(ux, text, cap)
            elif cursor == 1:
                text = "Input the length of the bar (Current: "+str(l)+")"
                l = inp(l, text, cap)
            elif cursor == 2:
                break
                
        # Rendering the frame
        cv2.imshow("Pong", canvas)
    return ux, l

#Title Screen
def main():

    # Capturing video from webcam
    cap = cv2.VideoCapture(0)
    fps = 30

    # Setting certain properties for the video capture
    #   3: frameWidth
    #   4: frameHeight
    #   5: frameRate
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(5, fps)
        
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
    ux = 120
    uy = int(ux/3+50)
    flagx = 0
    flagy = 0
    flag = 0
    l = 140
    # ax = 2
    # ay = 2
    cursor = 0
        
    while True:
        success, img = cap.read()
        img = img[0:int(frameHeight), 0:int(frameWidth)]
        
        # Flipping the image read by the webcam so all the movement is mirrored
        img = cv2.flip(img, 1)

        # Creating a canvas and initializing its colour to a shade of blue
        canvas = np.zeros((int(frameHeight),int(frameWidth),3), np.uint8)
        canvas[:] = (50, 30, 30)
        canvas = cv2.addWeighted(canvas,0.8,img,0.2,0,canvas)

        # Creating the elements of the title screen
        cv2.putText(canvas, "PONG", (int(frameWidth/2-185), int(frameHeight/2)-80), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)
        cv2.putText(canvas, "Spacebar: Confirm", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)
        cv2.putText(canvas, "W: Up", (20,85), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)
        cv2.putText(canvas, "S: Down", (20,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)

        # This variable will be used to record keyboard inputs
        key = cv2.waitKey(1) & 0xFF

        # Highlight the currently selected option
        if cursor == 0:
            cv2.putText(canvas, "Rally", (frameWidth-280,int(frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
            cv2.putText(canvas, "1v1", (frameWidth-280,int(frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Options", (frameWidth-280,int(frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Quit", (frameWidth-280,int(frameHeight/2)+220), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
        elif cursor == 1:
            cv2.putText(canvas, "Rally", (frameWidth-280,int(frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "1v1", (frameWidth-280,int(frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Options", (frameWidth-280,int(frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Quit", (frameWidth-280,int(frameHeight/2)+220), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
        elif cursor == 2:
            cv2.putText(canvas, "Rally", (frameWidth-280,int(frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "1v1", (frameWidth-280,int(frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Options", (frameWidth-280,int(frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Quit", (frameWidth-280,int(frameHeight/2)+220), cv2.FONT_HERSHEY_SIMPLEX, 2, (80,60,60), 3, cv2.LINE_AA)        
        elif cursor == 3:
            cv2.putText(canvas, "Rally", (frameWidth-280,int(frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "1v1", (frameWidth-280,int(frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Options", (frameWidth-280,int(frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            cv2.putText(canvas, "Quit", (frameWidth-280,int(frameHeight/2)+220), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
        
        # If 'w' is pressed, cursor goes up
        if key == ord('w'):
            if cursor != 0:
                cursor -= 1

        # If 's' is pressed, cursor goes down        
        if key == ord('s'):
            if cursor != 3:
                cursor += 1

        # If 'spacebar' is pressed, current option is selected
        elif key == 32:
            if cursor == 0:
                single_player(m,n,ux,uy,flagx,flagy,flag,l, cap)
            elif cursor == 1:
                local_multi_player(m,n,ux,uy,flagx,flagy,flag,l, cap)
            elif cursor == 2:
                ux, l = opt(ux, l, cap)
            elif cursor == 3:
                break
        # Rendering the frame
        cv2.imshow("Pong", canvas)
    cap.release()
    cv2.destroyAllWindows()

# Setting a custom frame width
frameWidth = 1280
frameHeight = 9*frameWidth/16

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3, min_tracking_confidence=0.3)

main()