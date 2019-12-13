from tkinter import *
import random
from time import time, sleep
import shelve
import pickle
import BrickBreaker


#below are the constants used in the game
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


class LeaderboardPopup():
    '''
    Creates popups at the end of the game to make leaderboard entries

    Parameters
    ----------
    master: Tk() object that this popup belongs to
    score: end score of the user

    Attributes
    -----------
    self.master: The popup window
    self.score: score parameter is stored here
    self.canvas: the canvas for the popup window
    self.name: label which holds string "Name:"
    self.nameVal: Entry object that allows user to enter name
    self.enter: Button that calls self.AddLeaderboard when pressed
    '''
    def __init__(self, master, score):
        self.master = Toplevel(master)
        self.score = score
        self.master.title("Leaderboard Entry")
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master,
                             cursor='pirate',
                             width=200,
                             height=200,
                             highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='#006666')
        self.name = Label(self.master, text="Name:")
        self.name.place(relx=0.5, rely=0.0, anchor=N)
        self.nameVal = Entry(self.master)
        self.nameVal.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.enter = Button(self.master, text='Publish',
                            command=self.AddLeaderboard)
        self.enter.place(relx=0.5, rely=0.4, anchor=CENTER)

    def AddLeaderboard(self):
        '''
        Adds the score and name to leaderboard data pickle
        '''
        # get the name that the user entered as a string
        name = self.nameVal.get()
        # load the current leaderboard data (2-d list)
        scores = pickle.load(open('leaderboard-data.p', 'rb'))
        # append new data to the list
        scores.append([name, self.score])
        # overwrite previous data with new data
        pickle.dump(scores, open('leaderboard-data.p', 'wb'))
        # destroy the popup
        self.master.destroy()


class SaveGamePopup():
    '''
    Create popups that allow the user to save the game with filename input

    Parameters
    ----------
    master: Tk() object that this popup belongs to
    score:score of the user at the start of the current level
    level: the current level of the user

    Attributes
    ----------
    self.parent: the parent window of the popup
    self.master: the popup window
    self.score: score parameter is stored here
    self.canvas: the canvas for the popup window
    self.name: Label asking for the filename
    self.nameVal: Entry object where user can enter filename
    self.enter: Button which calls self.SaveGame when called
    '''
    def __init__(self, master, score, level):
        self.parent = master
        self.master = Toplevel(master)
        self.score = score
        self.level = level
        self.master.title("Save Game")
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master,
                             cursor='pirate',
                             width=200,
                             height=200,
                             highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='#006666')
        self.name = Label(self.master, text="Filename:")
        self.name.place(relx=0.5, rely=0.0, anchor=N)
        self.nameVal = Entry(self.master)
        self.nameVal.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.enter = Button(self.master, text='Save', command=self.SaveGame)
        self.enter.place(relx=0.5, rely=0.4, anchor=CENTER)

    def SaveGame(self):
        # get the filename entered by the user
        gamename = self.nameVal.get()
        # create a file in the current directory
        # it's called gamename+'.db'
        # it will be a shelve and will store the score and level
        with shelve.open(gamename) as db:
            db['score'] = self.score
            db['level'] = self.level
        # destroy parent window and popup
        self.master.destroy()
        self.parent.destroy()
        # return the user to the main menu
        BrickBreaker.run()


class BossKeyPopup():
    '''
    Opens a fullscreen image that makes people think they're working

    Parameters
    ----------
    bossKey: the key that is bound on the canvas to the bosskey

    Attributes
    ----------
    self.master: Tk object which is the popup window
    self.canvas: Canvas object for the popup window
    self.Boss: Canvas element, full screen image
    '''
    def __init__(self, master, bossKey):
        self.master = Toplevel(master)
        self.master.title("Work")
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master,
                             cursor='none',
                             width=self.master.winfo_screenwidth(),
                             height=self.master.winfo_screenheight(),
                             highlightthickness=0)
        self.canvas.pack()
        self.canvas.configure(background='#006666')
        bossKeyImage = PhotoImage(file='BossKeyImage.png')
        # avoid the image from being garbage collected
        self.master.bossKeyImage = bossKeyImage
        self.Boss = self.canvas.create_image(0, 0, image=bossKeyImage,
                                             anchor=NW)
        # call the BossKeyPressed function when the bossKey is pressed
        self.master.bind(bossKey, self.BossKeyPressed)

    def BossKeyPressed(self, event):
        '''
        When pressed, returns the user to their game
        '''
        # destory the popup window
        self.master.destroy()


class OneP():
    '''
    The actual game

    Parameters
    ----------
    master: Tk object which will be the main game window
    gamename: (optional) provided when loading a game

    Attributes
    ----------
    self.gamename: gamename parameter is stored here
    self.master: master parameter is stored here
    self.canvas: Canvas object for the game window
    self.level: StringVar object used to vary text on self.level_label
    self.Level: self.level but as an integer between 0 and 5
    self.score: StringVar object used to vary text on self.score_label
    self.BackBtn: returns user to main menu when pressed
    self.RestartBtn: restarts the game
    self.SaveBtn: saves the current game in required format
    self.PlayerColour: colour of player's sprite rectangle
    self.Player: a rectangle that the user can control with keys
    self.keybindings: default/user chosen key bindings for the game
    self.Bricks: list of canvas rectangles
    self.BallSpeed: speed of the ball element
    self.GamePlaying: signifies whether game is paused or not
    self.GameOver: signifies whether game has been won/lost yet or not
    self.score_label: displays the current score of the user
    self.level_label: displays the current level of the user
    self.BallEffects: list of effects applied to ball using cheats
    self.PlayerEffects: list of effects applied to player using cheats
    self.lastDiffUpdatedTime: last time at which game difficulty was updated
    self.Cheats: list of valid cheats as strings that can be used
    self.KeysPressed: stack of keys pressed in the order (not part of controls)
    self.FireballImage: image of a fireball
    self.IceballImage: image of an iceball
    self.Bullets: list of bullets elements currently active on the canvas
    self.Ball: a circle element on the canvas
    self.BallXDir: signifies the x direction of the ball's movement
    self.BallYDir: signifies the y direction of the ball's movement
    self.start_msg: display instructions to the user on how to start the game
    '''
    def __init__(self, master, gamename=None):
        self.gamename = gamename
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

        self.level = StringVar()
        self.Level = 0
        self.score = StringVar()
        if gamename is None:
            # not loading a previously saved game
            self.score.set("Score: " + str(0))
            self.level.set("Level: " + str(self.Level))
        else:
            # loading the provided game from the start of that level
            # accessing game data from the file shelve
            # and then assigning it to relevant class attributes
            with shelve.open(gamename) as db:
                self.score.set("Score: " + str(db['score']))
                self.Level = db['level']
                self.level.set("Level: " + str(self.Level))

        # get the center coordinates of the window
        window_centerX = WINDOW_WIDTH / 2
        window_centerY = WINDOW_HEIGHT / 2
        # get the general center coordinates of the player
        player_centerX = PLAYER_WIDTH / 2
        player_centerY = PLAYER_HEIGHT / 2

        self.BackBtn = Button(self.master,
                              cursor='trek',
                              background='#00e6e6',
                              activebackground='#009999',
                              relief=GROOVE,
                              font="Helvetica 12",
                              command=self.BackBtnPressed,
                              text="Main Menu")
        self.BackBtn.place(relx=0.0, rely=0, anchor=NW)

        self.RestartBtn = Button(self.master,
                                 cursor='trek',
                                 background='#00e6e6',
                                 activebackground='#009999',
                                 relief=GROOVE,
                                 font="Helvetica 12",
                                 command=self.RestartBtnPressed,
                                 text="Restart")
        self.RestartBtn.place(relx=0.1, rely=0, anchor=NW)

        self.SaveBtn = Button(self.master,
                              cursor='trek',
                              background='#00e6e6',
                              activebackground='#009999',
                              relief=GROOVE,
                              font="Helvetica 12",
                              command=self.SaveGameBtnPressed,
                              text="Save Game")
        self.SaveBtn.place(relx=0.2, rely=0, anchor=NW)

        self.PlayerColour = 'blue'

        # create the player rectangle
        self.Player = self.canvas.create_rectangle(0.43 * WINDOW_WIDTH,
                                                   WINDOW_HEIGHT -
                                                   PLAYER_HEIGHT -
                                                   BOTTOM_PADDING,
                                                   0.57 * WINDOW_WIDTH,
                                                   WINDOW_HEIGHT -
                                                   BOTTOM_PADDING,
                                                   width=0,
                                                   fill=self.PlayerColour)

        # load up the default/user chosen key bindings
        # from the keybindings pickle file
        # and store this in a dictionary
        self.keybindings = pickle.load(open('keybindings.p', 'rb'))

        # bind the loaded keys to relevant functions
        self.master.bind(self.keybindings['left'], self.LeftKeyPressed)
        self.master.bind(self.keybindings['right'], self.RightKeyPressed)
        self.master.bind(self.keybindings['boss'], self.BossKeyPressed)

        # initialise an empty list for the list of bricks that will be rendered
        self.Bricks = []
        self.BallSpeed = 2

        # at the moment the game is not playing
        # game is loaded in a pause state
        self.GamePlaying = False
        # game is not over yet
        self.GameOver = False
        # start the game when the user first presses pause button
        self.master.bind(self.keybindings['pause'], self.StartGame)

        # used to display the current score of the user
        self.score_label = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 20 italic',
                                 background='#006666',
                                 textvariable=self.score)
        self.score_label.place(relx=0.95, rely=0, anchor=NE)

        # used to display the current level of the user
        self.level_label = Label(self.master,
                                 cursor='none',
                                 font='Helvetica 20 italic',
                                 background='#006666',
                                 textvariable=self.level)
        self.level_label.place(relx=0.5, rely=0, anchor=N)

        self.BallEffects = []
        self.PlayerEffects = []

        # look at the time for the purposes of making the game difficult
        # as a function of time
        self.lastDiffUpdateTime = 0

        # list of valid cheats that can be used during the game
        self.Cheats = ['fire', 'ice', 'colours', 'guns', 'big', 'slow']
        # and key that is not used for controls is bound to
        # the self.ApplyCheats function
        self.master.bind('<Key>', self.ApplyCheats)
        # this is the stack that the above described keys get appended to
        # when they are typed in the middle of the game
        self.KeysPressed = []

        # used to display the powerups currently in use
        self.powerups_label = Label(self.master,
                                    cursor='none',
                                    font='Helvetica 20 italic',
                                    background='#006666',
                                    text='Powerups:')
        self.powerups_label.place(relx=0.65, rely=0, anchor=N)

        fireball = PhotoImage(file='fireball.png')
        #  avoid the image from being garbage collected
        self.master.Fireball = fireball
        self.FireballImage = self.canvas.create_image(0.72 * WINDOW_WIDTH, 0,
                                                      image=fireball, anchor=N,
                                                      state=HIDDEN)

        iceball = PhotoImage(file='iceball.png')
        # avoid the image from being garbage collected
        self.master.Iceball = iceball
        self.IceballImage = self.canvas.create_image(0.75 * WINDOW_WIDTH, 0,
                                                     image=iceball, anchor=N,
                                                     state=HIDDEN)

        self.Bullets = []
        # call the UpdateLevel function to increase level from 0 to 1
        # and start the game
        self.UpdateLevel()
        # call BallMovement on a separate thread so that other tasks
        # can happen simultaneously, like the movement of the player
        self.master.after(1, self.BallMovement)

    def BackBtnPressed(self):
        '''Returns the user to the main menu'''
        # destroy the current window and open main menu
        self.master.destroy()
        BrickBreaker.run()

    def RestartBtnPressed(self):
        '''Restarts the game'''
        # destroy the current window and just open one of the same again
        # this re-initialises everything in the window
        self.master.destroy()
        run()

    def ApplyCheats(self, event):
        '''Used to apply cheats during the game
            The user can simply type their cheats while playing and they
            will be applied assuming certain conditions are met.
        '''
        # cheats cannot be typed in while the game is paused
        if self.GamePlaying:
            # append the character pressed to the self.KeysPressed stack
            self.KeysPressed.append(event.char)
            # cheats are case-insensitive
            keysPressed = ''.join(self.KeysPressed).lower()
            for cheat in self.Cheats:
                # iterate through every cheat in the valid cheats list
                # check if the cheat has been typed in that order by the user
                # if so, execute the relevant function
                if cheat in keysPressed:
                    if cheat not in self.BallEffects:
                        if cheat not in self.PlayerEffects:
                            # reset this key stack so that the same cheat
                            # is not applied continuously without user input
                            self.KeysPressed = []
                            if (cheat == 'fire'):
                                if ('ice' not in self.BallEffects):
                                    # iceball and fireball effects cannot be
                                    # applied at the same time apply the
                                    # fireball effect for 5 seconds
                                    self.master.after(
                                        1, lambda: self.ApplyFireball(5))
                            elif cheat == 'ice':
                                if 'fire' not in self.BallEffects:
                                    # apply the iceball effect for 5 seconds
                                    self.master.after(
                                        1, lambda: self.ApplyIceball(5))
                            elif cheat == 'big':
                                if 'big' not in self.PlayerEffects:
                                    # make the player bigger for 5 seconds
                                    self.master.after(
                                        1, lambda: self.ApplyBig(5, False))
                            elif cheat == 'slow':
                                if 'slow' not in self.BallEffects:
                                    # can't slow down multiple times
                                    # slow down the ball for 5 seconds
                                    ballSpeed = self.BallSpeed
                                    self.master.after(1, lambda:
                                                      self.ApplySlow(5,
                                                                     ballSpeed,
                                                                     False))
                            elif cheat == 'colours':
                                # change the colour of the player randomly
                                self.ApplyColours()
                            elif cheat == 'guns':
                                # give the player guns
                                self.master.after(
                                    1, lambda: self.ApplyGuns(3, 3))

    def ApplyGuns(self, timecounter, bullets):
        '''Shoots 2 bullets, every 3 seconds, 3 times
            the bullets destroy bricks when they get in contact with them.
            The bullets are two vertical rectangles generated at the edges
            of the self.Player and they travel upwards'''
        # get the current player coordinates so that we know where to generate
        # the bullets
        playerPos = self.canvas.coords(self.Player)
        if bullets > 0:
            # shoot bullets when timecounter is 3 and there is at least one
            # bullet remaining to be shot
            if timecounter == 3:
                # create two vertically slim rectangles at the edges of the
                # player
                bulletWidth = 5
                bulletHeight = 20
                bullet1 = self.canvas.create_rectangle(playerPos[0],
                                                       playerPos[1] +
                                                       bulletHeight,
                                                       playerPos[0] +
                                                       bulletWidth,
                                                       playerPos[1],
                                                       width=0, fill='yellow')
                bullet2 = self.canvas.create_rectangle(playerPos[2] -
                                                       bulletWidth,
                                                       playerPos[1] +
                                                       bulletHeight,
                                                       playerPos[2],
                                                       playerPos[1],
                                                       width=0, fill='yellow')
                self.Bullets.append(bullet1)
                self.Bullets.append(bullet2)
                # call the MoveBullets function on a separate thread to ensure
                # that other movements, such as that of the ball, can
                # continue without hindrance
                self.master.after(1, self.MoveBullets)
                # once the bullets have been shot, the number remaining goes
                # down by one
                bullets -= 1
            timecounter -= 1
            if timecounter == 0:
                # reset the timecounter once it hits 0
                timecounter = 3
            # call the function again after 1 second with updated parameters
            self.master.after(1000, lambda: self.ApplyGuns(timecounter,
                                                           bullets))

    def MoveBullets(self):
        '''
        Used to move bullets in the game generated using the guns cheat
        '''
        # move every bullet in self.Bullets by 10 pixels in the y direction
        # also destroy any bricks that they collide with
        for bullet in self.Bullets:
            bulletPos = self.canvas.coords(bullet)
            # newPosY = bulletPos[1] - 10
            # newBulletPos = bulletPos[0], newPosY, bulletPos[2], newPosY + 20
            # 20 is the bulletHeight and 10 is the bulletSpeed
            self.canvas.move(bullet, 0, -10)
            newBulletPos = self.canvas.coords(bullet)
            # if the bullet has exited the window frame, delete it
            if newBulletPos[2] <= 0:
                self.canvas.delete(bullet)
                self.Bullets.remove(bullet)
            # detect collision with bricks
            for (r, row) in enumerate(self.Bricks):
                done = False
                for (c, col) in enumerate(row):
                    brick = self.Bricks[r][c]
                    if brick[1]:
                        brickPos = self.canvas.coords(brick[0])
                        ball_brick_collision = self.CheckCollision(brickPos,
                                                                   newBulletPos
                                                                   )
                        if ball_brick_collision:
                            # bullet and brick get destroyed and score increase
                            self.score.set("Score: " +
                                           str(int(self.score.get().split(": ")
                                                   [1]) + 10))
                            self.Bricks[r][c][1] = False
                            self.canvas.delete(self.Bricks[r][c][0])
                            self.canvas.delete(bullet)
                            self.Bullets.remove(bullet)
                            done = True
                            break
                if done:
                    break
        if len(self.Bullets) != 0 and self.GamePlaying:
            # re-call the function for moving the bullets after 10 milliseconds
            # only if there is at least one remaining bullet on the canvas
            # also check if the game is paused or not
            self.master.after(10, self.MoveBullets)

    def ApplyColours(self):
        '''
        The colour of the player is changed to a random one chosen
        from a list of colours
        '''
        playerColours = ['red', 'green', 'grey', 'pink', 'blue', 'black']
        # randomly choose a colour from the above list
        # then assign it to the self.PlayerColour attribute to track it too
        self.PlayerColour = random.choice(playerColours)
        # set the colour to the newly randomly generated colour
        self.canvas.itemconfig(self.Player, fill=self.PlayerColour)

    def ApplySlow(self, timecounter, initialSpeed, applied):
        '''
        In this cheat, the ball speed slows down by a factor of two,
        making it easier for the user.
        Only applied for the amount of time specified by the timecounter
        '''
        if timecounter != 0:
            # while there is time remaining
            if not applied:
                # if it hasn't already been applied
                # if we don't do this, the cheat will be applied
                # timecounter times
                self.BallEffects.append('slow')
                # reduce the ball speed attribute
                self.BallSpeed *= 0.5
            timecounter -= 1
            # call the function again after a second with updated attributes
            self.master.after(1000, lambda: self.ApplySlow(timecounter,
                                                           initialSpeed, True))
        else:
            # once the time is up, remove this effect
            # and set the speed back to the initial speed
            self.BallEffects.remove('slow')
            self.BallSpeed = initialSpeed

    def ApplyBig(self, timecounter, applied):
        '''In this cheat, the player increases in width.
        This cheat can only be applied once during the game'''
        playerPos = self.canvas.coords(self.Player)
        if timecounter != 0:
            # while there is time remaining
            if not applied:
                # if it hasn't been applied already been applied
                self.PlayerEffects.append('big')
                self.canvas.delete(self.Player)
                colour = self.PlayerColour
                self.Player = self.canvas.create_rectangle(playerPos[0] -
                                                           (0.04*WINDOW_WIDTH),
                                                           WINDOW_HEIGHT -
                                                           PLAYER_HEIGHT -
                                                           BOTTOM_PADDING,
                                                           0.04*WINDOW_WIDTH +
                                                           playerPos[2],
                                                           WINDOW_HEIGHT -
                                                           BOTTOM_PADDING,
                                                           width=0,
                                                           fill=colour)
            timecounter -= 1

    def ApplyIceball(self, timecounter):
        '''
        In this cheat, the ball does not destroy any bricks upon contact,
        it simply rebounds
        '''
        ballColour = self.canvas.itemcget(self.Ball, "fill")
        if timecounter != 0:
            # while there is still time left
            if ballColour != '#4eaed8':
                # the above if checks if the cheat has already been applied
                self.BallEffects.append('ice')
                # change the colour of the ball
                self.canvas.itemconfig(self.Ball, fill='#4eaed8')
                # display the iceball image next to the powerups label
                self.canvas.itemconfig(self.IceballImage, state=NORMAL)
            timecounter -= 1
            # call the function again after a second
            self.master.after(1000, lambda: self.ApplyIceball(timecounter))
        else:
            # reset the colour of the ball and remove the cheat
            # from active ball effects
            # remove the iceball image from the powerups
            self.BallEffects.remove('ice')
            self.canvas.itemconfig(self.Ball, fill='#99ff99')
            self.canvas.itemconfig(self.IceballImage, state=HIDDEN)

    def ApplyFireball(self, timecounter):
        '''
        In this cheat, the ball does not rebound when it collides with a
        brick, it destroys everything in its path
        '''
        ballColour = self.canvas.itemcget(self.Ball, "fill")
        if timecounter != 0:
            # while there is still time left
            if ballColour != '#ff3333':
                # the above if checks if the cheat has already been applued
                self.BallEffects.append('fire')
                self.canvas.itemconfig(self.Ball, fill='#ff3333')
                # display the iceball image next to the powerups label
                self.canvas.itemconfig(self.FireballImage, state=NORMAL)
            timecounter -= 1
            self.master.after(1000, lambda: self.ApplyFireball(timecounter))
        else:
            # reset the colour of the ball and remove cheat from ball effects
            # remove the fireball image from the powerups
            self.BallEffects.remove('fire')
            self.canvas.itemconfig(self.Ball, fill='#99ff99')
            self.canvas.itemconfig(self.FireballImage, state=HIDDEN)

    def UpdateLevel(self):
        '''
        Called everytime the current level is finished and new one needs to be
        initialised
        '''
        if self.Level == 5:
            # if the level is 5, the game has been won
            self.GameWon()
        else:
            if self.Level != 0:
                # reset the following attributes to new values
                self.BallSpeed *= 1.5 * self.Level
                self.BallEffects = []
                if self.gamename is None:
                    self.canvas.delete(self.Ball)
            # increment the level and display the new one to the user
            self.Level += 1
            self.level.set("Level: " + str(self.Level))
            # pause the game while the rendering occurs
            self.GamePlaying = False
            # get new bricks
            # the number of rows of bricks depends on the level
            # number of rows = self.Level * 2
            self.ProduceBricks(self.Level * 2)
            self.canvas.update()
            # draw/re-draw the ball at the center of the screen
            self.Ball = self.DrawCircle(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                                        15, '#99ff99')
            # choose a random x direction of the ball
            self.BallXDir = random.uniform(-1, 1)
            # initially the ball has to travel downwards towards the user
            # hence the y direction in initialised to 1
            self.BallYDir = 1
            self.canvas.update()
            # needed to use this because of pep8 line limits
            pauseKey = self.keybindings['pause']
            self.start_msg = self.canvas.create_text((WINDOW_WIDTH / 2,
                                                      (WINDOW_HEIGHT/2) + 100),
                                                     text="Press " +
                                                     pauseKey +
                                                     " to Start Game",
                                                     font="Helvetica 50 bold" +
                                                     " italic")

    def CheckCollision(self, pos1, pos2):
        '''
        Takes the coordinates of two canvas elements as inputs and checks if
        there is an overlap
        '''
        if pos1[0] < pos2[2] and pos1[2] > pos2[0]:
            if pos1[1] < pos2[3] and pos1[3] > pos2[1]:
                # return true if there is an overlap implying a collision
                return True
        # else return false
        return False

    def GetCollisionState(self, pos1, pos2):
        '''
        This function is primarily used to find out whether the ball is
        colliding with the brick along the top/bottom lines or the
        left/right lines
        '''
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
        '''
        This function handles the movement of the ball element and
        its collisions
        '''
        if self.GamePlaying:
            # execute only if the game is not pause
            ballPos = self.canvas.coords(self.Ball)
            playerPos = self.canvas.coords(self.Player)
            ball_player_collision = self.CheckCollision(ballPos, playerPos)
            # detect collisions with left, right and top walls respectively
            newPosX = self.BallXDir * self.BallSpeed
            newPosY = self.BallYDir * self.BallSpeed
            if ballPos[2] + newPosX > WINDOW_WIDTH or ballPos[0] + newPosX < 0:
                # change the direction
                self.BallXDir *= -1
            elif ballPos[1] + newPosY < 0:
                self.BallYDir *= -1
            # detect collision with bottom wall
            elif ballPos[3] + newPosY > WINDOW_HEIGHT:
                self.GameLost()

            # detect collision with the player
            elif ball_player_collision != 0:
                self.BallYDir *= -1
                ballXPt = (ballPos[0] + ballPos[2]) / 2
                playerCenterX = (playerPos[0] + playerPos[2]) / 2
                distanceFromCentre = abs(playerCenterX - ballXPt)
                if ballXPt > playerCenterX:
                    # has to be positive (move towards the right of the screen)
                    self.BallXDir = abs(self.BallXDir) * \
                        (2 * distanceFromCentre / BRICK_WIDTH)
                elif ballXPt < playerCenterX:
                    # has to be negative (move towards the left of the screen)
                    self.BallXDir = -abs(self.BallXDir) * \
                        (2 * distanceFromCentre / BRICK_WIDTH)
                '''ball moves straight back up if it lands in the exact center
                of the screen so don't need to do anything
                explicitly for that case
                the speed of the ball depends on how far
                it is from the center too
                it is faster closer to edge but slower towards the center
                max speed for any level should be (4 * level)'''
                newSpeed = self.BallSpeed
                if 'slow' not in self.BallEffects:
                    newSpeed *= 5 * distanceFromCentre
                if newSpeed > 4 * self.Level:
                    newSpeed = 4 * self.Level
                if newSpeed > self.BallSpeed:
                    self.BallSpeed = newSpeed

            # detect collision with bricks
            for (r, row) in enumerate(self.Bricks):
                done = False
                for (c, col) in enumerate(row):
                    brick = self.Bricks[r][c]
                    if brick[1]:
                        brickPos = self.canvas.coords(brick[0])
                        ball_brick_collision = self.CheckCollision(
                            brickPos, ballPos)
                        if ball_brick_collision:
                            collision_state = self.GetCollisionState(
                                ballPos, brickPos)
                            if 'fire' not in self.BallEffects:
                                # if the fire effect is applied, it just goes
                                # through the brick without rebounding
                                if collision_state in [1, 3]:
                                    self.BallXDir *= -1
                                if collision_state in [2, 4]:
                                    self.BallYDir *= -1
                            if 'ice' not in self.BallEffects:
                                # if the ice effect is applied, it doesn
                                # not destroy the bricks but it does rebound
                                self.score.set("Score: " +
                                               str(int(self.score.get()
                                                       .split(": ")[1]) + 10))
                                self.Bricks[r][c][1] = False
                                self.canvas.delete(self.Bricks[r][c][0])
                                done = True
                                break
                if done:
                    break
            # update the ball position if the game is not over yet
            if not self.GameOver:
                # if the game is still going on, move the ball
                # to the new position
                newPosX = self.BallXDir * self.BallSpeed
                newPosY = self.BallYDir * self.BallSpeed
                self.canvas.move(self.Ball, newPosX, newPosY)
        if self.CheckLevelFinished():
            # check if the level is finished, if so update the level
            print('LEVEL FINISHED')
            self.UpdateLevel()
        elif self.GamePlaying:
            # if the game is not paused, go to UpdateDifficulty
            self.UpdateDifficulty()
        if not self.GameOver:
            # if the game is not yet over, continue ball movement
            self.master.after(int(1000 / 60), self.BallMovement)

    def GameWon(self):
        '''
        if the game has been won, let the user know
        '''
        self.GameOver = True
        self.GamePlaying = False
        self.end_msg = self.canvas.create_text((WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / 2 + 100),
                                               text="You Won!",
                                               font="Helvetica 60 bold italic")
        self.EnterToLeaderboard()

    def EnterToLeaderboard(self):
        '''
        if the game is over, create a popup where the user can enter their name
        this will be stored along with their name in the leaderboard
        '''
        popup = LeaderboardPopup(self.master,
                                 int(self.score.get().split(": ")[1]))

    def CheckLevelFinished(self):
        '''
        This level checks if the level is finished or not by checking if
        there is at least one brick that has not been deleted on the canvas
        '''
        levelFinished = True
        for row in range(len(self.Bricks)):
            for col in range(len(self.Bricks[row])):
                # check if there exists a single
                brick = self.Bricks[row][col]
                if brick[1]:
                    levelFinished = False
        return levelFinished

    def UpdateDifficulty(self):
        '''
        This function updates the difficulty by moving the bricks down
        by one brick height every few seconds.
        This time period is dependent on the level that the user is at
        '''
        currentTime = time()  # in seconds
        # difficulty should be updated more frequently as the level increases
        deltaTime = currentTime - self.lastDiffUpdateTime
        requiredDelta = 30 - (5 * self.Level)
        if deltaTime >= requiredDelta:
            self.lastDiffUpdateTime = currentTime
            # move all the blocks down one block height
            self.MoveBlocksDown(1)

    def MoveBlocksDown(self, levels):
        '''
        This function moves the bricks down
        '''
        # levels is the number of block heights we move the blocks down by
        # used to check if the game has been lost
        # due to the bricks moving too far down
        last_row = 0
        # if the last brick is 8 brick heights above the player,
        # the game has been lost
        for row in range(len(self.Bricks)):
            for col in range(len(self.Bricks[row])):
                brick = self.Bricks[row][col]
                if brick[1]:
                    self.canvas.move(brick[0], 0, levels * BRICK_HEIGHT)
                    brickCoords = self.canvas.coords(brick[0])
                    if last_row < brickCoords[3]:
                        last_row = brickCoords[3]
        if (self.canvas.coords(self.Player)[1] - last_row) <= BRICK_HEIGHT * 8:
            # game has been lost bevause the bricks have come down
            # beyond the arbitrarily defined point
            self.GameLost()

    def GameLost(self):
        '''
        If the game has been determined to be lost,
        let the user know
        '''
        self.GameOver = True
        self.GamePlaying = False
        self.end_msg = self.canvas.create_text((WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / 2 + 100),
                                               text="You Lost!",
                                               font="Helvetica 60 bold italic")
        self.EnterToLeaderboard()

    def StartGame(self, event):
        '''
        This function is used to pause and un-pause the game
        it is called whenever the user presses the pause key
        '''
        if not self.GameOver:
            # only need to execute this code if the game is not yet won/lost
            if not self.GamePlaying:
                # if the game was previously paused,
                # execute a timer that goes "3.. 2.. 1.. Go!"
                self.canvas.delete(self.start_msg)
                self.master.update()
                counterLabel = Label(self.master, cursor='none',
                                     font='Helvetica 50 bold italic',
                                     background='#006666', text='3...')
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
                counterLabel.destroy()
                counterLabel = Label(self.master,
                                     cursor='none',
                                     font='Helvetica 50 bold italic',
                                     background='#006666',
                                     text='Go!')
                counterLabel.place(relx=0.5, rely=0.75, anchor=CENTER)
                self.master.update()
                sleep(1)
                counterLabel.destroy()
                # at the end of the timer display, resume the game
                self.GamePlaying = True
            else:
                # if the game was previously playing, pause it
                # and then display instructions to the user on how they
                # may resume the game
                self.GamePlaying = False
                pauseKey = self.keyBindings['pause']
                self.start_msg = self.canvas.create_text((WINDOW_WIDTH / 2,
                                                          (WINDOW_HEIGHT / 2) +
                                                          100),
                                                         text="Press " +
                                                         pauseKey +
                                                         " to Start Game",
                                                         font="Helvetica 50" +
                                                         "bold italic")
                self.lastDiffUpdateTime = time()

    def DrawCircle(self, x, y, radius, colour):
        '''
        Used to draw the ball on the game canvas
        '''
        return self.canvas.create_oval(x - radius, y - radius,
                                       x + radius, y + radius, width=0,
                                       fill=colour)

    def ProduceBrick(self, colour, x1, y1, x2, y2):
        '''
        produces a brick of the given dimensions and colour and returns that
        '''
        brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colour)
        return brick

    def ProduceBricks(self, rows):
        '''
        Produces <rows> number of rows of bricks
        '''
        # the number of columns in each row is determined by the
        # following equation
        cols = (WINDOW_WIDTH - (2 * X_PADDING)) // BRICK_WIDTH
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
                colourIndex = colourIndex + \
                    1 if colourIndex < len(colours) - 1 else 0
                currentX = X_PADDING + (c * BRICK_WIDTH)
                currentEndX = currentX + BRICK_WIDTH
                brick = self.ProduceBrick(brickColour, currentX, currentY,
                                          currentEndX, currentEndY)
                # the True represents that the brick is visible
                row.append([brick, True])
            self.Bricks.append(row)

    def LeftKeyPressed(self, event):
        '''
        This function is called when the key assigned to move the player
        to the left is pressed
        '''
        playerPos = self.canvas.coords(self.Player)
        newPosX = playerPos[0] - PLAYER_SPEED
        if newPosX >= 0 and self.GamePlaying and not self.GameOver:
            self.canvas.move(self.Player, -PLAYER_SPEED, 0)

    def RightKeyPressed(self, event):
        '''
        This function is called when the key assigned to move the player
        to the right is pressed
        '''
        playerPos = self.canvas.coords(self.Player)
        newPosX = playerPos[2] + PLAYER_SPEED
        if newPosX <= WINDOW_WIDTH and self.GamePlaying and not self.GameOver:
            self.canvas.move(self.Player, PLAYER_SPEED, 0)

    def SaveGameBtnPressed(self):
        '''
        this function is called when the Save Game button is clicked on
        '''
        # pause the game
        self.GamePlaying = False
        # get the current score and level in the required format
        score = int(self.score.get().split(": ")[
                    1])
        level = int(self.level.get().split(": ")[1])
        print(score, level)
        # create a SaveGamePopup so that the user can enter the filename
        popup = SaveGamePopup(self.master, score, level)

    def BossKeyPressed(self, event):
        '''
        This function is called when the boss key is pressed
        '''
        # pause the game
        self.GamePlaying = False
        # create a full screen popup that displays an image to give the
        # appearance of the user working
        popup = BossKeyPopup(self.master, self.keybindings['boss'])


def run():
    '''
    This function is called to start a new game
    '''
    root = Tk()
    app = OneP(root)
    root.mainloop()


def load(gamename):
    '''
    This function is called to reload a previously saved game
    '''
    root = Tk()
    app = OneP(root, gamename)
    root.mainloop()
