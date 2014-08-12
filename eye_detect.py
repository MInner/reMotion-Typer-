from __future__ import print_function

import numpy as np
import cv2
import cv2.cv as cv
import threading

x = 0
y = 0

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

th = 0

black_perc = 10

def change_th(x):
    global th
    th = x

def change_black_perc(x):
    global black_perc
    black_perc = x

eye_counter_found = False

wsize = 3
window_x = [0]*wsize
window_y = [0]*wsize

def run():
    global th, x, y, eye_counter_found, black_perc
    
    cap = cv2.VideoCapture(0)
    cap.set(3,352)
    cap.set(4,288)

    th = 46
    p = 13

    cv2.namedWindow('tools', flags = 0)
    cv2.createTrackbar('threshold','tools',10, 100, change_th)
    cv2.setTrackbarPos('threshold', 'tools', th)
    cv2.createTrackbar('black_perc', 'tools', 5, 95, change_black_perc)
    cv2.setTrackbarPos('black_perc', 'tools', black_perc)

    notfoundcounter = 20
    cascade_conunter = 0

    (ex,ey,ew,eh) = (0, 0, 0, 0)

    while True:
        ret, img = cap.read()
        if not ret:
            print("No img on input :(")
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if not ret:
            continue

        frames_until_reset = 20

        if not eye_counter_found:
            notfoundcounter += 1
            if notfoundcounter > frames_until_reset:
                eyes = eye_cascade.detectMultiScale(gray)
                if len(eyes) != 2:
                    continue

                eyes = sorted(eyes, key = lambda x: x[0])
                (ex,ey,ew,eh) = eyes[0]
                notfoundcounter = 0
        else:
            notfoundcounter = 0

        cascade_conunter += 1

        newsize = (200, 100)

        eye = gray[ey+eh/3 : ey+ 3*eh/4, ex : ex+ew]
        eye = cv2.resize(eye, newsize)
        eye = cv2.GaussianBlur(eye,(5,5),0)

        (thresh, img_bw) = cv2.threshold(eye, th, 255, cv2.THRESH_BINARY )
        cv2.rectangle(img_bw, (0, 0), newsize, (255, 255, 255), 3)
        cv2.imshow('bw', img_bw)

        circles = cv2.HoughCircles(img_bw, cv.CV_HOUGH_GRADIENT, 1, 10, param1=p, param2=p, minRadius=0, maxRadius=0)
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

        contours, hierarchy = cv2.findContours(img_bw, 1, 2)
        
        cx = 0
        cy = 0

        eye_counter_found = False

        if len(contours) == 1:
            M = cv2.moments(contours[0])
            cx = int(M['m10']/ (M['m00'] + 0.0001) )
            cy = int(M['m01']/ (M['m00'] + 0.0001) )
        else:
            contours = sorted(contours, key = lambda x: cv2.contourArea(x), reverse=True)
            for contour in contours:
                S = cv2.contourArea(contour)
                fullarea = newsize[0]*newsize[1]
                if fullarea*(black_perc+10)/100 > S > fullarea*(black_perc-5)/100:
                    # print(S)
                    eye_counter_found = True
                    # cv2.drawContours(frame, contour, -1, (0,255,0), 3)
                    M = cv2.moments(contour)
                    cx = int(M['m10']/(M['m00'] + 0.0001))
                    cy = int(M['m01']/(M['m00'] + 0.0001))
                    # cv2.circle(frame,(cx,cy), 2, (0,0,255), 3)
        
        if x_center == 0 and y_center == 0:
            x_center = cx
            y_center = cy

        x = (cx + x_center)/2
        y = (cy + y_center)/2

        window_x.pop(0)
        window_x.append(x)
        window_y.pop(0)
        window_y.append(y)

        x = int(np.median(window_x))
        y = int(np.median(window_y))

        cv2.circle(eye,(x,y), 2, (255,255,255), 1)
        cv2.imshow('eye_grey', eye)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
cv2.destroyAllWindows()

def start_thread():
    t = threading.Thread(target = run)
    t.start()

if __name__ == '__main__':
    start_thread()