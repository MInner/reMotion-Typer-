import cv2
import cv2.cv as cv
import numpy as np
import time

cap = cv2.VideoCapture(0)
good_i = 0

while(True):
    okay, frame = cap.read()
    time.sleep(5)
    cv2.imshow('frmae', frame)

    if okay:
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

        if good_i == 0:
            for i in range(30, 80):
                print(i)
                circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 1, 100, param1=i, param2=i,minRadius=0,maxRadius=0)

                try:
                    circles = np.around(circles)
                except:
                    break

                if len(circles[0,:]) == 1:
                    print(len(circles[0,:]))
                    for j in circles[0,:]:
                        # draw the outer circle
                        cv2.circle(cimg,(j[0],j[1]),j[2],(0,255,0),2)
                        # draw the center of the circle
                        cv2.circle(cimg,(j[0],j[1]),2,(0,0,255),3)
                    good_i = i

                cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
            else:
                circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 1, 100, param1=good_i, param2=good_i,minRadius=0,maxRadius=0)
                circles = np.around(circles)
                for j in circles[0,:]:
                    # draw the outer circle
                    cv2.circle(cimg,(j[0],j[1]),j[2],(0,255,0),2)
                    # draw the center of the circle
                    cv2.circle(cimg,(j[0],j[1]),2,(0,0,255),3)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



cv2.destroyAllWindows()