'''from tkinter import *
import random

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

GAME_GROUND_HEIGHT = 600
        

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

    def RenderTank(self, position):
        #a tank is defined as a 

    def RenderGameScene(self):
        screen_center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        #create a rectangle from the bottom of the screen
        self.canvas.create_rectangle(0, GAME_GROUND_HEIGHT,
                                     WINDOW_WIDTH, WINDOW_HEIGHT,
                                     outline='green', fill='green')
        #create a triangle in the middle of the screen (on top of the rect)
        triangle_points = [screen_center[0], screen_center[1],
                           screen_center[0]/2, GAME_GROUND_HEIGHT,
                           3*screen_center[0]/2, GAME_GROUND_HEIGHT]
        self.canvas.create_polygon(triangle_points, outline='green', fill='green', width=0)
        

class Tank(Application):
    def __init__(self, AI=False):
        self.AI = AI

root = Tk()
app = Application(root)
root.mainloop()'''

from tkinter import *

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

GAME_GROUND_HEIGHT = 600

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
        #self.canvas.configure(background='#e6e6e6')

        #self.RenderGameScene()

        #self.Tanks = []

        self.PlayerImage = PhotoImage(file='PlayerState0.png')
        self.Player = self.canvas.create_image(WINDOW_WIDTH/2,
                                 100,
                                 image=self.PlayerImage)
        
        self.master.bind('<Left>', self.LeftKeyPressed)
        self.master.bind('<Right>', self.RightKeyPressed)
        self.master.bind('<Up>', self.LeftKeyPressed)
        self.master.bind('<Down>', self.RightKeyPressed)
        self.master.bind('<space>', self.SpaceKeyPressed)
        #self.Tanks.append(self.Player)

    def MoveTank(self, direction):
        print(direction)

    def LeftKeyPressed(self, event):
        self.MoveTank("Left")

    def RightKeyPressed(self, event):
        self.MoveTank("Right")

    def UpKeyPressed(self, event):
        self.MoveTank("Up")

    def DownKeyPressed(self, event):
        self.MoveTank("Down")

    def SpaceKeyPressed(self, event):
        self.MoveTank("Space")
        
        

    def RenderGameScene(self):
        pass
        

class Tank():
    def __init__(self, current_state=0, ai=False):
        self.image = PhotoImage()
        self.ai = ai
        self.current_state = current_state



root = Tk()
app = Application(root)
root.mainloop()
