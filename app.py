#importing all the required libraries
import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np
from boltiot import Bolt

cap = cv2.VideoCapture(0) #Checks for camera

mpHands = mp.solutions.hands #detects hand/finger
hands = mpHands.Hands()   #complete the initialization configuration of hands
mpDraw = mp.solutions.drawing_utils

# Initialize the Bolt IoT WiFi module
api_key = "XXXXXXXXXXXX"
device_id = "XXXXXXXX"
mybolt = Bolt(api_key, device_id)

def turn_on_led():
    response = mybolt.digitalWrite('0','HIGH')
    print('LED ON')
    
def turn_off_led():
    response = mybolt.digitalWrite('0','LOW')
    print('LED OFF')
    
def turn_on_buzzer():
    response = mybolt.digitalWrite('1','HIGH')
    print('BUZZER ON')
    
def turn_off_buzzer():
    response = mybolt.digitalWrite('1','LOW')
    print('BUZZER OFF')    
	
while True:
    success,img = cap.read() #If camera works capture an image
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Convert to rgb
    
    #Collection of gesture information
    results = hands.process(imgRGB) #completes the image processing.
 
    lmList = [] #empty list
    if results.multi_hand_landmarks: #list of all hands detected.
        #By accessing the list, we can get the information of each hand's corresponding flag bit
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark): #adding counter and returning it
                # Get finger joint points
                h,w,_ = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy]) #adding to the empty list 'lmList'
            mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)
    
    if lmList != []:
        #getting the value at a point
                        #x      #y
        x1,y1 = lmList[4][1],lmList[4][2]  #thumb
        x2,y2 = lmList[8][1],lmList[8][2]  #index finger
        #creating circle at the tips of thumb and index finger
        cv2.circle(img,(x1,y1),13,(255,0,0),cv2.FILLED) #image #fingers #radius #bgr
        cv2.circle(img,(x2,y2),13,(255,0,0),cv2.FILLED) #image #fingers #radius #bgr
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)  #create a line b/w tips of index finger and thumb
        length1 = hypot(x2-x1,y2-y1) #distance b/w tips using hypotenuse
    
        # Check if the index finger and middle finger are up
        x3, y3 = lmList[4][1],lmList[4][2]  # thumb tip coordinates
        x4, y4 = lmList[12][1], lmList[12][2]  # middle finger tip coordinates
        # Draw circle at the fingertips of index finger and middle finger
        cv2.circle(img,(x3,y3),13,(0,255,0),cv2.FILLED) #image #fingers #radius #bgr
        cv2.circle(img,(x4,y4),13,(0,255,0),cv2.FILLED) #image #fingers #radius #bgr
        cv2.line(img,(x3,y3),(x4,y4),(0,255,0),3)  #create a line b/w tips of index finger and thumb
        # Calculate the distance between the index finger and middle finger tips
        length2 = hypot(x4 - x3, y4 - y3)
        
        if length1<50:
            turn_off_led()
        else:
            turn_on_led()
        
        if length2<50:
            turn_on_buzzer()
        else:
            turn_off_buzzer()
            
    else:
        turn_on_led()
        turn_off_buzzer()
            
    cv2.imshow('Image',img) #Show the video 
    if cv2.waitKey(1) & 0xff==ord(' '):
        break
        
cap.release()     #stop cam       
cv2.destroyAllWindows() #close window