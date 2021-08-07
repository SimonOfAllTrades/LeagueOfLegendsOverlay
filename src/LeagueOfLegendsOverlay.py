from tkinter import *

root = Tk()
root.attributes('-topmost', True)
for i in range(10):
    hero_button = Button(
        root,
        text="Hero {}".format(i)
    )
    
    hero_button.config(height = 5, width = 10)
    hero_button.grid(column = i, row = 0)

root.mainloop()