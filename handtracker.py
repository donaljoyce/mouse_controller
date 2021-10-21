import cv2
import time
import os
import mediapipe as mp
from pynput.mouse import Button ,Controller
import wx
import numpy as np


mouse=Controller()
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(clx,cly)=(0,0)
(camx,camy)=(320,240)
print(sx,sy)

mLocOld=np.array([0,0])
mouseLoc=np.array([0,0])

DampingFactor=2

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,camx)
cap.set(4,camy)
with mp_hands.Hands(
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9) as hands:
 isPressed=0
 while cap.isOpened():
    success, image = cap.read()

    
    
    

    
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    
    image.flags.writeable = False
    results = hands.process(image)

  
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    imageHeight, imageWidth, _ = image.shape

    #Drawing green lines connecting hand land marks
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        
        normalizedLandmark = hand_landmarks.landmark[8]
        l5=hand_landmarks.landmark[5]
        lp5=mp_drawing._normalized_to_pixel_coordinates(l5.x, l5.y, imageWidth, imageHeight)
        l8=hand_landmarks.landmark[8]
        lp8=mp_drawing._normalized_to_pixel_coordinates(l8.x, l8.y, imageWidth, imageHeight)
        l9=hand_landmarks.landmark[10]
        lp9=mp_drawing._normalized_to_pixel_coordinates(l9.x, l9.y, imageWidth, imageHeight)
        l12=hand_landmarks.landmark[12]
        lp12=mp_drawing._normalized_to_pixel_coordinates(l12.x, l12.y, imageWidth, imageHeight)
        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
 
       
        
        if(pixelCoordinatesLandmark!=None):
          (clx,cly)=pixelCoordinatesLandmark



        
        
        mouseLoc=mLocOld+((clx,cly)-mLocOld)/2
        #mouse.position=(mouseLoc[0],mouseLoc[1])
        
        mouse.position=(int((mouseLoc[0]*sx)/(camx-30)),int((mouseLoc[1]*sy)/(camy-30)))
        
          

        if(lp8!=None and lp5!=None and lp9!=None and lp12!=None):
          (lp8x,lp8y)=lp8
          (lp5x,lp5y)=lp5
          (lp9x,lp9y)=lp9
          (lp12x,lp12y)=lp12
          if(lp8y<lp5y+5 and lp12y<lp9y+5 and lp12y<lp8x+5 and isPressed==0):
            print(lp8y,lp5y)
            isPressed=1
            mouse.press(Button.left)
          elif(isPressed==1 and lp12y>lp9y+5):
            isPressed=0
            mouse.release(Button.left)
          else:
            pass
          
          
          
            
            
    
    
    
       
        #while mouse.position!=(sx-int((mouseLoc[0]*sx)/camx),int((mouseLoc[1]*sy)/camy)):
         #   pass

        #setting the old location to the current mouse location
        mLocOld=mouseLoc
    
      


    
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()