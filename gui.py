import tkinter as tk
import head_tracker_dwell
import head_tracker_voice
import head_tracker_normal
import sys
import os
from threading import Thread


class dwellMode(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
    
    def run(self):
        head_tracker_dwell.main()

class voiceMode(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
    
    def run(self):
        head_tracker_voice.main()

class motionMode(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
    
    def run(self):
        head_tracker_normal.main()


def gui_main():

    root = tk.Tk()


    root.geometry("600x400")

    root.title("NosePoint Virtual Camera Mouse")

    def start_hover_mode():
        dwellMode()
        root.destroy()
        


    def start_voice_mode():
        voiceMode()
        root.destroy()
        

    def start_motion_mode():
        motionMode()
        root.destroy()
        


    def OptionMenu_CheckButton(event):
        if variable.get() == 'Hover Mode':
            lbl_explained['text'] = 'Hover Mode: Hover over a point of interest while keeping still for a second. This will initiate a click.'
            lbl_explained['text'] +='\nA small UI window will let you choose your preferred mouse function.'
            b1.configure(text = "Start", command=start_hover_mode)
        elif variable.get() == 'Voice Mode':
            lbl_explained['text'] = "Voice Mode: Control various mouse functions using your voice with Google Speech Recognition."
            lbl_explained['text'] +='\nRequires Internet Connection. A Headset Microphone is recommended.'
            lbl_explained['text'] +='\n'
            lbl_explained['text'] +='\nVoice Commands:'
            lbl_explained['text'] +="\nSay 'Left' for a left mouse click. Say 'Right' for a right mouse click."
            lbl_explained['text'] +="\nSay 'Scroll' for a middle mouse click which can be used for scrolling. Say 'Double' for a double left mouse click."
            lbl_explained['text'] +="\nSay 'Exit' to exit the application."
            b1.configure(text = "Start", command=start_voice_mode)
            

        elif variable.get() == 'Motion-only Mode':
            lbl_explained['text'] = 'Motion-only Mode: All Mouse functions are disabled. Mouse motion is enabled only.'
            lbl_explained['text'] +="\nThis is recommended for users that already have a foot controlled mouse or other assistive mouse peripherals,"
            lbl_explained['text'] +="\nor want to use this application with their preferred Speech Recognition software."
            b1.configure(text = "Start", command=start_motion_mode)
            




    lbl_mode = tk.Label(root, text="Mode:")

    lbl_mode.grid(row=1,column=0)  

    lbl_mode.place(relx=0.34, rely=0.2, anchor=tk.CENTER)

    variable = tk.StringVar(root)
    variable.set("Hover Mode") # default value

    options = ['Hover Mode','Voice Mode','Motion-only Mode']

    w = tk.OptionMenu(root, variable,  *(options), command =
    OptionMenu_CheckButton)

    w.grid(row=1,column=0)  

    w.place(relx=0.5, rely=0.2, anchor=tk.CENTER)


    b1 = tk.Button(text='Start',height=3,width=15,command=start_hover_mode)



    b1.grid(row=1,column=0)  

    b1.place(relx=0.5, rely=0.45, anchor=tk.CENTER)


    lbl_explained = tk.Label(root, text="")

    lbl_explained['text'] = 'Hover Mode: Hover over a point of interest while keeping still for a second. This will initiate a click.'
    lbl_explained['text'] +='\nA small UI window will let you choose your preferred mouse function.'

    lbl_explained.grid(row=1,column=0)  

    lbl_explained.place(relx=0.5, rely=0.7, anchor=tk.CENTER)



    root.mainloop()

if __name__ == '__main__':
    gui_main()