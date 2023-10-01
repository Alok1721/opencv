import cv2
import numpy as np

cap=cv2.VideoCapture("eye_recording.flv")

while True:
    ret,frame=cap.read()
    roi=frame[309:795,637:1416]
    gray_roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY )
    gray_roi=cv2.GaussianBlur(gray_roi,(7,7),0)
    rows,cols,_=roi.shape

    _, threshold=cv2.threshold(gray_roi,2,255,cv2.THRESH_BINARY_INV)
    contours,_=cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
    
    for cnt in contours:
        (x,y,w,h)=cv2.boundingRect(cnt)
        cv2.rectangle(roi,(x,y),(x+w,y+h),(255,0,0),3)
        cv2.line(roi,(x+int(w/2),0),(x+int(w/2),rows),(0,255,0),2)
        cv2.line(roi,(0,y+int(h/2)),(cols,y+int(h/2)),(0,255,0),2)
        #cv2.drawContours(roi,[cnt],-1,(0,255,0),2)
        break

    cv2.imshow("threshold",threshold)

    cv2.imshow("ROI",roi)
    cv2.imshow("GRAY_ROI",gray_roi)
    key=cv2.waitKey(30)
    if key==27:
        break
cv2.destroyAllWindows()
