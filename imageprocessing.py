import serial
import cv2
import numpy as np

def area(x1, y1, x2, y2, x3, y3): 
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def isInside(A,x1, y1, x2, y2, x3, y3, x4, y4, x, y):   
    A1 = area (x, y, x2, y2, x3, y3) 
    A2 = area (x1, y1, x, y, x4, y4) 
    A3 = area (x1, y1, x2, y2, x, y)
    A4 = area (x3, y3, x4, y4, x, y)
    if(A == A1 + A2 + A3+ A4):
        return True
    else: 
       return False
   
s=''
   
status=""
oldStatus=""

top=[[0,0],[450,0],[450,300],[0,300]]
left=[[0,300],[450,300],[450,600],[0,600]]
right=[[450,300],[900,300],[900,600],[450,600]]
bottom=[[450,0],[900,0],[900,300],[450,300]]

cap = cv2.VideoCapture(0)
ser = serial.Serial("COM7", '9600', timeout=2)

position = 0

green_lower = (29, 86, 6)
green_upper = (64, 255, 255)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (900, 600))
    blurred=cv2.GaussianBlur(frame,(11,11),0)
    
    cv2.line(frame,(0,300),(900,300),(255,255,255),2)
    cv2.line(frame,(450,0),(450,600),(255,255,255),2)
    
    cv2.putText(frame, "90 degree", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.putText(frame, "270 degree", (500,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.putText(frame, "0 degree", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.putText(frame, "180 degree", (500, 350), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, green_lower, green_upper)
    mask = cv2.erode(mask,None,iterations=2)
    mask = cv2.dilate(mask,None,iterations=2)
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
    cv2.drawContours(frame,contours,-1,(88,188, 88),3)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        radius=int((w/2+h/2)/2)
        
        
        medium_x = int(x+(w/2))
        medium_y = int(y +(h/2))
        
        text2 = ".X  = " + str(medium_x)
        cv2.putText(frame, text2, (medium_x,medium_y ), cv2.FONT_HERSHEY_SIMPLEX, 1, (88, 188, 255),2)
        
        
        text3 = ".Y  = " + str(medium_y)
        cv2.putText(frame, text3, (medium_x,medium_y+30 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (88,188, 255),2)
        
        oldStatus=status

        
        if isInside(450*300,top[0][0],top[0][1],top[1][0],top[1][1],top[2][0],top[2][1],top[3][0],top[3][1],medium_x,medium_y):
            status="top"
            position=90
            s='a'
        elif isInside(450*300,left[0][0],left[0][1],left[1][0],left[1][1],left[2][0],left[2][1],left[3][0],left[3][1],medium_x,medium_y):
            status="left"
            position=180
            s='a'
        elif isInside(450*300,bottom[0][0],bottom[0][1],bottom[1][0],bottom[1][1],bottom[2][0],bottom[2][1],bottom[3][0],bottom[3][1],medium_x,medium_y):
            status="bottom"
            position=180
            s='b'
        elif isInside(450*300,right[0][0],right[0][1],right[1][0],right[1][1],right[2][0],right[2][1],right[3][0],right[3][1],medium_x,medium_y):
            status="right"
            position=0
            s='a'
        if oldStatus!=status:
            print(status)
        cv2.putText(frame,status , (medium_x,medium_y+50 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,100, 100),2)
        ser.write((str(position) + s).encode('utf-8'))

        break


    cv2.imshow("frame",frame)
    key = cv2.waitKey(1)
    if key ==27:
        break
cap.release()
cv2.destroyAllWindows()






