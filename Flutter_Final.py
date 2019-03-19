import cv2
import numpy as np
import math
cap=cv2.VideoCapture('054A9898.mov')
fps = cap.get(cv2.CAP_PROP_FPS)
print cap.get(3)
print cap.get(4)
print(fps)
arc,maxAngle1,maxAngle2=0.0,0.0,0.0 # To store the sum of the distances both above and below the mean position
font = cv2.FONT_HERSHEY_SIMPLEX
c,d,f=0,0,0
while True:
    ret, frame=cap.read()
    if ret == True:
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_red=np.array([160,87,111])
        upper_red=np.array([180,255,255])
        kernel=np.ones((5,5),"uint8")
        red=cv2.inRange(hsv,lower_red,upper_red)
        red=cv2.dilate(red,kernel)
        ret,contours,hierarchy=cv2.findContours(red,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#finding contours in the red image which has only the red objects thresholded
        for contour in contours:# hence making it cumpolsury to find contours of only red objects
            if len(contour)>50:
                M=cv2.moments(contour)
                c+=1
                cx,cy = int(M['m10']/M['m00']),int(M['m01']/M['m00'])
                frame=cv2.line(frame,(cx,cy),(0,360),(0,255,0),3) # drawing the line between the mid point of the frame and centre of the contour
                angle=round((math.atan2(360-cy,cx-0)), 2)#calculating the angle between the line joining the centre of contour and left cnetre of image w.r.t horizontal.
                cv2.putText(frame,str(angle),(cx/2,cy/2),font,2,(0,0,255),2,cv2.LINE_AA)
                if angle>0 and d%2!= 0: # Since atan2 has its range from -180 to 180, it gives the angles below the horizontal in negative. This can be used as a condition to check
                    if(angle>maxAngle1):
                        maxAngle1=angle
                    else:
                        d=d+1
                        f+=0.25
                        arc=arc+2*(15*float(maxAngle1))
                        print(maxAngle1)
                        break
                    maxAngle2=0
                elif angle<0 and d%2 == 0:
                    angle= -1*angle # when the point is below the horizonntal
                    if(angle>maxAngle2):
                        maxAngle2=angle
                    else:
                        f+=0.25
                        d+=1
                        arc = arc+ 2*(15*float(maxAngle2))
                        print(-1*maxAngle2)
                        break
                    maxAngle1=0
        cv2.imshow('Angle',frame)
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break
print("Oscillations per sec= " + str(f/(c/fps)))
print(arc/(c/fps))
cap.release()
cv2.destroyAllWindows()

