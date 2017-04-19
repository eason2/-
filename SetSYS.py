# -*- coding: utf-8 -*-

import ConfigParser
from Tkinter import *

def sys_set():
    win=Tk()
    win.title(u"系統設定")
    win.attributes('-fullscreen', True) # 全螢幕
    label=Label(win, text="lalala")
    cf = ConfigParser.ConfigParser()
    cf.read("ROI.ini")
    imageget_mode = cf.getint("R1","image_from")
    def quit2():
        win.destroy()
    def click():
        k=0
        cf = ConfigParser.ConfigParser()
        cf.read("ROI.ini")
        imageget_mode = cf.getint("R1","image_from")
        if imageget_mode == 1:
            button.configure(text="使用相機")
            button["font"] = ("Times",50,'bold italic')
            label.configure(text="目前使用資料夾相片")
            label["font"] = ("Times",50,'bold italic')
            k=1
        if imageget_mode == 2:
            button.configure(text="使用資料夾相片")
            button["font"] = ("Times",50,'bold italic')
            label.configure(text="目前使用相機")
            label["font"] = ("Times",50,'bold italic')
            k=2
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read('ROI.ini')
        if k==2:
            config.set("R1", "image_from", "1")
        if k==1:
            config.set("R1", "image_from", "2")
        config.write(open('ROI.ini', 'wb'))
    button=Button(win, text="balabala", command=click)
    if imageget_mode == 2:
        button.configure(text="使用相機")
        label.configure(text="目前使用資料夾相片")
    if imageget_mode == 1:
        button.configure(text="使用資料夾相片")
        label.configure(text="目前使用相機")
    button2=Button(win, text="Quit", command=quit2)
    button2.pack( side = BOTTOM)
    button["font"] = ("Times",50,'bold italic')
    label["font"] = ("Times",50,'bold italic')
    button2.configure(text="Quit")
    button2["font"] = ("Times",50,'bold italic')
    label.pack()
    button.pack()
    win.mainloop()

