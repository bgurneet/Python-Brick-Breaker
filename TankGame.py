from tkinter import *
import random

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
        

class Application(object):
    def __init__(self, master):
        self.master = master
        self.master.title("Tank Destructors")
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master,
                             width=WINDOW_WIDTH,
                             height=WINDOW_HEIGHT,
                             highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='blue')

        self.RenderGameScene()

    def RenderGameScene(self):
        screen_center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        #create a rectangle from the bottom of the screen
        self.canvas.create_rectangle(0, 600,
                                     WINDOW_WIDTH, WINDOW_HEIGHT,
                                     outline='green', fill='green')
        #create a triangle in the middle of the screen (on top of the rect)
        triangle_points = [screen_center[0], screen_center[1],
                           screen_center[0]/2, 600,
                           3*screen_center[0]/2, 600]
        self.canvas.create_polygon(triangle_points, outline='green', fill='green', width=0)
        

class Tank(Application):
    def __init__(self, AI=False):
        self.AI = AI

root = Tk()
app = Application(root)
root.mainloop()
