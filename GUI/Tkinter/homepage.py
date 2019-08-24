from tkinter import *
from tkinter.ttk import *
import time

root = Tk()
root.geometry('800x480')

# This will create style object
style = Style()

# This will be adding style, and
# naming that style variable as
# W.Tbutton (TButton is used for ttk.Button).

style.configure('W.TButton', font =
               ('arial', 10, 'bold'),
                foreground = 'red')


pbar = Progressbar(root, orient="horizontal",
                       length=200, mode="determinate")

pbar.grid(row = 2, column = 0, pady = 10, padx = 10)

# def clicked(num):
#     num = num + 1
#     pbar['value'] = num
#     root.update_idletasks()

def clicked():

    num = 0
    btn2.config(text="Stop", command = root.stopInterrupts)
    for item in range(10):
        num += 10
        pbar['value'] = num
        root.update_idletasks()
        time.sleep(2)

#
# def changeBtn():

# Style will be reflected only on
# this button because we are providing
# style only on this Button.
''' Button 1 '''
btn1 = Button(root, text = 'Quit',
                style = 'W.TButton',
             command = root.destroy)
btn1.grid(row = 0, column = 0, padx = 10)

''' Button 2 '''
btn2 = Button(root, text = 'Click me', command = clicked)
btn2.grid(row = 1, column = 0, pady = 10, padx = 10)




root.mainloop()
