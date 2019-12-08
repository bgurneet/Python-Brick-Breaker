from tkinter import *
import random
from time import time, sleep

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BOTTOM_PADDING = 20
TOP_PADDING = 50
X_PADDING = 40


PLAYER_WIDTH = 60
PLAYER_HEIGHT = 20
PLAYER_SPEED = 15

BRICK_WIDTH = 100
BRICK_HEIGHT = 20

BALL_SPEED = 2


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
        self.Level = 1
        self.ProduceBricks(self.Level * 2)
    
        #make a ball in the center of the screen
        self.Ball = self.DrawCircle(window_centerX, window_centerY, 15, '#99ff99')
        self.BallXDir = random.choice([-1, 1])
        self.BallYDir = 1

        #make label instructing user how to start game
        self.start_msg = self.canvas.create_text((window_centerX, window_centerY + 100),
                                                 text="Press Spacebar to Start Game",
                                                 font="Helvetica 50 bold italic")

        self.GamePlaying = False
        self.GameOver = False
        #start the game when the user first presses space
        self.master.bind('<space>', self.StartGame)
        self.master.after(1, self.BallMovement)

        self.score_prefix_label = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 20 italic',
                                 background='#006666',
                                 text='SCORE: ')
        self.score_prefix_label.place(relx=0.92, rely=0, anchor=NE)

        self.score = StringVar()
        self.score.set(str(0))
        self.score_label = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 20 italic',
                                 background='#006666',
                                 textvariable=self.score)
        self.score_label.place(relx=0.95, rely=0, anchor=NE)
		

        # look at the time for the purposes of making the game difficult as a function of time
        self.lastDiffUpdateTime = 0


    def CheckCollision(self, pos1, pos2):
        if pos1[0] < pos2[2] and pos1[2] > pos2[0] and pos1[1] < pos2[3] and pos1[3] > pos2[1]:
            return True
        return False

    def GetCollisionState(self, pos1, pos2):
        collision_state = 0
        if pos1[2] < pos2[0] + 5:
            collision_state = 1
        if pos1[3] < pos2[1] + 5:
            collision_state = 2
        if pos1[0] > pos2[2] - 5:
            collision_state = 3
        if pos1[1] > pos2[3] - 5:
            collision_state = 4
        return collision_state
        
    def BallMovement(self):
        if self.GamePlaying:
            ballPos = self.canvas.coords(self.Ball)
            playerPos = self.canvas.coords(self.Player)
            #ball_player_inter = set(range(int(ballPos[0]), int(ballPos[2]))).intersection(range(int(playerPos[0]), int(playerPos[2])))
            ball_player_collision = self.CheckCollision(ballPos, playerPos)
            #detect collisions with left, right and top walls respectively
            newPosX = self.BallXDir * BALL_SPEED
            newPosY = self.BallYDir * BALL_SPEED
            if ballPos[2] + newPosX > WINDOW_WIDTH or ballPos[0] + newPosX < 0:
                self.BallXDir *= -1 #change the direction
            elif ballPos[1] + newPosY < 0: #or ballPos[3] + newPosY > WINDOW_HEIGHT:
                self.BallYDir *= -1
            #detect collision with bottom wall
            elif ballPos[3] + newPosY > WINDOW_HEIGHT:
                self.GameOver = True
                self.GamePlaying = False
                self.end_msg = self.canvas.create_text((WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100),
                                                 text="GAME OVER!",
                                                 font="Helvetica 60 bold italic")

            #detect collision with the player
            elif ball_player_collision != 0:
                self.BallYDir *= -1

            #detect collision with bricks
            for (r, row) in enumerate(self.Bricks):
                done = False
                for (c, col) in enumerate(row):
                    brick = self.Bricks[r][c]
                    if brick[1]:
                        brickPos = self.canvas.coords(brick[0])
                        ball_brick_collision = self.CheckCollision(brickPos, ballPos)
                        if ball_brick_collision:
                            self.score.set(str(int(self.score.get()) + 10))
                            collision_state = self.GetCollisionState(ballPos, brickPos)
                            if collision_state == 1 or collision_state == 3:
                                self.BallXDir *= -1
                            if collision_state == 2 or collision_state == 4:
                                self.BallYDir *= -1
                            self.Bricks[r][c][1] = False
                            self.canvas.delete(self.Bricks[r][c][0])
                            done = True
                            break
                if done:
                    break
            #update the ball position if the game is not over yet
            if not self.GameOver:
                newPosX = self.BallXDir * BALL_SPEED
                newPosY = self.BallYDir * BALL_SPEED
                self.canvas.move(self.Ball, newPosX, newPosY)
        if self.CheckGameWon():
            self.GameWon()
        else:
            self.UpdateDifficulty()        

            self.master.after(int(1000/60), self.BallMovement)

    def GameWon(self):
        self.GameOver = True
        self.GamePlaying = False
        self.end_msg = self.canvas.create_text((WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100),
                                                 text="You Won!",
                                                 font="Helvetica 60 bold italic")

    def CheckGameWon(self):
        gamewon = True
        for row in range(len(self.Bricks)):
            for col in range(len(self.Bricks[row])):
                #check if there exists a single 
                brick = self.Bricks[row][col]
                if brick[1]:
                    gamewon = False
        return gamewon

    def UpdateDifficulty(self):
        #factor in the pause time when using delta time
        currentTime = time() # in seconds
        #difficulty should be updated more frequently as the level increases
        deltaTime = currentTime - self.lastDiffUpdateTime
        requiredDelta = 30 * (5 - self.Level)
        if deltaTime >= requiredDelta:
            self.lastDiffUpdateTime = currentTime
            # move all the blocks down one block height
            self.MoveBlocksDown(1)

    def MoveBlocksDown(self, levels):
        #levels is the number of block heights we move the blocks down by
        for row in range(len(self.Bricks)):
            for col in range(len(self.Bricks[row])):
                brick = self.Bricks[row][col]
                if brick[1]:
                    self.canvas.move(brick[0], 0, levels * BRICK_HEIGHT)

    def StartGame(self, event):
        if not self.GamePlaying:
            self.GamePlaying = True
            self.canvas.delete(self.start_msg)
        else:
            self.GamePlaying = False
            self.start_msg = self.canvas.create_text((WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 100),
                                                 text="Press Spacebar to Start Game",
                                                 font="Helvetica 50 bold italic")
            self.lastDiffUpdateTime = time()
            

    def DrawCircle(self, x, y, radius, colour):
        return self.canvas.create_oval(x - radius, y - radius,
                                       x + radius, y + radius,
                                       width=0, fill=colour)

    def ProduceBrick(self, colour, x1, y1, x2, y2):
        brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colour)
        return brick


    def ProduceBricks(self, rows):
        cols = (WINDOW_WIDTH - (2 * X_PADDING)) // BRICK_WIDTH
        colours = ['#dc3020', '#f09336', '#fffd55', '#2e74f6', '#eb42f7', '#74f94c']
        colourIndex = random.randint(0, len(colours) - 1)
        currentY = TOP_PADDING
        counter = 0
        for r in range(rows):
            row = []
            currentY = TOP_PADDING + (r * BRICK_HEIGHT)
            currentEndY = currentY + BRICK_HEIGHT
            for c in range(cols):
                brickColour = colours[colourIndex]
                colourIndex = colourIndex + 1 if colourIndex < len(colours) - 1 else 0
                currentX = X_PADDING + (c * BRICK_WIDTH)
                currentEndX = currentX + BRICK_WIDTH
                brick = self.ProduceBrick(brickColour, currentX, currentY,
                                          currentEndX, currentEndY)
                row.append([brick, True]) #the True represents that the brick is visible
            self.Bricks.append(row)
            

    def LeftKeyPressed(self, event):
        playerPos = self.canvas.coords(self.Player)
        newPosX = playerPos[0] - PLAYER_SPEED
        if newPosX >= 0:
            self.canvas.move(self.Player, -PLAYER_SPEED, 0)

    def RightKeyPressed(self, event):
        playerPos = self.canvas.coords(self.Player)
        newPosX = playerPos[0] + PLAYER_SPEED
        if newPosX <= WINDOW_WIDTH:
            self.canvas.move(self.Player, PLAYER_SPEED, 0)

        

def run():
    root = Tk()
    app = OneP(root)
    root.mainloop()
#run()
