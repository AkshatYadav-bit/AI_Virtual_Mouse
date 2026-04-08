import cv2 as cv
import mediapipe as mp
import time
import math
import numpy as np
import handTrackingModule as htm
import cvzone
import autopy

#####################################
wCam , hCam = 640,480
frameR = 100 #frame reduction (coordinate paramter for area of controlling mouse)
smoothening = 7
prev_x,prev_y = 0,0
current_x,current_y = 0,0
clickTime = 0
clickDelay = 0.3   # seconds
#####################################

cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

cTime = 0
pTime = 0
detector = htm.handDetector(max_hands=1)
wScr , hScr = autopy.screen.size() # width of screen and height of screen

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv.flip(img,1)

    #1. Find hand Landmarks
    img = detector.findHands(img)
    lmlst  = detector.findPosition(img,draw=False)

    #drawing the area for mouse control
    cv.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),thickness=2)

    if len(lmlst) != 0:
        #2. getting tip of index and middle fingers
        x1,y1 = lmlst[8][1:]
        x2,y2 = lmlst[12][1:]

        #3. Checking which fingers are up
        fingers = detector.findFingersUp()
        

        #4. only index finger up : moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            #5. Convert Coordinates
            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))

            # taking precaution so value doesn't go beyond screen bound
            x3 = np.clip(x3, 0, wScr)
            y3 = np.clip(y3, 0, hScr)

            #6. Smoothen Values
            current_x = prev_x + (x3 - prev_x) / smoothening
            current_y = prev_y + (y3 - prev_y) / smoothening
            
            #7. Move mouse
            autopy.mouse.move(current_x,current_y)
            cv.circle(img,(x1,y1),15,(255,0,255),cv.FILLED)

            prev_x,prev_y = current_x,current_y
        
        #8. both index and middle fingers are open :- clicking mode
        if fingers[1] == 1 and fingers[2] == 1:

            #9. finding distance b/w fingers
            dist,img,lineInfo = detector.findDistance(img,8,12)
            
            #10. clicking mouse if short distance
            if dist <18 and time.time() - clickTime > clickDelay:
                cv.circle(img,lineInfo[2],10,(0,255,0),cv.FILLED)
                autopy.mouse.click()
                clickTime = time.time()

    # FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cvzone.putTextRect(img,f"fps : {int(fps)}",(10,70),3,thickness=2,colorT=(255,255,255),font=cv.FONT_HERSHEY_PLAIN)
    cv.imshow("video",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

