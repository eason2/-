# -*- coding: utf-8 -*-

import ConfigParser
import cv2
import numpy as np
import os
import time
import Dialog
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
global client , start_getPicture,num
start_getPicture = 0
client = ModbusClient(method = "rtu", port = "COM2",stopbits = 1,bytesize=8,parity='N',baudrate=19200,timeout=0.04)
ddd = True
num = 0
video = cv2.VideoCapture(0)

video.set(3,1280)
video.set(4,1024)
def click_and_crop2(event, x, y, flags, param):
    global ddd,start_getPicture
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.destroyWindow("openCV")
        ddd=False
        rq = client.write_registers(0x78,[2266],unit=0x01) #R120
        rq = client.write_registers(0x7e,[2266],unit=0x01) #R126
        rq = client.write_registers(0x80,[0],unit=0x01) #R128
        start_getPicture = 0

def updateImage():  # match display
    global ddd , start_getPicture , num
    t1=time.time()
    cf = ConfigParser.ConfigParser()
    cf.read("ROI.ini")
    delaytime = cf.getint("R1","key_delaytime_1")
    imageget_mode = cf.getint("R1","image_from")
    PictureNumber = cf.getint("R1","pic_num")
    font = cv2.FONT_HERSHEY_SIMPLEX # 文字
    client.write_registers(0x78,[9090],unit=0x01)
    if imageget_mode == 1:    # 相機
        try:
            ret, frame = video.read()
            color_image = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = gray.copy()
        except:
            cv2.destroyWindow("openCV")
            ddd=False
            rq = client.write_registers(0x78,[2266],unit=0x01)
            Dialog.show("尚未連接相機。\nUSB3 not conneted.")
            return
        cf = ConfigParser.ConfigParser()
        cf.read("ROI.ini")
        y11 = cf.getint("R1","key_y1_image_1")
        y21 = cf.getint("R1","key_y2_image_1")
        x11 = cf.getint("R1","key_x1_image_1")
        x21 = cf.getint("R1","key_x2_image_1")
        y12 = cf.getint("R1","key_y1_image_2")
        y22 = cf.getint("R1","key_y2_image_2")
        x12 = cf.getint("R1","key_x1_image_2")
        x22 = cf.getint("R1","key_x2_image_2")
        myscore1 = cf.getint("R1","score1")
        myscore2 = cf.getint("R1","score2")
        Delay102 = cf.getint("R1","delay102")
        Delay104 = cf.getint("R1","delay104")
        try:
            result = client.read_holding_registers( 0x64 ,21,unit=0x01)
            ru = result.registers
        except:
            cv2.destroyWindow("openCV")
            ddd=False
            rq = client.write_registers(0x78,[2266],unit=0x01)
            Dialog.show("尚未連接機台。\n COM2 not conneted.")
            return
        signal1 = ru[2]
        signal2 = ru[4]
        if signal1 == 102: # 接收到102拍照訊號
            if Delay102 >0: # 延遲時間
                cv2.waitKey(Delay102)
            if start_getPicture == 102: # 取得102相片訊號 取得相片 結束
                cv2.imwrite("102.png",color_image)
                cv2.destroyWindow("openCV")
                ddd=False
                rq = client.write_registers(0x78,[2266],unit=0x01)
                start_getPicture = 0
                return
            elif start_getPicture == 104: # 取得104相片訊號 直接OK
                client.write_registers(0x7a,[9090],unit=0x01) # OK
            else: # 進行檢測
                try: # 獲取樣本
                    template1 = cv2.cvtColor(cv2.imread("ROI1.png"),cv2.COLOR_BGR2GRAY)
                    Image102 = cv2.cvtColor(cv2.imread("102.png"),cv2.COLOR_BGR2GRAY)
                except:# 錯誤 離開 跳出訊息
                    cv2.destroyWindow("openCV")
                    ddd=False
                    rq = client.write_registers(0x78,[2266],unit=0x01)
                    rq = client.write_registers(0x7e,[2266],unit=0x01)
                    Dialog.show("閉模前樣本錯誤，請重新選取樣本。\nTemplate error,please reset template.")
                    return
                try:
                    try:# 取得拍照相片中的檢測範圍(ROI)
                        w, h = template1.shape[::-1]
                        if y21<y11: y11,y21 = y21,y11
                        if x21<x11: x11,x21 = x21,x11
                        y11 = y11-10
                        if y11 <= 0: y11 = 0
                        y21 = y21+10
                        x11 = x11-10
                        if x11 <= 0: x11 = 0
                        x21 = x21+10 
                        print y11,',',y21,',',x11,',',x21
                        myROI = img[y11:y21,x11:x21]    # ROI
                    except:# 錯誤 離開 跳出訊息
                        cv2.destroyWindow("openCV")
                        ddd=False
                        rq = client.write_registers(0x78,[2266],unit=0x01)
                        rq = client.write_registers(0x7e,[2266],unit=0x01)
                        Dialog.show("1021.ROI錯誤，請重新框選檢測範圍。\nROI error.")
                    # MatchTemplate
                    res = cv2.matchTemplate(template1,myROI,method= eval('cv2.TM_CCOEFF_NORMED'))  # 比對ROI與template error
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                    score = round(max_val*1000,0) # 分數
                    if score <= 0: score = 0 # 分數小於0 => 0
                    if score < myscore1: # 分數比對 NG
                        cv2.imwrite("D:/todocv/imm/pic/"+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'-'+str(score)+"_NG_102.png",color_image)
                        cv2.imwrite("D:/todocv/imm/NGpic/"+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'-'+str(score)+"_NG_102.png",color_image)
                    else: # 分數比對 OK
                        cv2.imwrite("D:/todocv/imm/pic/"+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'-'+str(score)+"_OK_102.png",color_image)
                    top_left = (max_loc[0]+x11,max_loc[1]+y11)
                    bottom_right = (top_left[0]+w, top_left[1]+h)
                    if score < myscore1:# NG
                        ###  不一樣的地方=>畫出紅點
                        color_image = NG_show_Different(color_image,Image102,myROI,y11,x11,max_loc[0],max_loc[0],y21-y11,x21-x11)
                        cv2.putText(color_image,"NG",(0,img.shape[1]-380), font, 4,(0,0,255),8,cv2.LINE_AA) # 文字
                        client.write_registers(0x7a,[2266],unit=0x01) # NG訊號
                    else: # OK
                        cv2.putText(color_image,"OK",(0,img.shape[1]-380), font, 4,(0,255,0),8,cv2.LINE_AA) # 文字
                        client.write_registers(0x7a,[9090],unit=0x01) # OK訊號        
                    cv2.rectangle(color_image,(x11,y11),(x21,y21),(255,255,0),2)       # 框框
                    cv2.putText(color_image,str(score),(400,img.shape[1]-380), font, 4,(255,100,0),8,cv2.LINE_AA)
                    t2=time.time()-t1 # 總共花費時間
                    cv2.putText(color_image,"open  time:"+str(round(t,4)),(50,50), font, 1.5,(255,100,100),3,cv2.LINE_AA) # 文字
                    cv2.namedWindow("openCV", cv2.WND_PROP_FULLSCREEN)
                    cv2.setWindowProperty("openCV", cv2.WND_PROP_FULLSCREEN,True) # 螢幕最大化
                    cv2.imshow("openCV",color_image)
                    cv2.setMouseCallback("openCV", click_and_crop2) # add event
                    if score < myscore1: # NG 
                        cv2.waitKey(0)
                    else:                # OK 顯示 0.7 秒
                        cv2.waitKey(700)
                except: # 錯誤 離開 顯示訊息
                    cv2.destroyWindow("openCV")
                    ddd=False
                    rq = client.write_registers(0x78,[2266],unit=0x01)
                    rq = client.write_registers(0x7e,[2266],unit=0x01)
                    Dialog.show("1022.ROI錯誤，請從新框選檢測範圍。\nROI Error.")
        elif signal2 == 104:
            if Delay104 >0: # 延遲時間
                cv2.waitKey(Delay104)
            if start_getPicture == 104:
                cv2.imwrite("104.png",color_image)
                cv2.destroyWindow("openCV")
                ddd=False
                rq = client.write_registers(0x78,[2266],unit=0x01) # close
                start_getPicture = 0
                return
            elif start_getPicture == 102:
                client.write_registers(0x7c,[9090],unit=0x01)  # OK
            else:
                try:
                    template2 = cv2.cvtColor(cv2.imread("ROI2.png"),cv2.COLOR_BGR2GRAY)  # template
                    Image104 = cv2.cvtColor(cv2.imread("104.png"),cv2.COLOR_BGR2GRAY)  # template
                except:
                    cv2.destroyWindow("openCV")
                    ddd=False
                    rq = client.write_registers(0x78,[2266],unit=0x01)
                    rq = client.write_registers(0x7e,[2266],unit=0x01)
                    Dialog.show("開模後樣本錯誤，請從新選取樣本。\nTemplate Error,Please reset template.")
                    return
                try:
                    try:
                        w, h = template2.shape[::-1]
                        if y22<y12: y12,y22 = y22,y12
                        if x22<x12: x12,x22 = x22,x12
                        y12 = y12-10
                        if y12 <= 0: y12 = 0
                        y22 = y22+10
                        x12 = x12-10
                        if x12 <= 0: x12 = 0                            
                        x22 = x22+10
                        myROI = img[y12:y22,x12:x22]    # ROI
                    except:
                        cv2.destroyWindow("openCV")
                        ddd=False
                        rq = client.write_registers(0x78,[2266],unit=0x01)
                        rq = client.write_registers(0x7e,[2266],unit=0x01)
                        Dialog.show("1041.ROI錯誤，請從新框選檢測範圍。\nROI error.")
                    res = cv2.matchTemplate(template2,myROI,method= eval('cv2.TM_CCOEFF_NORMED'))  # 比對ROI與template error
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                    score = max_val*1000
                    if score <=0: score = 0
                    score = round(score,0)
                    if score < myscore2:
                        cv2.imwrite("D:/todocv/imm/pic/"+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'-'+str(score)+"_NG_104.png",color_image)
                        cv2.imwrite("D:/todocv/imm/NGpic/"+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'-'+str(score)+"_NG_104.png",color_image)
                    else:
                        cv2.imwrite("D:/todocv/imm/pic/"+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'-'+str(score)+"_OK_104.png",color_image)
                    top_left = (max_loc[0]+x12,max_loc[1]+y12)
                    bottom_right = (top_left[0]+w, top_left[1]+h)
                    if score < myscore2:
                        Show_Error_Image = NG_show_Different(color_image,Image104,myROI,y12,x12,max_loc[0],max_loc[0],y22-y12,x22-x12)
                        color_image = Show_Error_Image
                        cv2.putText(color_image,"NG",(0,img.shape[1]-380), font, 4,(0,0,255),8,cv2.LINE_AA) # 文字
                        client.write_registers(0x7c,[2266],unit=0x01) # NG
                    else:
                        cv2.putText(color_image,"OK",(0,img.shape[1]-380), font, 4,(0,255,0),8,cv2.LINE_AA) # 文字
                        client.write_registers(0x7c,[9090],unit=0x01) # OK
                    cv2.rectangle(color_image,(x12,y12),(x22,y22),(255,255,0),2)       # 框框
                    cv2.putText(color_image,str(score),(400,img.shape[1]-380), font, 4,(255,100,0),8,cv2.LINE_AA)
                    t2=time.time()
                    t=t2-t1
                    cv2.putText(color_image,"close  time:"+str(round(t,4)),(50,50), font, 1.5,(255,100,100),3,cv2.LINE_AA) # 文字
                    cv2.namedWindow("openCV", cv2.WND_PROP_FULLSCREEN)
                    cv2.setWindowProperty("openCV", cv2.WND_PROP_FULLSCREEN,True) # 螢幕最大化
                    cv2.imshow("openCV",color_image)
                    cv2.setMouseCallback("openCV", click_and_crop2)
                    if score < myscore2:
                        cv2.waitKey(0)
                    else:
                        cv2.waitKey(700)
                except:
                    cv2.destroyWindow("openCV")
                    ddd=False
                    rq = client.write_registers(0x78,[2266],unit=0x01)
                    rq = client.write_registers(0x7e,[2266],unit=0x01)
                    Dialog.show("1042.ROI錯誤，請從新框選檢測範圍。\nROI Error.")
        else: # 沒接收到102 104 訊號
            num = num + 1
            if start_getPicture == 102 or start_getPicture == 104:
                if num == 1: cv2.putText(color_image,"get picture.",(500,img.shape[1]-380), font, 3,(255,100,0),6,cv2.LINE_AA)
                elif num == 2: cv2.putText(color_image,"get picture..",(500,img.shape[1]-380), font, 3,(255,100,0),6,cv2.LINE_AA)
                else : cv2.putText(color_image,"get picture...",(500,img.shape[1]-380), font, 3,(255,100,0),6,cv2.LINE_AA)
            else:
                if num == 1: cv2.putText(color_image,"CCD Checking.",(500,img.shape[1]-380), font, 3,(255,100,0),6,cv2.LINE_AA)
                elif num == 2: cv2.putText(color_image,"CCD Checking..",(500,img.shape[1]-380), font, 3,(255,100,0),6,cv2.LINE_AA)
                else: cv2.putText(color_image,"CCD Checking...",(500,img.shape[1]-380), font, 3,(255,100,0),6,cv2.LINE_AA)
            cv2.putText(color_image,"102:"+str(signal1),(10,40), font, 0.8,(255,100,0),2,cv2.LINE_AA)
            cv2.putText(color_image,"104:"+str(signal2),(10,60), font, 0.8,(255,100,0),2,cv2.LINE_AA)
            cv2.putText(color_image,"120:"+str(ru[20]),(10,80), font, 0.8,(255,100,0),2,cv2.LINE_AA)
            cv2.namedWindow("openCV", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("openCV", cv2.WND_PROP_FULLSCREEN,True) # 螢幕最大化
            cv2.imshow("openCV",color_image)
            cv2.setMouseCallback("openCV", click_and_crop2)
            if num == 3: num = 0
    if ru[20] == 0: # 避免離開檢測模式後又會再進來一次
        cv2.destroyWindow("openCV")
        ddd=False
        rq = client.write_registers(0x78,[2266],unit=0x01)
        rq = client.write_registers(0x7e,[2266],unit=0x01)
        start_getPicture = 0
    # 設定相片的數量
    if len(os.listdir('D:/todocv/imm/pic')) > PictureNumber:
        o='D:/todocv/imm/pic/'+os.listdir('D:/todocv/imm/pic')[0]
        os.remove(o)

# 以紅點畫出兩張圖片不同的地點
def NG_show_Different(colorImage,Image,ROI,pos_y,pos_x,offset_y,offset_x,size_y,size_x):
    #~ print 'pos_x:',pos_x
    #~ print 'pos_y:',pos_y
    #~ print 'offset_x:',offset_x
    #~ print 'offset_y:',offset_y
    #~ print 'size_x:',size_x
    #~ print 'size_y:',size_y
    #~ pos_y += offset_x
    #~ pos_x += offset_y
    mtemplate = Image[pos_y:pos_y+size_y,pos_x:pos_x+size_x]
    #~ cv2.imshow('1',mtemplate)
    #~ cv2.waitKey(0)
    print mtemplate.shape[::-1]
    print ROI.shape[::-1]
    #~ i1 = cv2.adaptiveThreshold(mtemplate, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)
    #~ i2 = cv2.adaptiveThreshold(ROI, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)
    a1, i1 = cv2.threshold(mtemplate, 40, 255, cv2.THRESH_BINARY) 
    a2, i2 = cv2.threshold(ROI, 40, 255, cv2.THRESH_BINARY) 
    #~ d = cv2.absdiff(mtemplate, ROI) # 相減
    d = cv2.absdiff(i1, i2) # 相減
    #~ cv2.imshow('i1',i1)
    #~ cv2.imshow('i2',i2)
    #~ cv2.imshow('mtemplate',mtemplate)
    #~ cv2.imshow('ROI',ROI)
    #~ cv2.imshow('d',d)
    #~ cv2.waitKey(0)
    ca=0
    cb=0
    cc=0
    mx = pos_x
    my = pos_y
    #~ print 'd:',d
    for i in d: # 畫紅點
        #~ print 'i:',i
        for j in i:
            #~ print 'j:',j
            #~ if j[0] <> 0 or j[1] <> 0 or j[2] <> 0:
            if j > 30:
                #~ cv2.circle(colorImage,(my+cb,mx+ca), 1, (0,0,255), -1)
                cv2.circle(colorImage,(mx+cb,my+ca), 1, (0,0,255), -1)
            cb +=1
        cb=0
        ca +=1
    return colorImage

if __name__ == "__main__":
    while ddd:
        updateImage()
