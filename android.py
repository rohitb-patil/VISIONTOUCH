#This code is to swipe left and right in an android phone connected to python. 
import cv2
import numpy as np
import dlib
from math import hypot
import schedule
import time

import subprocess

def send_scroll_command(start_x, start_y, end_x, end_y):
    cmd = f"adb shell input swipe {start_x} {start_y} {end_x} {end_y}"
    subprocess.run(cmd.split())

font = cv2.FONT_HERSHEY_SIMPLEX
ip_camera_url = "http://192.168.1.37:8080/video"  # Replace with your IP camera's stream URL

# Create a VideoCapture object
count =0
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor =dlib.shape_predictor("D:\PW1\pw1\shape_predictor_68_face_landmarks.dat") 
def midpoint(p1,p2):
    return int((p1.x + p2.x)/2),int((p1.y + p2.y)/2)
  
  
def get_gaze_ratio(eye_points,landmarks):
  left_eye_region = np.array([(landmarks.part(eye_points[0]).x,landmarks.part(eye_points[0]).y),
                                    (landmarks.part(eye_points[1]).x,landmarks.part(eye_points[1]).y),
                                    (landmarks.part(eye_points[2]).x,landmarks.part(eye_points[2]).y),
                                    (landmarks.part(eye_points[3]).x,landmarks.part(eye_points[3]).y),
                                    (landmarks.part(eye_points[4]).x,landmarks.part(eye_points[4]).y),
                                    (landmarks.part(eye_points[5]).x,landmarks.part(eye_points[5]).y) ],np.int32)
  right_eye_region = np.array([(landmarks.part(eye_points[0]).x,landmarks.part(eye_points[0]).y),
                                    (landmarks.part(eye_points[1]).x,landmarks.part(eye_points[1]).y),
                                    (landmarks.part(eye_points[2]).x,landmarks.part(eye_points[2]).y),
                                    (landmarks.part(eye_points[3]).x,landmarks.part(eye_points[3]).y),
                                    (landmarks.part(eye_points[4]).x,landmarks.part(eye_points[4]).y),
                                    (landmarks.part(eye_points[5]).x,landmarks.part(eye_points[5]).y) ],np.int32) 

        
        #to create mask on rest on face exept eye
  height,width, _ =frame.shape
  mask=np.zeros((height,width),np.uint8)
  cv2.polylines(mask,[left_eye_region],True,255,2) #255, only 1 channel for white
  cv2.polylines(mask,[right_eye_region],True,255,2)
  cv2.fillPoly(mask,[left_eye_region],255) #fill the polygon with white
  cv2.fillPoly(mask,[right_eye_region],255)
  both_eye=cv2.bitwise_and(gray,gray,mask=mask)
        
       
        #to find min and max regions of eyes
  min_x=np.min(left_eye_region[:, 0])
  max_x=np.max(left_eye_region[:, 0])
  min_y=np.min(left_eye_region[:, 1])
  max_y=np.max(left_eye_region[:, 1])

  gray_eye = both_eye[min_y: max_y,min_x:max_x]
  gray_eye1 = cv2.GaussianBlur(gray_eye, (5, 5), 0)
  threshold_eye = cv2.adaptiveThreshold(gray_eye1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)


  height,width=threshold_eye.shape
  print('h',height)
  print('w',width)
  left_threshold=threshold_eye[0: height,0:int(width/2)]#to divide threshold bw left and right eye
  left_white=cv2.countNonZero(left_threshold)

  right_threshold=threshold_eye[0: height,int(width/2):width]
  right_white=cv2.countNonZero(right_threshold)
  
  if left_white==0:
      gaze_ratio=1
  elif right_white==0:
    gaze_ratio=5

  else:
    gaze_ratio=right_white/left_white
  return gaze_ratio

def midpoint(p1,p2):
    return int((p1.x + p2.x)/2),int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points,landmarks):
  left_point = (landmarks.part(eye_points[0]).x,landmarks.part(eye_points[0]).y)
  right_point = (landmarks.part(eye_points[3]).x,landmarks.part(eye_points[3]).y)                                
  center_top = midpoint(landmarks.part(eye_points[1]),landmarks.part(eye_points[2]))
  center_bottom = midpoint(landmarks.part(eye_points[5]),landmarks.part(eye_points[4]))     
  
  hor_line=cv2.line(frame,left_point,right_point,(0,255,0),2)
  ver_line=cv2.line(frame,center_top,center_bottom,(0,255,0),2)   

  hor_line_length=hypot((left_point[0]-right_point[0]),(left_point[1]-right_point[1]))      
  ver_line_length=hypot((center_top[0]-center_bottom[0]),(center_top[1]-center_bottom[1])) 
  ratio=hor_line_length/ver_line_length
  return ratio

def get_blink_count():
    global count
    cv2.putText(frame, str(count), (80, 80), font, 7, (0, 0, 255), 2)
    print((count))
    count = 0

schedule.every(10).seconds.do(get_blink_count)

while True:
    _, frame =cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    
    for face in faces:
        
        landmarks = predictor(gray,face)
        #gaze detection
        gr_left = get_gaze_ratio([36,37,38,39,40,41],landmarks)
        gr_right = get_gaze_ratio([42,43,44,45,46,47],landmarks)
        left_eye_ratio=get_blinking_ratio([36,37,38,39,40,41],landmarks)
        right_eye_ratio=get_blinking_ratio([42,43,44,45,46,47],landmarks)
        blink_ratio=((gr_left+gr_right)/2)
        print('blink',(blink_ratio*1.5))
        blink_ratio = (blink_ratio*1.5)
        if (left_eye_ratio  and right_eye_ratio) > 5.7:
                cv2.waitKey(300)
                cv2.putText(frame,"blinking",(50,450),font,2,(0,255,255),3)
                count=count+1
        if blink_ratio<=1.2:
            cv2.putText(frame,"LEFT",(50,100),font,2,(0,0,255),3)
            send_scroll_command(500, 1500, 200, 1500)  # Scroll left
        elif 1.2<blink_ratio<1.9 :
            cv2.putText(frame,"CENTER",(50,100),font,2,(0,0,255),3)
        elif blink_ratio>=1.9:
            cv2.putText(frame,"RIGHT",(50,100),font,2,(0,0,255),3) 
            send_scroll_command(200, 1500, 500, 1500)  # Scroll right
       
           
    cv2.imshow("output",frame)
    
    key=cv2.waitKey(1)
    if key ==27:
        break

cap.release()