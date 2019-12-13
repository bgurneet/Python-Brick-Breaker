from tkinter import *
import pickle
import BrickBreaker

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700


class Settings():
    '''
    Allows the user to change the controls for the game

    Parameters
    ----------
    master: Tk object which will be the main menu window

    Attributes
    ----------
    self.master: the master parameter is stored here
    self.canvas: the canvas for this window
    self.title_label: displays the string "Controls"
    self.function_label: Displays the string "Function"
    self.moveleft_label: Displays the string "Move Left"
    self.moveright_label: Displays the string "Move Right"
    self.pause_label: Displays the string "Pause Game"
    self.boss_label: Displays the string "Boss Key"
    self.moveleftkey_label: The currently selected key for moving left
    self.moverightkey_label: The currently selected key for moving right
    self.pausekey_label: The currently selected key for pausing the game
    self.bosskey_label: The currently selected key for enabling boss key
    self.moveleft_button: calls the self.ChangeLeft function
    self.moveright_button: calls the self.ChangeRight function
    self.pause_button: calls the self.ChangePause function
    self.boss_button: calls the self.ChangeBoss function
    self.back_button: calls the self.BackBtnPressed function
    self.Changing: signifies the key that is being changed
    self.ChangeInProgress: signifies whether a change is occuring right now
    '''
    def __init__(self, master):
        self.master = master
        self.master.title("Brick Breaker - Settings")
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master,
                             cursor='pirate',
                             width=WINDOW_WIDTH,
                             height=WINDOW_HEIGHT,
                             highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='#006666')

        self.title_label = Label(self.master,
                                 cursor='pirate',
                                 font='Helvetica 50 bold',
                                 background='#006666',
                                 text="Controls")
        self.title_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        # need settings for moving left, moving right, game pause, and boss key
        self.function_label = Label(self.master,
                                    cursor='pirate',
                                    font='Helvetica 25 bold',
                                    background='#006666',
                                    text="Function")
        self.function_label.place(relx=0.25, rely=0.3, anchor=CENTER)

        self.moveleft_label = Label(self.master,
                                    cursor='pirate',
                                    font='Helvetica 20',
                                    background='#006666',
                                    text="Move Left")
        self.moveleft_label.place(relx=0.25, rely=0.4, anchor=CENTER)

        self.moveright_label = Label(self.master,
                                     cursor='pirate',
                                     font='Helvetica 20',
                                     background='#006666',
                                     text="Move Right")
        self.moveright_label.place(relx=0.25, rely=0.5, anchor=CENTER)

        self.pause_label = Label(self.master,
                                 cursor='pirate',
                                 font='Helvetica 20',
                                 background='#006666',
                                 text="Pause Game")
        self.pause_label.place(relx=0.25, rely=0.6, anchor=CENTER)

        self.boss_label = Label(self.master,
                                cursor='pirate',
                                font='Helvetica 20',
                                background='#006666',
                                text="Boss Key")
        self.boss_label.place(relx=0.25, rely=0.7, anchor=CENTER)

        self.function_label = Label(self.master,
                                    cursor='pirate',
                                    font='Helvetica 25 bold',
                                    background='#006666',
                                    text="Current")
        self.function_label.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.GetCurrentKeys()

        self.moveleft_button = Button(self.master,
                                      cursor='trek',
                                      background='#00e6e6',
                                      activebackground='#009999',
                                      relief=GROOVE,
                                      font="Helvetica 20",
                                      command=self.ChangeLeft,
                                      text="Change")
        self.moveleft_button.place(relx=0.75, rely=0.4, anchor=CENTER)

        self.moveright_button = Button(self.master,
                                       cursor='trek',
                                       background='#00e6e6',
                                       activebackground='#009999',
                                       relief=GROOVE,
                                       font="Helvetica 20",
                                       command=self.ChangeRight,
                                       text="Change")
        self.moveright_button.place(relx=0.75, rely=0.5, anchor=CENTER)

        self.pause_button = Button(self.master,
                                   cursor='trek',
                                   background='#00e6e6',
                                   activebackground='#009999',
                                   relief=GROOVE,
                                   font="Helvetica 20",
                                   command=self.ChangePause,
                                   text="Change")
        self.pause_button.place(relx=0.75, rely=0.6, anchor=CENTER)

        self.boss_button = Button(self.master,
                                  cursor='trek',
                                  background='#00e6e6',
                                  activebackground='#009999',
                                  relief=GROOVE,
                                  font="Helvetica 20",
                                  command=self.ChangeBoss,
                                  text="Change")
        self.boss_button.place(relx=0.75, rely=0.7, anchor=CENTER)

        self.back_button = Button(self.master,
                                  cursor='trek',
                                  background='#00e6e6',
                                  activebackground='#009999',
                                  relief=GROOVE,
                                  font="Helvetica 20",
                                  command=self.BackBtnPressed,
                                  text="Back")
        self.back_button.place(relx=0.5, rely=0.85, anchor=CENTER)

        self.Changing = None
        self.ChangeInProgress = False

        # all keys on the keyboard are bound to the self.KeyPressed function
        self.master.bind('<Key>', self.KeyPressed)

    def KeyPressed(self, event):
        '''
        This function is used to change the control of the selected key
        '''
        if self.ChangeInProgress and event.keysym not in 'firecolursgnbiw':
            # change only if there is a ChangeInProgress
            # if we didn't have that things would constantly keep getting
            # changed. Addtionally, it also ensures that the key entered is
            # not used in any of the cheat codes
            self.ChangeInProgress = False
            # load the current key bindings
            keybindings = pickle.load(open('keybindings.p', 'rb'))
            # make sure the selected key is not already in use for something
            if '<'+event.keysym+'>' not in keybindings.values():
                # change the selected key and update the pickle file
                keybindings[self.Changing] = '<'+event.keysym+'>'
                pickle.dump(keybindings, open('keybindings.p', 'wb'))
            # re-enable all the keys
            self.moveleft_button['state'] = NORMAL
            self.moveright_button['state'] = NORMAL
            self.pause_button['state'] = NORMAL
            self.boss_button['state'] = NORMAL
            self.back_button['state'] = NORMAL
            # destroy current labels
            self.moveleftkey_label.destroy()
            self.moverightkey_label.destroy()
            self.pausekey_label.destroy()
            self.bosskey_label.destroy()
            # get the labels again with new keybindings
            self.GetCurrentKeys()

    def BackBtnPressed(self):
        '''
        Return the user to the main menu by destroying the current window
        '''
        self.master.destroy()
        BrickBreaker.run()

    def ChangeBoss(self):
        '''
        Change the boss key is pressed
        '''
        # disable all the buttons on the canvas
        self.moveleft_button['state'] = DISABLED
        self.moveright_button['state'] = DISABLED
        self.pause_button['state'] = DISABLED
        self.boss_button['state'] = DISABLED
        self.back_button['state'] = DISABLED
        self.Changing = 'boss'
        self.ChangeInProgress = True

    def ChangePause(self):
        '''
        Change the pause key is pressed
        '''
        # disable all the buttons on the canvas
        self.moveleft_button['state'] = DISABLED
        self.moveright_button['state'] = DISABLED
        self.pause_button['state'] = DISABLED
        self.boss_button['state'] = DISABLED
        self.back_button['state'] = DISABLED
        self.Changing = 'pause'
        self.ChangeInProgress = True

    def ChangeRight(self):
        '''
        Change the move right key is pressed
        '''
        # disable all the buttons on the canvas
        print('Change right pressed')
        self.moveleft_button['state'] = DISABLED
        self.moveright_button['state'] = DISABLED
        self.pause_button['state'] = DISABLED
        self.boss_button['state'] = DISABLED
        self.back_button['state'] = DISABLED
        self.Changing = 'right'
        self.ChangeInProgress = True

    def ChangeLeft(self):
        '''
        Change the move left key is pressed
        '''
        # disable all the buttons on the canvas
        print('Change left pressed')
        self.moveleft_button['state'] = DISABLED
        self.moveright_button['state'] = DISABLED
        self.pause_button['state'] = DISABLED
        self.boss_button['state'] = DISABLED
        self.back_button['state'] = DISABLED
        self.Changing = 'left'
        self.ChangeInProgress = True

    def GetCurrentKeys(self):
        '''
        Load and display all the current keys to the user
        '''
        # load the current key bindings from the pickle
        keybindings = pickle.load(open('keybindings.p', 'rb'))
        self.moveleftkey_label = Label(self.master,
                                       cursor='pirate',
                                       font='Helvetica 20',
                                       background='#006666',
                                       text=keybindings['left'][1:-1])
        self.moveleftkey_label.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.moverightkey_label = Label(self.master,
                                        cursor='pirate',
                                        font='Helvetica 20',
                                        background='#006666',
                                        text=keybindings['right'][1:-1])
        self.moverightkey_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.pausekey_label = Label(self.master,
                                    cursor='pirate',
                                    font='Helvetica 20',
                                    background='#006666',
                                    text=keybindings['pause'][1:-1])
        self.pausekey_label.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.bosskey_label = Label(self.master,
                                   cursor='pirate',
                                   font='Helvetica 20',
                                   background='#006666',
                                   text=keybindings['boss'][1:-1])
        self.bosskey_label.place(relx=0.5, rely=0.7, anchor=CENTER)


def run():
    '''
    This function is called to launch the Settings window
    '''
    root = Tk()
    app = Settings(root)
    root.mainloop()
