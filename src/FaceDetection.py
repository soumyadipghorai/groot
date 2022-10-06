import cv2 
import pathlib
import numpy as np 

cascPath = "/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml"
# eyePath = "/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml"
# smilePath = "/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_smile.xml"


# faceCascade = cv2.CascadeClassifier(cascPath)
# eyeCascade = cv2.CascadeClassifier(eyePath)
# smileCascade = cv2.CascadeClassifier(smilePath)


clf = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# eyeCascade = cv2.CascadeClassifier(eyePath)
# smileCascade = cv2.CascadeClassifier(smilePath)

camera = cv2.VideoCapture(0)

while True : 
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    
    faces = clf.detectMultiScale(
        gray, 
        scaleFactor = 1.1, 
        minNeighbors = 5, 
        minSize = (30, 30), 
        flags = cv2.CASCADE_SCALE_IMAGE
    )       

    num = 0 
    for face in faces : 
        x, y, hi, wi = face

        cv2.rectangle(frame, (x, y), (x+hi, y+wi), (255, 255, 0), 2)
        num += 1 

        cv2.putText(frame, 'face'+str(num), (x-12, y-12), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if len(faces) > 1 : 
            cv2.putText(frame, 'More than 1 face detected',(x-32, y-32),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
    cv2.imshow("Faces", frame)

    if cv2.waitKey(1) == ord("q") : 
        break 

camera.release()
cv2.destroyAllWindows()

