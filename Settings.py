from tkinter import *
import pickle
import BrickBreaker

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700


class Settings():
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
                                 text="Settings")
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

        self.master.bind('<Key>', self.KeyPressed)

    def KeyPressed(self, event):
        print(event)
        if self.ChangeInProgress and event.keysym not in 'firecolursgnbiw':
            self.ChangeInProgress = False
            keybindings = pickle.load(open('keybindings.p', 'rb'))
            if '<'+event.keysym+'>' not in keybindings.values():
                keybindings[self.Changing] = '<'+event.keysym+'>'
                pickle.dump(keybindings, open('keybindings.p', 'wb'))
            self.moveleft_button['state'] = NORMAL
            self.moveright_button['state'] = NORMAL
            self.pause_button['state'] = NORMAL
            self.boss_button['state'] = NORMAL
            self.back_button['state'] = NORMAL
            self.moveleftkey_label.destroy()
            self.moverightkey_label.destroy()
            self.pausekey_label.destroy()
            self.bosskey_label.destroy()
            self.GetCurrentKeys()

    def BackBtnPressed(self):
        self.master.destroy()
        BrickBreaker.run()

    def ChangeBoss(self):
        print('Change boss pressed')
        # disable all the buttons on the canvas
        self.moveleft_button['state'] = DISABLED
        self.moveright_button['state'] = DISABLED
        self.pause_button['state'] = DISABLED
        self.boss_button['state'] = DISABLED
        self.back_button['state'] = DISABLED
        self.Changing = 'boss'
        self.ChangeInProgress = True

    def ChangePause(self):
        print('Change pause pressed')
        self.moveleft_button['state'] = DISABLED
        self.moveright_button['state'] = DISABLED
        self.pause_button['state'] = DISABLED
        self.boss_button['state'] = DISABLED
        self.back_button['state'] = DISABLED
        self.Changing = 'pause'
        self.ChangeInProgress = True

    def ChangeRight(self):
        print('Change right pressed')
        self.moveleft_button['state'] = DISABLED
        self.moveright_button['state'] = DISABLED
        self.pause_button['state'] = DISABLED
        self.boss_button['state'] = DISABLED
        self.back_button['state'] = DISABLED
        self.Changing = 'right'
        self.ChangeInProgress = True

    def ChangeLeft(self):
        print('Change left pressed')
        self.moveleft_button['state'] = DISABLED
        self.moveright_button['state'] = DISABLED
        self.pause_button['state'] = DISABLED
        self.boss_button['state'] = DISABLED
        self.back_button['state'] = DISABLED
        self.Changing = 'left'
        self.ChangeInProgress = True

    def GetCurrentKeys(self):
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
    root = Tk()
    app = Settings(root)
    root.mainloop()
