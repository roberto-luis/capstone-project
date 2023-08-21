import cv2
import numpy as np

        
def detect_dataMatrix(img):
    found = False
    #Turn image into grayscale,blur image to smooth,apply threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(11,11),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,4)
    
    #Perform morphology to remove smaller black dots in image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    closed = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel,iterations=2)
        
    
    #find contours
    cnts = cv2.findContours(closed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    
    for cnt in cnts:
        epsilon = 0.05*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        area = cv2.contourArea(approx)
        x,y,w,h = cv2.boundingRect(approx)
        if w > (h-5) and w < (h+5) and area > 5000:
            #cv2.rectangle(img, (x,y),(x+w,y+h),(36,255,12),2)
            if y > 5 and x > 5:
                ROI = img[y-5:y+h+5,x-5:x+w+5]
                cv2.imwrite('datamatrix.jpg',ROI)
                found = True
    
    return found
    
    
    
    