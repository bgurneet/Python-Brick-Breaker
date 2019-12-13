from tkinter import *
import pickle
import BrickBreaker

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700


class Leaderboard(object):
    '''
    The leaderboard is displayed here

    Parameters
    ----------
    master: Tk object which will be the main menu window

    Attributes
    ----------
    self.master: The master parameter is stored here
    self.canvas: The canvas for this window
    self.BackBtn: Button that calls the self.BackBtnPressed function
    self.title_label: Label that displays the string "Leaderboard"
    self.row_title: Shows the titles of the columns in the table
    self.row_label: Displays the data for a certain row
    '''
    def __init__(self, master):
        self.master = master
        self.master.title("Brick Breaker - Leaderboard")
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master,
                             cursor='pirate',
                             width=WINDOW_WIDTH,
                             height=WINDOW_HEIGHT,
                             highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='#006666')

        self.BackBtn = Button(self.master,
                              cursor='trek',
                              background='#00e6e6',
                              activebackground='#009999',
                              relief=GROOVE,
                              font="Helvetica 30",
                              command=self.BackBtnPressed,
                              text="Main Menu")
        self.BackBtn.place(relx=0.0, rely=0.0, anchor=NW)

        self.title_label = Label(self.master,
                                 cursor='pirate',
                                 font='Helvetica 40 bold',
                                 background='#006666',
                                 activebackground='#009999',
                                 text='Leaderboard')
        self.title_label.place(relx=0.5, rely=0.25, anchor=CENTER)

        # raw_data is the 2d list of format [[username, score]]
        raw_data = pickle.load(open('leaderboard-data.p', 'rb'))
        # list gets sorted by the score of the user
        # which is the element at index 1 in every sub array of raw_data
        # this then gets reversed because we want the highest score first
        # also we are only displaying the top five scores
        sorted_data = sorted(raw_data, key=lambda x: x[1], reverse=True)[:5]

        # the column titles for the data in the table
        row_title_text = "Pos \t Name \t Score"
        currentY = 0.25 * WINDOW_HEIGHT + 50
        self.row_title = self.canvas.create_text((300, currentY),
                                                 text=row_title_text,
                                                 font='Helvetica 20')
        for (index, data) in enumerate(sorted_data):
            # number is position of the user in the leaderboard
            number = str(index+1).zfill(3)
            name = data[0][:10]
            score = str(data[1]).zfill(3)
            # all the data for this row is concatenated into one string
            row = number + '\t' + name + '\t' + score
            # each row is 50 pixels below the previous one
            currentY += 50
            # create a label with the concatenated text at the new Y value
            self.row_label = self.canvas.create_text((300, currentY),
                                                     text=row,
                                                     font='Helvetica 20')

    def BackBtnPressed(self):
        '''
        Return the user to the main menu by destroying the current window
        '''
        self.master.destroy()
        BrickBreaker.run()


def run():
    '''
    This function is called to launch the leaderboard window
    '''
    root = Tk()
    app = Leaderboard(root)
    root.mainloop()
