from tkinter import *
import random

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BOTTOM_PADDING = 20
TOP_PADDING = 50
X_PADDING = 50

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 20
PLAYER_SPEED = 15

BRICK_HEIGHT = 20

class OneP(object):
    def __init__(self, master):
        self.master = master
        self.master.title("Brick Breaker - One Player")
        self.canvas = Canvas(self.master,
                             cursor='none',
                             width=WINDOW_WIDTH,
                             height=WINDOW_HEIGHT,
                             highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='#006666')
        
        self.Player = self.canvas.create_rectangle(0.45*WINDOW_WIDTH,
                                                   WINDOW_HEIGHT - PLAYER_HEIGHT - BOTTOM_PADDING,
                                                   0.55*WINDOW_WIDTH,
                                                   WINDOW_HEIGHT - BOTTOM_PADDING,
                                                   width=0, fill='blue')

        self.master.bind("<Left>", self.LeftKeyPressed)
        self.master.bind("<Right>", self.RightKeyPressed)

        self.Bricks = []
        self.ProduceBricks(3, 5)

    def ProduceBricks(self, rows, cols):
        colours = ['#dc3020', '#f09336', '#fffd55', '#2e74f6', '#eb42f7', '#74f94c']
        colourIndex = random.randint(0, len(colours) - 1)
        self.Brick_Width = (WINDOW_WIDTH - X_PADDING*2) // cols
        for r in range(0, rows):
            row = []
            startY = TOP_PADDING + (r * BRICK_HEIGHT)
            endY = startY + BRICK_HEIGHT
            for c in range(cols):
                brickColour = colours[colourIndex]
                colourIndex = colourIndex + 1 if colourIndex < len(colours) - 1 else 0
                startX = (X_PADDING) + (c * self.Brick_Width)
                endX = startX + self.Brick_Width
                brick = self.canvas.create_rectangle(startX, startY,
                                                     endX, endY,
                                                     fill=brickColour)
                row.append(brick)
            self.Bricks.append(row)

    def LeftKeyPressed(self):
        print("Left Key Pressed")

    def RightKeyPressed(self):
        print("Right Key Pressed")

        

def run():
    root = Tk()
    WINDOW_WIDTH = root.winfo_screenwidth()
    WINDOW_HEIGHT = root.winfo_screenheight()
    app = OneP(root)
    root.mainloop()

run()
