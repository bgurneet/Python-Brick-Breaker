from tkinter import *
import OnePlayer
import Leaderboard

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

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
                                   highlightbackground='#00e6e6',
                                   relief=GROOVE,
                                   font="Helvetica 30",
                                   command=self.OnePlayerBtnPressed,
                                   text="1 Player")
        self.OnePlayerBtn.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.OnePlayerBtn.bind("<Enter>", self.BtnOneEnter)
        self.OnePlayerBtn.bind("<Leave>", self.BtnOneLeave)

        self.LoadBtn = Button(self.master,
                                   cursor='trek',
                                   highlightbackground='#00e6e6',
                                   relief=GROOVE,
                                   font="Helvetica 30",
                                   command=self.LoadBtnPressed,
                                   text="Load Game")
        self.LoadBtn.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.LoadBtn.bind("<Enter>", self.BtnLoadEnter)
        self.LoadBtn.bind("<Leave>", self.BtnLoadLeave)

        self.LeaderboardBtn = Button(self.master,
                                   cursor='trek',
                                   highlightbackground='#00e6e6',
                                   relief=GROOVE,
                                   font="Helvetica 30",
                                   command=self.LeaderboardBtnPressed,
                                   text="Leaderboard")
        self.LeaderboardBtn.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.LeaderboardBtn.bind("<Enter>", self.BtnLeaderboardEnter)
        self.LeaderboardBtn.bind("<Leave>", self.BtnLeaderboardLeave)

        self.SettingsBtn = Button(self.master,
                                  cursor='trek',
                                  highlightbackground="#00e6e6",
                                  relief=GROOVE,
                                  font="Helvetica 30",
                                  command=self.SettingsBtnPressed,
                                  text="Settings")
        self.SettingsBtn.place(relx=0.5, rely=0.8, anchor=CENTER)
        self.SettingsBtn.bind("<Enter>", self.BtnSettingsEnter)
        self.SettingsBtn.bind("<Leave>", self.BtnSettingsLeave)
        

    def OnePlayerBtnPressed(self):
        print("One Player Pressed")
        self.master.destroy()
        OnePlayer.run()


    def BtnOneEnter(self, event):
        self.OnePlayerBtn['highlightbackground'] = '#009999'
        self.OnePlayerBtn['font'] = "Helvetica 30 italic"
        
    def BtnOneLeave(self, event):
        self.OnePlayerBtn['highlightbackground'] = '#00e6e6'
        self.OnePlayerBtn['font'] = "Helvetica 30"

    def TwoPlayerBtnPressed(self):
        print("Two Player Pressed")

    def BtnTwoEnter(self, event):
        self.TwoPlayerBtn['highlightbackground'] = '#009999'
        self.TwoPlayerBtn['font'] = "Helvetica 30 italic"
        
    def BtnTwoLeave(self, event):
        self.TwoPlayerBtn['highlightbackground'] = '#00e6e6'
        self.TwoPlayerBtn['font'] = "Helvetica 30"

    def LoadBtnPressed(self):
        print("Load Game Pressed")

    def BtnLoadEnter(self, event):
        self.LoadBtn["highlightbackground"] = "#009999"
        self.LoadBtn["font"] = "Helvetica 30 italic"

    def BtnLoadLeave(self, event):
        self.LoadBtn["highlightbackground"] = "#009999"
        self.LoadBtn["font"] = "Helvetica 30"

    def LeaderboardBtnPressed(self):
        print("Leaderboard Pressed")
        Leaderboard.run

    def BtnLeaderboardEnter(self, event):
        self.LeaderboardBtn["highlightbackground"] = "#009999"
        self.LeaderboardBtn["font"] = "Helvetica 30 italic"

    def BtnLeaderboardLeave(self, event):
        self.LeaderboardBtn["highlightbackground"] = "#009999"
        self.LeaderboardBtn["font"] = "Helvetica 30"

    def SettingsBtnPressed(self):
        print("Settings Pressed")

    def BtnSettingsEnter(self, event):
        self.SettingsBtn["highlightbackground"] = "#009999"
        self.SettingsBtn["font"] = "Helvetica 30 italic"

    def BtnSettingsLeave(self, event):
        self.SettingsBtn["highlightbackground"] = "#009999"
        self.SettingsBtn["font"] = "Helvetica 30"
        
        
def run():
    root = Tk()
    app = Application(root)
    root.mainloop()
