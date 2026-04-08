import cv2 as cv
import cvzone
import mediapipe as mp
import time
from mediapipe.python.solutions import hands
from mediapipe.python import solutions
import numpy as np

cap = cv.VideoCapture(0)

class handDetector():
    def __init__(self,mode = False,max_hands = 2,minDetConf = 0.5 , minTrackConf = 0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.minDetConf = minDetConf
        self.minTrackConf = minTrackConf
        self.hand_detector = hands.Hands(self.mode,self.max_hands,1,self.minDetConf,self.minTrackConf)
        self.mpDraw = solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self,img,draw = True):
        imgrgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.hand_detector.process(imgrgb)

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,hand,hands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo = 0 , draw = True):
        self.lst = [] # coordinates of the hand landmarks)

        if self.results.multi_hand_landmarks:
                hand = self.results.multi_hand_landmarks[handNo]
                for id,lm in enumerate(hand.landmark):
                    h,w,c = img.shape # height and width of img
                    x,y = int(lm.x * w),int(lm.y*h) # coprdinates of landmark
                    self.lst.append([id,x,y])
                    if draw:
                        cv.circle(img,(x, y), 3, (255, 0, 255), cv.FILLED)
        return self.lst
    
    def findFingersUp(self):
        self.fingers = []
        if len(self.lst) != 0:
            #for thumb --> using x - coordinates to tell that thumb is open its x coordinate less than x coordinate of 3rd landmark(just below thumb-tip)
            if(self.lst[4][1] < self.lst[3][1]): # "<" use when the image is flipped horizontally for right hand or just non-filpeed left hand image
                self.fingers.append(1)
            else:
                self.fingers.append(0)

            #for fingers --> using y-coodinate to tell finger is open if its y-coordiant below than 2nd bottom landmark of finger
            for i in range(1,5):
                if(self.lst[self.tipIds[i]][2] < self.lst[self.tipIds[i] - 2][2]):
                    self.fingers.append(1)
                else:
                    self.fingers.append(0)
        return self.fingers
    
    def drawFingers(self,img,id): #id-> landmarks postion to be drawn
        for i in range(0,8,2):
            x,y = self.lst[self.tipIds[id-i]][1:]
            cv.circle(img,(x,y), 3, (255, 0, 255), cv.FILLED)
        return img
    def findDistance(self,img,id1,id2,draw = True):
        x1,y1 = self.lst[id1][1:]
        x2,y2 = self.lst[id2][1:]

        if draw: 
            cv.circle(img,(x1,y1),7,(255,0,0),cv.FILLED)
            cv.circle(img,(x2,y2),7,(255,0,0),cv.FILLED)
            cv.line(img,(x1,y1),(x2,y2),(255,0,0),thickness=2)
            
            cx,cy = (x1+x2)//2,(y1+y2)//2  #centre of line
            cv.circle(img,(cx,cy),7,(255,0,0),cv.FILLED)

        dist = np.hypot(x2-x1,y2-y1)
        
        return dist,img,[(x1,y1),(x2,y2),(cx,cy)]


def main():
    cap = cv.VideoCapture(0)
    pTime = 0 
    cTime = 0
    detector = handDetector()
    while True:
        success, frame = cap.read()
        frame = detector.findHands(frame,False)
        lst = detector.findPosition(frame,0,True)

        if len(lst) != 0:
            print(lst[4]) # printing (id,x,y) of thumb in every frame

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cvzone.putTextRect(frame,f"fps : {int(fps)}",(10,70),3,thickness=2,colorT=(255,255,255),font=cv.FONT_HERSHEY_PLAIN)

        cv.imshow("video",frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
