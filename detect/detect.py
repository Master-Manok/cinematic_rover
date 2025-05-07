import numpy as np
import cv2 as cv
center_color=(0,0,255)
face_center_color=(0, 255, 255)

path = r"/home/manoj/VScodes/cinematic_rover/detect/haarcascade_frontalface_default.xml"
face_cascade = cv.CascadeClassifier(path)

def draw(frame,para1,para2):
    global center_color, face_center_color
    (x,y,w,h)= para1
    cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
    cv.circle(frame, (int(x+w/2), int(y+h/2)), 1, face_center_color, -1)
    cv.circle(frame, para2, 1, center_color, -1)

def loc_face(frame,frame_width,frame_height):
    global face_cascade
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.10, minNeighbors=6, minSize=(50,50))
    if len(faces)>1:
        print("More faces detected!")
        #print(faces)
        return (0,0)
    elif len(faces)==1:
        parameters= faces[0] #(x,y,w,h)
        loc_x= parameters[0] + parameters[2]/2
        loc_y= parameters[1] + parameters[3]/2
        diff_x= frame_width/2 - loc_x
        diff_y= frame_height/2 - loc_y
        draw(frame,parameters,(int(frame_width/2),int(frame_height/2)))
        return (diff_x,diff_y)
    else:
        print("No face detected!")
        return (0,0)
    #
    #for f in faces:
    #    draw(frame,f,(int(frame_width/2),int(frame_height/2)))