import cv2
import numpy as np
import dlib
from imutils.video import WebcamVideoStream
import imutils
from imutils import face_utils
import pyautogui
from optical_flow_tracker import Tracker
from threading import Thread
import os
from pydub import AudioSegment
from pydub.playback import play
import tkinter as tk
import sys
import gui


buttonClicked1 = False
buttonClicked2 = False
buttonClicked3 = False
buttonClicked4 = False




class clickSound(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    
    def run(self):
        sound = AudioSegment.from_wav("sounds/click.wav")
        play(sound)



class GUI(Thread):



    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    
    
    
    def run(self):
        root = tk.Tk()

        root.title("Mouse Helper")

        switch_frame = tk.Frame(root)
        switch_frame.pack()

        root.attributes('-topmost', True)
        root.update()
        root.attributes('-topmost', False)

        root.geometry("230x200")

        def left_click(event):
            global buttonClicked1
            global buttonClicked2
            global buttonClicked3
            global buttonClicked4

            buttonClicked1 = True
            buttonClicked2 = False
            buttonClicked3 = False
            buttonClicked4 = False

            event.widget.invoke()

    
        def right_click(event):
            global buttonClicked1
            global buttonClicked2
            global buttonClicked3
            global buttonClicked4

            buttonClicked1 = False
            buttonClicked2 = True
            buttonClicked3 = False
            buttonClicked4 = False
            event.widget.invoke()

        
        def middle_click(event):
            global buttonClicked1
            global buttonClicked2
            global buttonClicked3
            global buttonClicked4

            buttonClicked1 = False
            buttonClicked2 = False
            buttonClicked3 = True
            buttonClicked4 = False
            event.widget.invoke()
  
        
        def double_click(event):
            global buttonClicked1
            global buttonClicked2
            global buttonClicked3
            global buttonClicked4

            buttonClicked1 = False
            buttonClicked2 = False
            buttonClicked3 = False
            buttonClicked4 = True
            event.widget.invoke()


        
        switch_variable = tk.StringVar(value="off")

        

        b1 = tk.Radiobutton(switch_frame, text='Left Click',width=15,height=6,variable=switch_variable,indicatoron=False,value="low")
        b2 = tk.Radiobutton(switch_frame, text='Right Click',width=15,height=6,variable=switch_variable,indicatoron=False,value="medium")
        b3 = tk.Radiobutton(switch_frame, text='Double Click',width=15,height=6,variable=switch_variable,indicatoron=False,value="high")
        b4 = tk.Radiobutton(switch_frame, text='Middle Click',width=15,height=6,variable=switch_variable,indicatoron=False)


        b1.bind("<Button>", left_click)
        b2.bind("<Button>", right_click)
        b3.bind("<Button>", double_click)
        b4.bind("<Button>", middle_click)



        b1.grid(column=0, row=0)   
        b2.grid(column=1, row=0)   
        b3.grid(column=0, row=1)   
        b4.grid(column=1, row=1)  

        root.call('wm', 'attributes', '.', '-topmost', '1')
        root.mainloop()





def ref2dImagePoints(shape):
    # The 2D Model Points of the:
    imagePoints = [[shape.part(27).x, shape.part(27).y]]   # Nose tip
                    
    return np.array(imagePoints, dtype=np.float64)  



#Define Path of the Model
face_landmark_path = 'model/shape_predictor_68_face_landmarks.dat'




def main():

    
    #Different Thread for Capturing Frames, better performance

    FRAME_COUNTER = 0 
    val_x= 0 
    val_y = 0

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

    GUI()

    
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

                pyautogui.moveTo(curr_loc_X,curr_loc_Y)

                #print(abs(curr_loc_Y - prev_loc_Y))


                global buttonClicked1
                global buttonClicked2
                global buttonClicked3
                global buttonClicked4

                if  0 <= (abs(curr_loc_X  - prev_loc_X)) <=0.5:
                    if  0 <= (abs(curr_loc_Y  - prev_loc_Y)) <=0.5:
                        #print('AAAA')
                        smoothing = 5
                        
                        FRAME_COUNTER+=1
                        if val_x != curr_loc_X and val_y!= curr_loc_Y:
                            if FRAME_COUNTER ==10: 
                                clickSound()
                                if buttonClicked1 is True:
                                    pyautogui.click(button='left')
                                elif buttonClicked2 is True:
                                    pyautogui.click(button='right')
                                elif buttonClicked3 is True:
                                    pyautogui.click(button='middle')
                                elif buttonClicked4 is True:
                                    pyautogui.doubleClick()
                                else:
                                    pyautogui.click(button='left')
                                
                else:
                    smoothing = 2
                    FRAME_COUNTER = 0
                    val_x,val_y = pyautogui.position()



            
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