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
        
        self.Player = self.canvas.create_oval(0.43*WINDOW_WIDTH,
                                                   WINDOW_HEIGHT - PLAYER_HEIGHT - BOTTOM_PADDING,
                                                   0.57*WINDOW_WIDTH,
                                                   WINDOW_HEIGHT - BOTTOM_PADDING,
                                                   width=0, fill='blue')
        self.master.bind("<Left>", self.LeftKeyPressed)
        self.master.bind("<Right>", self.RightKeyPressed)
        
        self.Bricks = []
        self.Level = 0
        self.BallSpeed = 2

        self.GamePlaying = False
        self.GameOver = False
        #start the game when the user first presses space
        self.master.bind('<space>', self.StartGame)
        self.master.after(1, self.BallMovement)

        self.score = StringVar()
        self.score.set("Score: "+str(0))
        self.score_label = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 20 italic',
                                 background='#006666',
                                 textvariable=self.score)
        self.score_label.place(relx=0.95, rely=0, anchor=NE)

        self.level = StringVar()
        self.level.set("Level: "+str(self.Level))
        self.level_label = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 20 italic',
                                 background='#006666',
                                 textvariable=self.level)
        self.level_label.place(relx=0.5, rely=0, anchor=N)
        
        self.BallEffects = []
        self.PlayerEffects = []
		

        # look at the time for the purposes of making the game difficult as a function of time
        self.lastDiffUpdateTime = 0

        self.Cheats = ['fire', 'ice', 'colours', 'guns', 'big', 'slow']
        self.master.bind('<Key>', self.ApplyCheats)
        self.KeysPressed = []

        self.UpdateLevel()

    def ApplyCheats(self, event):
        self.KeysPressed.append(event.char)
        print(self.KeysPressed)

        keysPressed = ''.join(self.KeysPressed).lower()#cheats are case-insensitive
        for cheat in self.Cheats:
            if cheat in keysPressed and cheat not in self.BallEffects and cheat not in self.PlayerEffects:
                #reset this key stack so that the same cheat is not applied continuously without user input
                self.KeysPressed = []
                if cheat == 'fire' and 'ice' not in self.BallEffects:
                    #iceball and fireball effects cannot be applied at the same time
                    #apply the fireball effect for 5 seconds
                    self.master.after(1, lambda: self.ApplyFireball(5))
                elif cheat == 'ice' and 'fire' not in self.BallEffects:
                    #apply the iceball effect for 5 seconds
                    self.master.after(1, lambda: self.ApplyIceball(5))
                elif cheat == 'big':
                    #make the player bigger for 5 seconds
                    self.master.after(1, lambda: self.ApplyBig(5, False))

    def ApplyBig(self, timecounter, applied):
        '''In this cheat, the player increases in width for 5 seconds'''
        playerPos = self.canvas.coords(self.Player)
        if timecounter != 0:
            if not applied:
                self.canvas.delete(self.Player)
                self.Player = self.canvas.create_oval(playerPos[0] - (0.04*WINDOW_WIDTH),
                                                           WINDOW_HEIGHT - PLAYER_HEIGHT - BOTTOM_PADDING,
                                                           (0.04*WINDOW_WIDTH) + playerPos[2],
                                                           WINDOW_HEIGHT - BOTTOM_PADDING,
                                                           width=0, fill='blue')
            timecounter -= 1
            self.master.after(1000, lambda: self.ApplyBig(timecounter, True))
        else:
            self.canvas.delete(self.Player)
            self.Player = self.canvas.create_oval((0.02*WINDOW_WIDTH) + playerPos[0],
                                                  WINDOW_HEIGHT - PLAYER_HEIGHT - BOTTOM_PADDING,
                                                  playerPos[2] - (0.02*WINDOW_WIDTH),
                                                  WINDOW_HEIGHT - BOTTOM_PADDING,
                                                  width=0, fill='blue')
            

    def ApplyIceball(self, timecounter):
        '''In this cheat, the ball does not destroy any bricks upon contact, it simply rebounds'''
        ballColour = self.canvas.itemcget(self.Ball, "fill")
        if timecounter != 0:
            if ballColour != '#4eaed8':
                self.BallEffects.append('ice')
                self.canvas.itemconfig(self.Ball, fill='#4eaed8')
            timecounter -= 1
            self.master.after(1000, lambda: self.ApplyIceball(timecounter))
        else:
            #reset the colour of the ball and remove the cheat from active ball effects
            self.BallEffects.remove('ice')
            self.canvas.itemconfig(self.Ball, fill='#99ff99')

    def ApplyFireball(self, timecounter):
        '''In this cheat, the ball does not rebound when it collides with a brick, it destorys
            everything in its path'''
        ballColour = self.canvas.itemcget(self.Ball, "fill")
        if timecounter != 0:
            if ballColour != '#ff3333':
                self.BallEffects.append('fire')
                self.canvas.itemconfig(self.Ball, fill='#ff3333')
            timecounter -= 1
            self.master.after(1000, lambda: self.ApplyFireball(timecounter))
        else:
            #reset the colour of the ball and remove cheat from active ball effects
            self.BallEffects.remove('fire')
            self.canvas.itemconfig(self.Ball, fill='#99ff99')
        
                
        
            

    def UpdateLevel(self):
        if self.Level == 5:
            self.GameWon()
        else:
            if self.Level != 0:
                #congratulate them for making it to the next level
                self.LevelTransition()
                self.BallSpeed *= 1.5 * self.Level
                self.canvas.delete(self.Ball)
            self.Level += 1
            self.level.set("Level: "+str(self.Level))
            self.GamePlaying = False
            self.ProduceBricks(self.Level * 2)
            self.canvas.update()
            self.Ball = self.DrawCircle(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 15, '#99ff99')
            self.BallXDir = random.uniform(-1, 1)
            self.BallYDir = 1
            self.canvas.update()
            self.start_msg = self.canvas.create_text((WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 100),
                                                 text="Press Spacebar to Start Game",
                                                 font="Helvetica 50 bold italic")
            
    def LevelTransition(self):
        self.GamePlaying = False
        msg = self.canvas.create_text((WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 100),
                                                 text="Congratularions on finishing "+str(self.Level)+"!",
                                                 font="Helvetica 50 bold italic")
        sleep(3)
        self.canvas.delete(msg)
        self.canvas.update()
        msg = self.canvas.create_text((WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 100),
                                                 text="Get ready for level "+str(self.Level + 1)+"!",
                                                 font="Helvetica 50 bold italic")
        self.canvas.delete(msg)
        self.canvas.update()
        sleep(3)
        self.start_msg = self.canvas.create_text((WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) + 100),
                                                 text="Press Spacebar to Start Game",
                                                 font="Helvetica 50 bold italic")
        

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
            newPosX = self.BallXDir * self.BallSpeed
            newPosY = self.BallYDir * self.BallSpeed
            if ballPos[2] + newPosX > WINDOW_WIDTH or ballPos[0] + newPosX < 0:
                self.BallXDir *= -1 #change the direction
            elif ballPos[1] + newPosY < 0: #or ballPos[3] + newPosY > WINDOW_HEIGHT:
                self.BallYDir *= -1
            #detect collision with bottom wall
            elif ballPos[3] + newPosY > WINDOW_HEIGHT:
                self.GameLost()

            #detect collision with the player
            elif ball_player_collision != 0:
                self.BallYDir *= -1
                ballXPt = (ballPos[0] + ballPos[2])/2
                playerCenterX = (playerPos[0] + playerPos[2])/2
                distanceFromCentre = abs(playerCenterX - ballXPt)
                if ballXPt > playerCenterX:
                    #has to be positive (move towards the right of the screen)
                    self.BallXDir = abs(self.BallXDir) * (2 * distanceFromCentre / BRICK_WIDTH)
                elif ballXPt < playerCenterX:
                    #has to be negative (move towards the left of the screen)
                    self.BallXDir = -abs(self.BallXDir) * (2 * distanceFromCentre / BRICK_WIDTH)
                #ball moves straight back up if it lands in the exact center of the screen so don't need to do anything explicitly for that case
                #the speed of the ball depends on how far it is from the center too
                #it is faster closer to edge but slower towards the center
                #max speed for any level should be (4 * level)
                newSpeed = 5 * self.BallSpeed * distanceFromCentre / BRICK_WIDTH
                if newSpeed > 4 * self.Level:
                    newSpeed = 4 * self.Level
                if newSpeed > self.BallSpeed:
                    self.BallSpeed = newSpeed
                

            #detect collision with bricks
            for (r, row) in enumerate(self.Bricks):
                done = False
                for (c, col) in enumerate(row):
                    brick = self.Bricks[r][c]
                    if brick[1]:
                        brickPos = self.canvas.coords(brick[0])
                        ball_brick_collision = self.CheckCollision(brickPos, ballPos)
                        if ball_brick_collision:
                            collision_state = self.GetCollisionState(ballPos, brickPos)
                            if not 'fire' in self.BallEffects:
                                if collision_state == 1 or collision_state == 3:
                                    self.BallXDir *= -1
                                if collision_state == 2 or collision_state == 4:
                                    self.BallYDir *= -1
                            if 'ice' not in self.BallEffects:
                                self.score.set("Score: "+str(int(self.score.get().split(": ")[1]) + 10))
                                self.Bricks[r][c][1] = False
                                self.canvas.delete(self.Bricks[r][c][0])
                                done = True
                                break
                if done:
                    break
            #update the ball position if the game is not over yet
            if not self.GameOver:
                newPosX = self.BallXDir * self.BallSpeed
                newPosY = self.BallYDir * self.BallSpeed
                self.canvas.move(self.Ball, newPosX, newPosY)
        if self.CheckLevelFinished():
            self.UpdateLevel()
        elif self.GamePlaying:
            self.UpdateDifficulty()        
        if not self.GameOver:
            self.master.after(int(1000/60), self.BallMovement)



    def GameWon(self):
        self.GameOver = True
        self.GamePlaying = False
        self.end_msg = self.canvas.create_text((WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100),
                                                 text="You Won!",
                                                 font="Helvetica 60 bold italic")

    def CheckLevelFinished(self):
        levelFinished = True
        for row in range(len(self.Bricks)):
            for col in range(len(self.Bricks[row])):
                #check if there exists a single 
                brick = self.Bricks[row][col]
                if brick[1]:
                    levelFinished = False
        return levelFinished

    def UpdateDifficulty(self):
        #factor in the pause time when using delta time
        currentTime = time() # in seconds
        #difficulty should be updated more frequently as the level increases
        deltaTime = currentTime - self.lastDiffUpdateTime
        requiredDelta = 30 - (5 * self.Level)
        if deltaTime >= requiredDelta:
            self.lastDiffUpdateTime = currentTime
            # move all the blocks down one block height
            self.MoveBlocksDown(1)

    def MoveBlocksDown(self, levels):
        #levels is the number of block heights we move the blocks down by
        last_row = 0#used to check if the game has been lost due to the bricks moving too far down
        #if the last brick is 8 brick heights above the player, the game has been lost
        for row in range(len(self.Bricks)):
            for col in range(len(self.Bricks[row])):
                brick = self.Bricks[row][col]
                if brick[1]:
                    self.canvas.move(brick[0], 0, levels * BRICK_HEIGHT)
                    brickCoords = self.canvas.coords(brick[0])
                    if last_row < brickCoords[3]:
                        last_row = brickCoords[3]
        if (self.canvas.coords(self.Player)[1] - last_row) <= BRICK_HEIGHT * 8:
            #game has been lost bevause the bricks have come down beyond the arbitrarily defined point
            self.GameLost()

    def GameLost(self):
        self.GameOver = True
        self.GamePlaying = False
        self.end_msg = self.canvas.create_text((WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100),
                                                 text="You Lost!",
                                                 font="Helvetica 60 bold italic")

    def StartGame(self, event):
        if not self.GamePlaying:
            self.canvas.delete(self.start_msg)
            self.canvas.update()
            counterLabel = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 50 bold italic',
                                 background='#006666',
                                 text='3...')
            counterLabel.place(relx=0.5, rely=0.75, anchor=CENTER)
            self.master.update()
            sleep(1)
            counterLabel.destroy()
            counterLabel = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 50 bold italic',
                                 background='#006666',
                                 text='2...')
            counterLabel.place(relx=0.5, rely=0.75, anchor=CENTER)
            self.master.update()
            sleep(1)
            counterLabel.destroy()
            counterLabel = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 50 bold italic',
                                 background='#006666',
                                 text='1...')
            counterLabel.place(relx=0.5, rely=0.75, anchor=CENTER)
            self.master.update()
            sleep(1)
            counterLabel.destroy()
            self.GamePlaying = True
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
        #colours = ['#dc3020', '#f09336', '#fffd55', '#2e74f6', '#eb42f7', '#74f94c']
        colours = ['#ff3333', '#f7da57', '#4eaed8', '#439541', '#4d4d4d']
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
        if newPosX >= 0 and self.GamePlaying and not self.GameOver:
            self.canvas.move(self.Player, -PLAYER_SPEED, 0)

    def RightKeyPressed(self, event):
        playerPos = self.canvas.coords(self.Player)
        newPosX = playerPos[2] + PLAYER_SPEED
        if newPosX <= WINDOW_WIDTH and self.GamePlaying and not self.GameOver:
            self.canvas.move(self.Player, PLAYER_SPEED, 0)

        

def run():
    root = Tk()
    app = OneP(root)
    root.mainloop()
#run()
