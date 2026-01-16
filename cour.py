from tkinter import *

root = Tk()

toile = Canvas(root,bg = 'white',height = 600,width = 600)
r = toile.create_rectangle(10,10,110,110,fill = 'red')
toile.create_oval(120,10,220,110,fill = 'yellow')
toile.create_line(10,130,230,130)
toile.pack()
input('press return:')
toile.move(r,100,200)
root.mainloop()


