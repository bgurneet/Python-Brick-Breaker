from tkinter import *
import OnePlayer
import Leaderboard

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700


class LoadGamePopup():
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
        gamename = self.nameVal.get()
        try:
            open(gamename+'.db', 'r')
            #file found
            self.master.destroy()
            self.parent.destroy()
            OnePlayer.load(gamename)
        except:
            #file not found
            msg = self.canvas.create_text((WINDOW_WIDTH/2, WINDOW_HEIGHT - 100),
                                                 text="ERROR: FILE NOT FOUND!",
                                                 font="Helvetica 20 bold italic")
        
        


class Application(object):
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
                                   text="1 Player")
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
                                  text="Settings")
        self.SettingsBtn.place(relx=0.5, rely=0.8, anchor=CENTER)
        

    def OnePlayerBtnPressed(self):
        print("One Player Pressed")
        self.master.destroy()
        OnePlayer.run()

    def LoadBtnPressed(self):
        print("Load Game Pressed")
        popup = LoadGamePopup(self.master)

    def LeaderboardBtnPressed(self):
        print("Leaderboard Pressed")
        self.master.destroy()
        Leaderboard.run()

    def SettingsBtnPressed(self):
        print("Settings Pressed")
        
        
def run():
    root = Tk()
    app = Application(root)
    root.mainloop()
