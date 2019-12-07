from tkinter import *

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

        #using highlightbackground instaed of just background because Macs dont support the changing of button coloura
        #additionally I wanted to ensure cross-platform functionality
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

        self.TwoPlayerBtn = Button(self.master,
                                   cursor='trek',
                                   highlightbackground='#00e6e6',
                                   relief=GROOVE,
                                   font="Helvetica 30",
                                   command=self.TwoPlayerBtnPressed,
                                   text="2 Player")
        self.TwoPlayerBtn.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.TwoPlayerBtn.bind("<Enter>", self.BtnTwoEnter)
        self.TwoPlayerBtn.bind("<Leave>", self.BtnTwoLeave)

        self.SettingsBtn = Button(self.master,
                                  cursor='trek',
                                  highlightbackground="#00e6e6",
                                  relief=GROOVE,
                                  font="Helvetica 30",
                                  command=self.SettingsBtnPressed,
                                  text="Settings")
        self.SettingsBtn.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.SettingsBtn.bind("<Enter>", self.BtnSettingsEnter)
        self.SettingsBtn.bind("<Leave>", self.BtnSettingsLeave)
        

    def OnePlayerBtnPressed(self):
        print("One Player Pressed")

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

    def SettingsBtnPressed(self):
        print("Settings Pressed")

    def BtnSettingsEnter(self, event):
        self.SettingsBtn["highlightbackground"] = "#009999"
        self.SettingsBtn["font"] = "Helvetica 30 italic"

    def BtnSettingsLeave(self, event):
        self.SettingsBtn["highlightbackground"] = "#009999"
        self.SettingsBtn["font"] = "Helvetica 30"
        
        

root = Tk()
app = Application(root)
root.mainloop()
