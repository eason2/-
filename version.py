# -*- coding: utf-8 -*-

import ConfigParser
from Tkinter import *

def show():
    win=Tk()
    win.title(u"系統提示")
    win.attributes('-fullscreen', True) # 全螢幕
    def quit2():
        win.destroy()
    mytext = "Ver1.87\n2017_04_10"
    button2=Button(win, text = mytext, command=quit2)
    button2.configure(text=mytext,fg = "red")
    button2["font"] = ("Times",40,'bold italic')
    button2.place(y=250 ,relx = 0.5,anchor = CENTER)
    win.mainloop()

if __name__ == "__main__":
	show()
