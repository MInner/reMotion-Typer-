import numpy as np
import cv2

def is_nod(prev):
    diff=prev[len(prev)-1]-prev[0]
    if diff>16:
        return 1
    else:
        return 0


def nod_detection():
    face_cascade=cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    cap=cv2.VideoCapture(0)
    #inicial params
    #timer - how many shots left to enable nod detection
    #prev - list of 5 previous y-axes for the actual one 
    timer=0
    prev=[0]*5
    while(cap.isOpened()):
        #ret-if camera is opened, img - photo
        ret,img=cap.read()
        if (not ret):
                continue
        else:
            #detecting faces
            gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces=face_cascade.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5,minSize=(60, 60))    
            
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                #renew previous photo list
                el=prev.pop(0)
                prev.append(y)
                #case of nod detection denial
                if timer:
                    timer=timer-1
                    nod=0
                else:
                    nod=is_nod(prev)
                    if nod:
                        print 'BINGO'
                        #renew the timer
                        timer=15
            
            #enable if need to watch video stream           
            cv2.imshow('frame', img)
        #press 'q' for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #stopping strem    
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    nod_detection()    
    