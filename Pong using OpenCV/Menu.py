import cv2
import numpy as np
import math

class Menu:
    def __init__(self, gameSettings, pongGame):
        self.gameSettings = gameSettings
        self.pongGame = pongGame

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

        self.m = 100
        self.n = 100
        self.ux = 50
        self.uy = int(self.ux/2)
        self.flagx = 0
        self.flagy = 0
        self.flag = 0
        self.l = 140
        # self.ax = 2
        # self.ay = 2

        self.frameWidth = gameSettings.frameWidth
        self.frameHeight = gameSettings.frameHeight
        

    def inp(self, var, text, cap):
        # var1 is the variable in which we shall store the input
        var1 = 0
        
        while True:
            success, img = cap.read()
            img = img[0:int(self.frameHeight), 0:int(self.frameWidth)]
            
            # Flipping the image read by the webcam so all the movement is mirrored
            img = cv2.flip(img, 1)

            # Creating a canvas and initializing its colour to a shade of blue
            canvas = np.zeros((int(self.frameHeight),int(self.frameWidth),3), np.uint8)
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
            cv2.putText(canvas, str(var1), (int(self.frameWidth/2)-20*digits,int(self.frameHeight/2)-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)

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

    def opt(self, cap):
        cursor = 0
        
        while True:
            success, img = cap.read()
            img = img[0:int(self.frameHeight), 0:int(self.frameWidth)]
            
            # Flipping the image read by the webcam so all the movement is mirrored
            img = cv2.flip(img, 1)

            # Creating a canvas and initializing its colour to a shade of blue
            canvas = np.zeros((int(self.frameHeight),int(self.frameWidth),3), np.uint8)
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
                cv2.putText(canvas, "Configure Speed", (20,int(self.frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Configure Bar Length", (20,int(self.frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Quit", (20,int(self.frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            elif cursor == 1:
                cv2.putText(canvas, "Configure Speed", (20,int(self.frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Configure Bar Length", (20,int(self.frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Quit", (20,int(self.frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            elif cursor == 2:
                cv2.putText(canvas, "Configure Speed", (20,int(self.frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Configure Bar Length", (20,int(self.frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Quit", (20,int(self.frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
    
            # If 'w' is pressed, cursor goes up
            if key == ord('w') and cursor != 0:
                cursor -= 1
            # If 's' is pressed, cursor goes down
            elif key == ord('s') and cursor != 2:
                cursor += 1
            # If spacebar is pressed, current option is selected
            elif key == 32:
                if cursor == 0:
                    text = "Input the ball speed (Current: "+str(self.ux)+")"
                    self.ux = self.inp(self.ux, text, cap)
                    self.uy = int(self.ux/2)
                elif cursor == 1:
                    text = "Input the length of the bar (Current: "+str(self.l)+")"
                    self.l = self.inp(self.l, text, cap)
                elif cursor == 2:
                    break
                    
            # Rendering the frame
            cv2.imshow("Pong", canvas)

    def title(self):
        # Capturing video from webcam
        cap = cv2.VideoCapture(0)
        fps = 30

        # Setting certain properties for the video capture
        #   3: frameWidth
        #   4: frameHeight
        #   5: frameRate
        cap.set(3, self.frameWidth)
        cap.set(4, self.frameHeight)
        cap.set(5, fps)

        cursor = 0

        while True:
            success, img = cap.read()
            img = img[0:int(self.frameHeight), 0:int(self.frameWidth)]
            
            # Flipping the image read by the webcam so all the movement is mirrored
            img = cv2.flip(img, 1)

            # Creating a canvas and initializing its colour to a shade of blue
            canvas = np.zeros((int(self.frameHeight),int(self.frameWidth),3), np.uint8)
            canvas[:] = (50, 30, 30)
            canvas = cv2.addWeighted(canvas,0.8,img,0.2,0,canvas)

            # Creating the elements of the title screen
            cv2.putText(canvas, "PONG", (int(self.frameWidth/2-185), int(self.frameHeight/2)-80), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 4, cv2.LINE_AA)
            cv2.putText(canvas, "Spacebar: Confirm", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)
            cv2.putText(canvas, "W: Up", (20,85), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)
            cv2.putText(canvas, "S: Down", (20,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (80,60,60), 1, cv2.LINE_AA)

            # This variable will be used to record keyboard inputs
            key = cv2.waitKey(1) & 0xFF

            # Highlight the currently selected option
            if cursor == 0:
                cv2.putText(canvas, "Rally", (self.frameWidth-280,int(self.frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
                cv2.putText(canvas, "1v1", (self.frameWidth-280,int(self.frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Options", (self.frameWidth-280,int(self.frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Quit", (self.frameWidth-280,int(self.frameHeight/2)+220), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            elif cursor == 1:
                cv2.putText(canvas, "Rally", (self.frameWidth-280,int(self.frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "1v1", (self.frameWidth-280,int(self.frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Options", (self.frameWidth-280,int(self.frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Quit", (self.frameWidth-280,int(self.frameHeight/2)+220), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
            elif cursor == 2:
                cv2.putText(canvas, "Rally", (self.frameWidth-280,int(self.frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "1v1", (self.frameWidth-280,int(self.frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Options", (self.frameWidth-280,int(self.frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Quit", (self.frameWidth-280,int(self.frameHeight/2)+220), cv2.FONT_HERSHEY_SIMPLEX, 2, (80,60,60), 3, cv2.LINE_AA)        
            elif cursor == 3:
                cv2.putText(canvas, "Rally", (self.frameWidth-280,int(self.frameHeight/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "1v1", (self.frameWidth-280,int(self.frameHeight/2)+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Options", (self.frameWidth-280,int(self.frameHeight/2)+150), cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 60, 60), 3, cv2.LINE_AA)
                cv2.putText(canvas, "Quit", (self.frameWidth-280,int(self.frameHeight/2)+220), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
            
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
                    self.pongGame.single_player(self.m,self.n,self.ux,self.uy,self.flagx,self.flagy,self.flag,self.l, cap)
                elif cursor == 1:
                    self.pongGame.local_multi_player(self.m,self.n,self.ux,self.uy,self.flagx,self.flagy,self.flag,self.l, cap)
                elif cursor == 2:
                    self.opt(cap)
                elif cursor == 3:
                    break
            # Rendering the frame
            cv2.imshow("Pong", canvas)
        cap.release()
        cv2.destroyAllWindows()
