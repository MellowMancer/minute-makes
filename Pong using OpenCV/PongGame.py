import cv2
import numpy as np
import random

class PongGame:
    def __init__(self, gameSettings):
        self.gameSettings = gameSettings

    def single_player(self, m,n,ux,uy,flagx,flagy,flag,l, cap):
        # Point counter for the player
        t = 0
            # while loop to make sure the frame is refreshed regularly
        while True:
            success, img = cap.read()
            img = img[0:int(self.gameSettings.frameHeight), 0:int(self.gameSettings.frameWidth)]
            
            # Flipping the image read by the webcam so all the movement is mirrored
            img = cv2.flip(img, 1)

            # Creating a canvas and initializing its colour to a shade of blue
            canvas = np.zeros((int(self.gameSettings.frameHeight),int(self.gameSettings.frameWidth),3), np.uint8)
            canvas[:] = (50, 30, 30)
            canvas = cv2.addWeighted(canvas,0.8,img,0.2,0,canvas)

            image = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
            # Process the image for hand detection
            results = self.gameSettings.hands.process(image)
            cy = -500
            # Draw landmarks on the image
            if results.multi_hand_landmarks:
                center = results.multi_hand_landmarks[0].landmark[9]

                # Finding the coordinates of each landmark
                cy = int(center.y * img.shape[0])

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
            if((m+3 >= self.gameSettings.frameWidth - 30) or (m-3 <= 30)) and flagx == 0:
                ux = -ux
                uy += random.randint(-10, 10)
                flagx = 1
            else:
                flagx = 0
            if((n+3 >= self.gameSettings.frameHeight - 30) or (n-3 <= 30)) and flagy == 0:
                uy = -uy
                flagy = 1
            else:
                flagy = 0

            # Creating the ball and updating its position with each iteration
            cv2.circle(canvas, (int(m), int(n)), 4, (255,255,255), 10)

            # Displaying the points and pausing the point counter if no face is detected
            cv2.putText(canvas, str(t), (int(self.gameSettings.frameWidth/2-40), 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)

            # Updating coordinates of ball
            m = m+ux
            n = n+uy
            # Rendering the self.gameSettings.frame
            cv2.imshow("Pong", canvas)

            # Game is paused if 'p' is pressed and it terminates if 'q' is pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord('p'):
                canvas1 = canvas
                cv2.putText(canvas1, "PAUSED", (int(self.gameSettings.frameWidth/2-200), int(self.gameSettings.frameHeight/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (150,150,150), 4, cv2.LINE_AA)
                cv2.imshow("Pong", canvas1)
                while(cv2.waitKey(1) & 0xFF != ord('p')):
                    temp = 1
            elif key == ord('q'):
                break

    def local_multi_player(self, m, n, ux, uy, flagx, flagy, flag, l, cap):
        # Point counters for the respective players
        t1 = 0
        t2 = 0
        # while loop to make sure the frame is refreshed regularly
        while True:
            success, img = cap.read()
            img = img[0:int(self.gameSettings.frameHeight), 0:int(self.gameSettings.frameWidth)]
            # Flipping the image read by the webcam so all the movement is mirrored
            img = cv2.flip(img, 1)        

            # Creating a canvas and initializing its colour to a shade of blue
            canvas = np.zeros((int(self.gameSettings.frameHeight),int(self.gameSettings.frameWidth),3), np.uint8)
            canvas[:] = (50, 30, 30)
            canvas = cv2.addWeighted(canvas,0.8,img,0.2,0,canvas)

            # Process the image for hand detection
            results = self.gameSettings.hands.process(img)
            cy1 = -500
            cy2 = -500
            # Draw landmarks on the image
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    center = handLms.landmark[9]
                    if(id == 9):
                        h, w, c = img.shape

                        # Finding the coordinates of each landmark
                        cx, cy =int(center.x *w), int(center.y * h)

                        # Drawing the landmark connections
                        if cx <= int(self.gameSettings.frameWidth//2):
                            cy1 = cy
                            cv2.rectangle (canvas, (0,int(cy-l)), (3, int(cy+l)), (255,255,255), 5)
                        elif cx > int(self.gameSettings.frameWidth//2):
                            cy2 = cy
                            cv2.rectangle (canvas, (self.gameSettings.frameWidth,int(cy-l)), (self.gameSettings.frameWidth-3, int(cy+l)), (255,255,255), 5)
        
            # Increment the points of other player if the ball misses
            if(m+3 >= self.gameSettings.frameWidth-30) and ((n+30 >= int(cy2-l)) and (n-30 <= int(cy2+l))) and flag == 0:
                flag = 1 
            elif(m+3 >= self.gameSettings.frameWidth-30) and flag == 0:
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
            if((m+3 >= self.gameSettings.frameWidth - 30) or (m-3 <= 30)) and flagx == 0:
                ux = -ux
                flagx = 1
            else:
                flagx = 0
            if((n+3 >= self.gameSettings.frameHeight - 30) or (n-3 <= 30)) and flagy == 0:
                uy = -uy
                flagy = 1
            else:
                flagy = 0

            # Creating the ball and updating its position with each iteration
            cv2.circle(canvas, (int(m), int(n)), 4, (255,255,255), 10)
            cv2.line(canvas, (int(self.gameSettings.frameWidth//2), 0), (int(self.gameSettings.frameWidth//2), int(self.gameSettings.frameHeight)), (255,255,255), 1)

            # Displaying the points and pausing the point counter if no face is detected
            cv2.putText(canvas, str(t1), (int(self.gameSettings.frameWidth/2-140), 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)
            cv2.putText(canvas, str(t2), (int(self.gameSettings.frameWidth/2+120), 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)

            # Updating coordinates of ball
            m = m+ux
            n = n+uy

            # Rendering the frame
            cv2.imshow("Pong", canvas)

            # Game is paused if 'p' is pressed and it terminates if 'q' is pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord('p'):
                canvas1 = canvas
                cv2.putText(canvas1, "PAUSED", (int(self.gameSettings.frameWidth/2-200), int(self.gameSettings.frameHeight/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (150,150,150), 4, cv2.LINE_AA)
                cv2.imshow("Pong", canvas1)
                while(cv2.waitKey(1) & 0xFF != ord('p')):
                    temp = 1
            elif key == ord('q'):
                break