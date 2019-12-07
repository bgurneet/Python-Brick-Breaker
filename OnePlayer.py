from tkinter import *
import random

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BOTTOM_PADDING = 20
TOP_PADDING = 50
X_PADDING = 20


PLAYER_WIDTH = 60
PLAYER_HEIGHT = 20
PLAYER_SPEED = 10

BRICK_WIDTH = 60
BRICK_HEIGHT = 20

BALL_SPEED = 5


class OneP(object):
    def __init__(self, master):
        self.master = master
        self.master.title("Brick Breaker - One Player")
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master,
                             cursor='none',
                             width=WINDOW_WIDTH,
                             height=WINDOW_HEIGHT,
                             highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='#006666')

        #make player
        window_centerX = WINDOW_WIDTH/2
        window_centerY = WINDOW_HEIGHT/2
        player_centerX = PLAYER_WIDTH/2
        player_centerY = PLAYER_HEIGHT/2
        self.Player = self.canvas.create_rectangle(0.45*WINDOW_WIDTH,
                                                   WINDOW_HEIGHT - PLAYER_HEIGHT - BOTTOM_PADDING,
                                                   0.55*WINDOW_WIDTH,
                                                   WINDOW_HEIGHT - BOTTOM_PADDING,
                                                   width=0, fill='blue')
        self.master.bind("<Left>", self.LeftKeyPressed)
        self.master.bind("<Right>", self.RightKeyPressed)
        
        self.Bricks = []
        self.ProduceBricks(10)

        #make a ball in the center of the screen
        self.Ball = self.DrawCircle(window_centerX, window_centerY, 15, '#99ff99')
        self.BallXDir = 1 #random.choice([-1, 0, 1])
        self.BallYDir = 0

        #make label instructing user how to start game
        '''self.start_label = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 60 bold italic',
                                 background='#006666',
                                 anchor=N,
                                 text="Press Spacebar to Start Game")
        self.start_label.place(relx=0.5, rely=0.55, anchor=CENTER)'''
        self.start_msg = self.canvas.create_text((window_centerX, window_centerY + 100),
                                                 text="Press Spacebar to Start Game",
                                                 font="Helvetica 50 bold italic")

        self.GamePlaying = False
        #start the game when the user first presses space
        self.master.bind('<space>', self.StartGame)
        self.master.after(1, self.BallMovement)
        print("HEREEEEEEEEEEEEEEE")

    def BallMovement(self):
        if self.GamePlaying:
            ballPos = self.canvas.coords(self.Ball)
            print(ballPos)
            #detect collisions with left, right and top walls respectively
            newPosX = self.BallXDir * BALL_SPEED
            newPosY = self.BallYDir * BALL_SPEED
            if ballPos[2] > WINDOW_WIDTH or ballPos[0] < 0:
                print("HERE")
                newPosX *= -1 #change the direction
            elif ballPos[1] < 0 or ballPos[3] > WINDOW_HEIGHT:
                newPosY *= -1
            print(newPosX, newPosY)
            self.canvas.move(self.Ball, newPosX, newPosY)
            
        self.master.after(1, self.BallMovement)

    def StartGame(self, event):
        if not self.GamePlaying:
            self.GamePlaying = True
            self.canvas.delete(self.start_msg)
        else:
            self.GamePlaying = False
            self.start_msg = self.canvas.create_text((WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 100),
                                                 text="Press Spacebar to Start Game",
                                                 font="Helvetica 50 bold italic")
            

    def DrawCircle(self, x, y, radius, colour):
        return self.canvas.create_oval(x - radius, y - radius,
                                       x + radius, y + radius,
                                       width=0, fill=colour)

    def ProduceBrick(self, colour, x1, y1, x2, y2):
        brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colour)
        return brick

    def ProduceBricks(self, rows):
        colours = ['#dc3020', '#f09336', '#fffd55', '#2e74f6', '#eb42f7', '#74f94c']
        #colourIndex = random.randint(0, len(colours) - 1)
        colourIndex = 5
        currentY = TOP_PADDING
        while True:
            #rowColour = random.choice(colours)
            #print(currentY + BRICK_HEIGHT)
            currentX = TOP_PADDING
            currentEndY = currentY + BRICK_HEIGHT
            if currentEndY > TOP_PADDING + (rows * BRICK_HEIGHT):
                break
            while True:
                brickColour = colours[colourIndex]
                colourIndex = colourIndex + 1 if colourIndex < len(colours) - 1 else 0
                currentEndX = currentX + BRICK_WIDTH
                if currentEndX <= WINDOW_WIDTH - X_PADDING:
                    brick = self.ProduceBrick(brickColour, currentX, currentY,
                                              currentEndX, currentEndY)
                    self.Bricks.append(brick)
                    currentX = currentEndX
                else:
                    currentY = currentEndY
                    break

    def LeftKeyPressed(self, event):
        playerPos = self.canvas.coords(self.Player)
        newPosX = playerPos[0] - PLAYER_SPEED
        if newPosX >= 0:
            self.canvas.move(self.Player, -PLAYER_SPEED, 0)
        print(playerPos)

    def RightKeyPressed(self, event):
        playerPos = self.canvas.coords(self.Player)
        newPosX = playerPos[0] + 1
        if newPosX <= WINDOW_WIDTH:
            self.canvas.move(self.Player, PLAYER_SPEED, 0)
        

def run():
    root = Tk()
    app = OneP(root)
    root.mainloop()
run()
