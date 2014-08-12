import numpy as np

import cv2
import cv2.cv as cv

cap = cv2.VideoCapture(1)
cap.set(3,352)
cap.set(4,288)

th = 100
p = 13
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # th = th - 1

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # (thresh, img_bw) = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    (thresh, img_bw) = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY )

    circles = cv2.HoughCircles(img_bw, cv.CV_HOUGH_GRADIENT, 1, 10, param1=p, param2=p, minRadius=10, maxRadius=80)
    x_center = 0
    y_center = 0

    if circles != None:
        circles = np.around(circles.astype(np.int),0)


        for i in circles[0,:]:
            x_center += i[0]
            y_center += i[1]
            cv2.circle(img_bw,(i[0],i[1]),i[2],(0,255,0),2)


        x_center = int(x_center / len(circles[0,:]))
        y_center = int(y_center / len(circles[0,:]))
        # cv2.circle(frame,(x_center,y_center),2,(0,255,255),3)

    cv2.imshow('gray', img_bw)
    contours, hierarchy = cv2.findContours(img_bw, 1, 2)
    
    cx = 0
    cy = 0

    eye_counter_found = False

    for contour in contours:
        P = cv2.arcLength(contour, True)
        S = cv2.contourArea(contour)
        if  50000 > S > 2000:
            eye_counter_found = True
            # cv2.drawContours(frame, contour, -1, (0,255,0), 3)
            M = cv2.moments(contour)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # cv2.circle(frame,(cx,cy), 2, (0,0,255), 3) 
    
    if not eye_counter_found:
        print("Eye counter not found :(")

    if x_center == 0 and y_center == 0:
        x_center = cx
        y_center = cy

    medium_x = (cx + x_center)/2
    medium_y = (cy + y_center)/2
    cv2.circle(frame,(medium_x,medium_y), 2, (0,128,128), 3)

    # print(medium_x)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    # cv2.imshow('gray', img_bw)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()