from tkinter import *
from time import time

PLAYER_WIDTH = 62
PLAYER_HEIGHT = 64
PLAYER_SPEED = 5

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700




class Application(Frame):
    def __init__(self, master):
        self.master = master
        self.master.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))#width x height
        self.master.title("Space Invaders")
        self.master.configure(background='black')
        self.master.resizable(False, False)

        self.Bullets = []
        self.PreviousBulletTime = 0
        
        self.Player = PhotoImage(file='Player1.png')
        self.PlayerLabel = Label(self.master, image=self.Player, borderwidth=0, highlightthickness=0)
        #self.PlayerLabel.place(relx=0, rely=1, x=300, anchor='s')
        self.PlayerLabel.place(x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT-PLAYER_HEIGHT)
        self.PlayerLabel.config(background="systemTransparent")
        self.master.bind('<Left>', self.LeftKeyPressed)
        self.master.bind('<Right>', self.RightKeyPressed)
        self.master.bind('<space>', self.SpaceKeyPressed)
        

    def LeftKeyPressed(self, event):
        print("Left")
        newPos = self.PlayerLabel.winfo_x()-PLAYER_SPEED
        if newPos >= 0:
            self.PlayerLabel.place(x=newPos)
            self.master.update()

    def RightKeyPressed(self, event):
        print("Right")
        newPos = self.PlayerLabel.winfo_x()+PLAYER_SPEED
        if newPos <= WINDOW_WIDTH - PLAYER_WIDTH:
            self.PlayerLabel.place(x=newPos)
            self.master.update()

    def SpaceKeyPressed(self, event):
        print("Space")
        #make a bullet appear first in front of the middle of the user sprite
        #then it travels upwards continuously
        current_time = time()
        if current_time - self.PreviousBulletTime >= 3:#bullets can only be launched every 3 seconds
            bullet = Bullet(self.PlayerLabel.winfo_x())
        
  

root = Tk()
app = Application(root)
root.mainloop()
