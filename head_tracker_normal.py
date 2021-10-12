import os
import cv2
import numpy as np
import dlib
from imutils.video import WebcamVideoStream
import imutils
from imutils import face_utils
import pyautogui
from optical_flow_tracker import Tracker
import gui
import sys
from threading import Thread


class startGUI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
    
    def run(self):
        gui.gui_main()


def ref2dImagePoints(shape):
    # The 2D Model Points of the:
    imagePoints = [[shape.part(27).x, shape.part(27).y]]   # Nose tip
                    
    return np.array(imagePoints, dtype=np.float64)  



#Define Path of the Model
face_landmark_path = 'model/shape_predictor_68_face_landmarks.dat'




def main():
    #Different Thread for Capturing Frames, better performance



    cam_w = 420
    cam_h = 200

    smoothing = 2

    prev_loc_X,prev_loc_Y = 0,0 
    curr_loc_X,curr_loc_Y = 0,0


    pyautogui.FAILSAFE = False

    pyautogui.PAUSE = False

    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

    pyautogui.moveTo(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    cap = WebcamVideoStream(src=0).start() 
    
    #Dlib Face Detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_path)

    tracker = Tracker()

    prev_gray = cap.read()


    while True:
        
        # Read Image
        im = cap.read()
        
        

        im = cv2.flip(im, 1)

        #Resizing the frame to a smaller resolution drastically improves perfomance
        im = imutils.resize(im, width=cam_w, height=cam_h)

        #Sending Grayscale frames improves perfomance (Face Detection does not require color)
        frame_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        face_rects = detector(frame_gray,0)


        if len(face_rects) > 0:


            for face in face_rects:
                (x,y,w,h) = face_utils.rect_to_bb(face)
            
       

            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #Update tracks.
            if len(tracker.tracks) > 0:
                tracker.update_tracks(prev_gray, frame_gray,face_rectangle)
            
            # Get new tracks every detect_interval frames.
            target_box = [100, 400, 100, 400]

            shape = predictor(im, face_rects[0])

            refImgPts = ref2dImagePoints(shape)

           
    
            
            tracker.get_new_tracks(refImgPts[0][0],refImgPts[0][1])
            

            face_rectangle = (x,y,w,h)

            
            
            if len(tracker.tracks) > 0:
                for p in tracker.tracks[0]:

                    xcoord = p[0]
                    ycoord = p[1]

                cv2.circle(im, (int(xcoord), int(ycoord)), 0, (0,0,255), 5)


                xcoord = np.interp(xcoord+16,(160,cam_w-160),(0,SCREEN_WIDTH))

                ycoord = np.interp(ycoord-40,(80,cam_h-80),(0,SCREEN_HEIGHT))

               
                curr_loc_X = prev_loc_X + (xcoord - prev_loc_X) / smoothing

                curr_loc_Y = prev_loc_Y + (ycoord - prev_loc_Y) / smoothing


                #print(abs(curr_loc_Y - prev_loc_Y))

                pyautogui.moveTo(curr_loc_X,curr_loc_Y)



                if  0 <= (abs(curr_loc_X  - prev_loc_X)) <=0.5:
                    if  0 <= (abs(curr_loc_Y  - prev_loc_Y)) <=0.5:
                        #print('AAAA')
                        smoothing = 5
                else:
                    smoothing = 2

            
                

            prev_loc_X,prev_loc_Y = curr_loc_X,curr_loc_Y


            
            prev_gray = frame_gray

        else:       
            print("No Face found")

           
        cv2.imshow('Output', im)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.stop()
            break

if __name__ == '__main__':
    main()