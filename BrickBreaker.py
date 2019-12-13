from tkinter import *
import OnePlayer
import Leaderboard
import Settings

# constants are declared here
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700


class LoadGamePopup():
    '''
    Creates a popup that allows the user to enter the filename of the game
    that they would like to load.

    Parameters
    ----------
    master: Tk() object that this popup belongs to

    Attributes:
    self.parent: the master parameter is stored here
    self.master: the popup window
    self.canvas: the canvas for the popup window
    self.name: Label thats says "Filename:"
    self.nameVal: Entry object that allows the user to enter filename
    self.enter: Button that calls self.LoadGame() when clicked on
    '''
    def __init__(self, master):
        self.parent = master
        self.master = Toplevel(master)
        self.master.title("Load Game")
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master,
                             cursor='pirate',
                             width=200,
                             height=400,
                             highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='#006666')
        self.name = Label(self.master, text="Filename:")
        self.name.place(relx=0.5, rely=0.0, anchor=N)
        self.nameVal = Entry(self.master)
        self.nameVal.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.enter = Button(self.master, text='Open', command=self.LoadGame)
        self.enter.place(relx=0.5, rely=0.4, anchor=CENTER)

    def LoadGame(self):
        '''
        Used to open the game with the loaded contents
        '''
        # get the filename entered by the user
        gamename = self.nameVal.get()
        try:
            # first check if a file with such a name exists in the current
            # working directory
            open(gamename+'.db', 'r')
            # file found
            # destory main menu and the popup
            self.master.destroy()
            self.parent.destroy()
            # load the game
            OnePlayer.load(gamename)
        except:
            # file not found
            # display an appropriate error message
            msg = self.canvas.create_text((100, 300),
                                          text="ERROR: FILE NOT FOUND!",
                                          font="Helvetica 10 bold italic")


class Application(object):
    '''
    The main menu of the game

    Parameters
    ----------
    master: Tk object which will be the main menu window

    Attributes
    ----------
    self.master: the master parameter is stored here
    self.canvas: the Canvas for the main menu window
    self.title_label: Displays the title of the game in a Label
    self.OnePlayerBtn: Calls the self.OnePlayerBtnPressed function when pressed
    self.LoadBtn: calls the self.LoadBtnPressed function when pressed
    self.LeaderboardBtn: calls the self.LeaderboardBtnPressed function
    self.SettingsBtn: calls the self.SettingsBtnPressed function
    '''
    def __init__(self, master):
        self.master = master
        self.master.title("Brick Breaker - Menu")
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
                                 font='Helvetica 40 bold',
                                 background='#006666',
                                 text="BRICK\nBREAKER")
        self.title_label.place(relx=0.5, rely=0.25, anchor=CENTER)

        self.OnePlayerBtn = Button(self.master,
                                   cursor='trek',
                                   background='#00e6e6',
                                   activebackground='#009999',
                                   relief=GROOVE,
                                   font="Helvetica 30",
                                   command=self.OnePlayerBtnPressed,
                                   text="Play")
        self.OnePlayerBtn.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.LoadBtn = Button(self.master,
                              cursor='trek',
                              background='#00e6e6',
                              activebackground='#009999',
                              relief=GROOVE,
                              font="Helvetica 30",
                              command=self.LoadBtnPressed,
                              text="Load Game")
        self.LoadBtn.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.LeaderboardBtn = Button(self.master,
                                     cursor='trek',
                                     background='#00e6e6',
                                     activebackground='#009999',
                                     relief=GROOVE,
                                     font="Helvetica 30",
                                     command=self.LeaderboardBtnPressed,
                                     text="Leaderboard")
        self.LeaderboardBtn.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.SettingsBtn = Button(self.master,
                                  cursor='trek',
                                  background='#00e6e6',
                                  activebackground='#009999',
                                  relief=GROOVE,
                                  font="Helvetica 30",
                                  command=self.SettingsBtnPressed,
                                  text="Controls")
        self.SettingsBtn.place(relx=0.5, rely=0.8, anchor=CENTER)

    def OnePlayerBtnPressed(self):
        '''
        Destroys the current window and launches the game
        '''
        self.master.destroy()
        OnePlayer.run()

    def LoadBtnPressed(self):
        '''
        Opens the LoadGamePopup on top of the current window
        '''
        popup = LoadGamePopup(self.master)

    def LeaderboardBtnPressed(self):
        '''
        Destroys the current window and opens the leaderboard
        '''
        self.master.destroy()
        Leaderboard.run()

    def SettingsBtnPressed(self):
        '''
        Destroys the current window and opens the settings
        '''
        self.master.destroy()
        Settings.run()


def run():
    '''
    This function is called to launch the main menu window
    '''
    root = Tk()
    app = Application(root)
    root.mainloop()
