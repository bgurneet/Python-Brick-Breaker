from tkinter import *
import pickle

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

#test = [['', 100], ['Gurneet', 90], ['Haikal', 110], ['Zeynep', 60], ['Greta', 120], ['Pedro', 40]]

class Leaderboard(object):
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
                                   highlightbackground='#00e6e6',
                                   relief=GROOVE,
                                   font="Helvetica 30",
                                   command=self.BackBtnPressed,
                                   text="1 Player")
        self.BackBtn.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.BackBtn.bind("<Enter>", self.BtnBackEnter)
        self.BackBtn.bind("<Leave>", self.BtnBackLeave)

        self.title_label = Label(self.master,
                                 cursor='pirate',
                                 font='Helvetica 40 bold',
                                 background='#006666',
                                 text='Leaderboard')
        self.title_label.place(relx=0.5, rely=0.25, anchor=CENTER)

        raw_data = pickle.load(open('leaderboard-data.p', 'rb'))
        sorted_data = sorted(raw_data, key=lambda x: x[1], reverse=True)[:10]

        row_title_text = "Num \t Name \t Score"
        currentY = 0.25 * WINDOW_HEIGHT + 50
        self.row_title = self.canvas.create_text((300, currentY),
                                                 text=row_title_text,
                                                 font='Helvetica 20')
        for (index, data) in enumerate(sorted_data):
            number = str(index+1).zfill(3)#.zfill(3)[:4]
            name = data[0][:10]#.ljust(10)[:10]
            score = str(data[1]).zfill(3)#.ljust(10)[:10]
            row = number +'\t'+ name +'\t'+ score
            currentY += 50
            self.row_label = self.canvas.create_text((300, currentY),
                                                     text=row,
                                                     font='Helvetica 20')

    #def BackBtnPressed(self):
        
            
            
            
        




def run():
    root = Tk()
    app = Leaderboard(root)
    root.mainloop()
