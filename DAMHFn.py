import cv2
import tkinter
import time
from tkinter import filedialog
from tkinter import *
import imutils
import numpy as np
import math
from PIL import ImageTk, Image
#import serial

#ser = serial.Serial(
#    port ='/dev/ttyAMA0',
#    baudrate = 9600,
#    parity = serial.PARITY_NONE,
#    stopbits = serial.STOPBITS_ONE,
#    bytesize = serial.EIGHTBITS,
#    timeout = 1
#)
#
Vuong = 0; HCN = 0; Tron = 0; TamGiac = 0 ; san_pham_loi = 0
shape= ""

def Che_do_chay():
    global san_pham_loi, Vuong, HCN, Tron, TamGiac
    if che_do.get() == 1:
        cap = cv2.VideoCapture(0)
        while 1:
            success, image = cap.read()
            #cv2.imshow("frame", image)
            inputimg = cv2.imwrite(filename="Rawimg.jpg", img = image)
            readimg = cv2.imread("Rawimg.jpg")
            dimg = imutils.resize(readimg,width=1000)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            processed_image = cv2.medianBlur(gray, 3)
            anh_tach_bien = cv2.Canny(processed_image, 30, 140, L2gradient=False)
            kernel = np.ones((2, 2), np.uint8)
            dilation = cv2.dilate(anh_tach_bien, kernel, iterations=1)
            im_floodfill = dilation.copy()
            h, w = dilation.shape[:2]
            mask = np.zeros((h + 2, w + 2), np.uint8)
            cv2.floodFill(im_floodfill, mask, (0, 0), 255);
            im_floodfill_inv = cv2.bitwise_not(im_floodfill)
            im_out = dilation | im_floodfill_inv
            thresh = im_out
            img_ = cv2.resize(thresh, (640, 480))
            img_resized = cv2.imwrite(filename="Load.jpg", img=img_)
            #cv2.imshow("thresh", img_)

            imageRead = cv2.imread("Load.jpg")
            _, thres = cv2.threshold(img_, 240, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            for c in contours:
                area = cv2.contourArea(c)
                # Lấy nhãn có diện tích >= 900
                if area >= 900:
                    #shape = ""
                    # Tính chu vi hình
                    peri = cv2.arcLength(c, True)
                    # Tọa độ các đỉnh
                    dinh = cv2.approxPolyDP(c, 0.04 * peri, True)
                    cv2.drawContours(imageRead, [dinh], 0, (0, 255, 0), 5)
                    x = dinh.ravel()[0]
                    y = dinh.ravel()[1] - 5
                    so_dinh = len(dinh)
                    # Phân biệt hình Vuông và hình Chữ Nhật
                    if so_dinh == 4:
                        dinh1 = dinh[0, 0, :]
                        dinh2 = dinh[1, 0, :]
                        dinh3 = dinh[2, 0, :]
                        dinh4 = dinh[3, 0, :]
                        canh_1 = math.sqrt(math.pow(dinh2[0] - dinh1[0], 2) + math.pow(dinh2[1] - dinh1[1], 2))
                        canh_2 = math.sqrt(math.pow(dinh3[0] - dinh2[0], 2) + math.pow(dinh3[1] - dinh2[1], 2))

                        # Tính Toán
                        dt_tinh_toan = canh_1 * canh_2
                        dt_thuc_te = cv2.contourArea(c)
                        ti_le_canh = canh_1 / canh_2
                        if dt_tinh_toan >= dt_thuc_te * 0.95 and dt_tinh_toan <= dt_thuc_te * 1.05:
                            if (ti_le_canh >= 0.95 and ti_le_canh <= 1.05):
                                shape = "Vuong"
                                cv2.putText(imageRead, "Vuong", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                            else:
                                shape = "HCN"
                                cv2.putText(imageRead, "HCN", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                        else:
                            shape = "san_pham_loi"

                    # Phân biệt Tam Giác
                    elif so_dinh == 3:
                        dinh1 = dinh[0, 0, :]
                        dinh2 = dinh[1, 0, :]
                        dinh3 = dinh[2, 0, :]
                        canh_1 = math.sqrt(math.pow(dinh2[0] - dinh1[0], 2) + math.pow(dinh2[1] - dinh1[1], 2))
                        canh_2 = math.sqrt(math.pow(dinh3[0] - dinh2[0], 2) + math.pow(dinh3[1] - dinh2[1], 2))
                        canh_3 = math.sqrt(math.pow(dinh1[0] - dinh3[0], 2) + math.pow(dinh1[1] - dinh3[1], 2))

                        p = (canh_1 + canh_2 + canh_3) / 2
                        dt_tam_giac = math.sqrt(p * (p - canh_1) * (p - canh_2) * (p - canh_3))
                        dt_thuc_te = cv2.contourArea(c)

                        if dt_tam_giac >= dt_thuc_te * 0.95 and dt_tam_giac <= dt_thuc_te * 1.05:
                            shape = "TamGiac"
                            cv2.putText(imageRead, "TamGiac", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                        else:
                            shape = "san_pham_loi"
                    else:
                        M = cv2.moments(c)
                        cX = int((M["m10"] / M["m00"]))
                        cY = int((M["m01"] / M["m00"]))
                        # Phân biệt hình tròn
                        so_bk_bang_nhau = 0
                        ban_kinh_mau = math.sqrt(math.pow(c[0, 0, 0] - cX, 2) + math.pow(c[0, 0, 1] - cY, 2))
                        for i in range(len(c)):
                            bk_tt = math.sqrt(math.pow(c[i, 0, 0] - cX, 2) + math.pow(c[i, 0, 1] - cY, 2))
                            if bk_tt > (ban_kinh_mau * 0.95) and bk_tt < (ban_kinh_mau * 1.05):
                                so_bk_bang_nhau = so_bk_bang_nhau + 1
                        if len(c) == so_bk_bang_nhau:
                            shape = "Tron"
                            cv2.putText(imageRead, "Tron", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                        else:
                            shape = "san_pham_loi"
            if shape == "Vuong":
                Vuong = Vuong + 1
                if Vuong == 5:
                    Vuong = 0
                # ser.write(b'Vuong')
                # ser.flush()
                # time.sleep(3)
            elif shape == "HCN":
                HCN = HCN + 1
                if HCN == 5:
                    HCN = 0
                # ser.write(b'HCN')
                # ser.flush()
                # time.sleep(3)
            elif shape == "TamGiac":
                TamGiac = TamGiac + 1
                if TamGiac == 5:
                    TamGiac = 0
                # ser.write(b'TamGiac')
                # ser.flush()
                # time.sleep(3)
            elif shape == "Tron":
                Tron = Tron + 1
                if Tron == 5:
                    Tron = 0
                #ser.write(b'Tron')
                #ser.flush()
                #time.sleep(3)
            else:
                san_pham_loi = san_pham_loi + 1
                #ser.write(b'unknown')
                #ser.flush()
                #time.sleep(3)

            print(shape)
            print(Vuong, HCN, Tron, TamGiac, san_pham_loi)
            img_resized = cv2.imwrite(filename="detected.jpg", img=imageRead)
            cv2.imshow("frame", image)
            cv2.imshow("Shapes", imageRead)
            time.sleep(2)
            if cv2.waitKey(1) == 27:
                Vuong = 0; HCN = 0; Tron = 0; TamGiac = 0; san_pham_loi = 0;
                break

        cap.release()
        cv2.destroyAllWindows()

    else:
        camera = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('FraCheck.avi', fourcc, 20.0, (640, 480))
        fourfra = cv2.VideoWriter_fourcc(*'XVID')
        outdetection = cv2.VideoWriter('FraDetection.avi', fourfra, 20.0, (640, 480))
        while (camera.isOpened()):
            ret, cam = camera.read()
            if ret == True:
                fraf = cv2.flip(cam, -1)
                fra = cv2.flip(fraf, -1)
                out.write(fra)
                #cv2.imshow('Fra', fra)
                grayfra = cv2.cvtColor(fra, cv2.COLOR_BGR2GRAY)
                processed_image_fra = cv2.medianBlur(grayfra, 3)
                tachbien_fra = cv2.Canny(processed_image_fra, 30, 140, L2gradient=False)
                kernelfra = np.ones((2, 2), np.uint8)
                dilationfra = cv2.dilate(tachbien_fra, kernelfra, iterations=1)
                fra_floodfill = dilationfra.copy()
                h, w = dilationfra.shape[:2]
                mask = np.zeros((h + 2, w + 2), np.uint8)
                cv2.floodFill(fra_floodfill, mask, (0, 0), 255);
                fra_floodfill_inv = cv2.bitwise_not(fra_floodfill)
                fra_out = dilationfra | fra_floodfill_inv
                thresh_fra = fra_out
                img_fra = cv2.resize(thresh_fra, (640, 480))
                fra_resized = cv2.imwrite(filename="FraFn.jpg", img=img_fra)
                #cv2.imshow("FraFn",fra_resized)

                imageFra = cv2.imread("FraFn.jpg")
                _, thres = cv2.threshold(img_fra, 240, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

                for c in contours:
                    area = cv2.contourArea(c)
                    # Lấy nhãn có diện tích >= 900
                    if area >= 900:
                        shape = ""
                        # Tính chu vi hình
                        peri = cv2.arcLength(c, True)
                        # Tọa độ các đỉnh
                        dinh = cv2.approxPolyDP(c, 0.04 * peri, True)
                        cv2.drawContours(imageFra, [dinh], 0, (0, 255, 0), 5)
                        x = dinh.ravel()[0]
                        y = dinh.ravel()[1] - 5
                        so_dinh = len(dinh)
                        # Phân biệt hình Vuông và hình Chữ Nhật
                        if so_dinh == 4:
                            dinh1 = dinh[0, 0, :]
                            dinh2 = dinh[1, 0, :]
                            dinh3 = dinh[2, 0, :]
                            dinh4 = dinh[3, 0, :]
                            canh_1 = math.sqrt(math.pow(dinh2[0] - dinh1[0], 2) + math.pow(dinh2[1] - dinh1[1], 2))
                            canh_2 = math.sqrt(math.pow(dinh3[0] - dinh2[0], 2) + math.pow(dinh3[1] - dinh2[1], 2))

                            # Tính Toán
                            dt_tinh_toan = canh_1 * canh_2
                            dt_thuc_te = cv2.contourArea(c)
                            ti_le_canh = canh_1 / canh_2
                            if dt_tinh_toan >= dt_thuc_te * 0.95 and dt_tinh_toan <= dt_thuc_te * 1.05:
                                if (ti_le_canh >= 0.95 and ti_le_canh <= 1.05):
                                    shape = "Vuong"
                                    cv2.putText(imageFra, "Vuong", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0),
                                                5)
                                else:
                                    shape = "HCN"
                                    cv2.putText(imageFra, "HCN", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                                (255, 0, 0), 5)
                            else:
                                shape = "san_pham_loi"

                        # Phân biệt Tam Giác
                        elif so_dinh == 3:
                            dinh1 = dinh[0, 0, :]
                            dinh2 = dinh[1, 0, :]
                            dinh3 = dinh[2, 0, :]
                            canh_1 = math.sqrt(math.pow(dinh2[0] - dinh1[0], 2) + math.pow(dinh2[1] - dinh1[1], 2))
                            canh_2 = math.sqrt(math.pow(dinh3[0] - dinh2[0], 2) + math.pow(dinh3[1] - dinh2[1], 2))
                            canh_3 = math.sqrt(math.pow(dinh1[0] - dinh3[0], 2) + math.pow(dinh1[1] - dinh3[1], 2))

                            p = (canh_1 + canh_2 + canh_3) / 2
                            dt_tam_giac = math.sqrt(p * (p - canh_1) * (p - canh_2) * (p - canh_3))
                            dt_thuc_te = cv2.contourArea(c)

                            if dt_tam_giac >= dt_thuc_te * 0.95 and dt_tam_giac <= dt_thuc_te * 1.05:
                                shape = "TamGiac"
                                cv2.putText(imageFra, "TamGiac", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                            else:
                                shape = "san_pham_loi"
                        else:
                            M = cv2.moments(c)
                            cX = int((M["m10"] / M["m00"]))
                            cY = int((M["m01"] / M["m00"]))
                            # Phân biệt hình tròn
                            so_bk_bang_nhau = 0
                            ban_kinh_mau = math.sqrt(math.pow(c[0, 0, 0] - cX, 2) + math.pow(c[0, 0, 1] - cY, 2))
                            for i in range(len(c)):
                                bk_tt = math.sqrt(math.pow(c[i, 0, 0] - cX, 2) + math.pow(c[i, 0, 1] - cY, 2))
                                if bk_tt > (ban_kinh_mau * 0.95) and bk_tt < (ban_kinh_mau * 1.05):
                                    so_bk_bang_nhau = so_bk_bang_nhau + 1
                            if len(c) == so_bk_bang_nhau:
                                shape = "Tron"
                                cv2.putText(imageFra, "Tron", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                            else:
                                shape = "san_pham_loi"


                fra_detection = cv2.flip(imageFra, 0)
                fraf_detection = cv2.flip(fra_detection,0)
                outdetection.write(fraf_detection)

            if cv2.waitKey(1) == 27:
                break
            cv2.imshow("Fra", fra)
            cv2.imshow("OutDetection", fraf_detection)
        camera.release()
        out.release()
        cv2.destroyAllWindows()

def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename

top = tkinter.Tk()
top.geometry("550x300+300+150")
top.resizable(width=True, height=True)
che_do = BooleanVar()
def open_img():
    x = openfn()
    img = Image.open(x)
    img = img.resize((360, 240), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = tkinter.Label(top, image=img)
    panel.image = img
    panel.pack()
    panel.place(x=320, y=400)

r1=Radiobutton(top,text=" Check Camera ",fg = "red",bg = "white",font = "Verdana 12 bold",variable=che_do,value=0)
r1.pack()
r1.place(x=540,y=190)

r2=Radiobutton(top,text="     Phân Loại ",fg = "#007700",bg = "white", font="Verdana 12 bold", variable=che_do, value=1)
r2.pack()
r2.place(x=540,y=220)

ld1 = tkinter.Label(top, text=" Check image ", fg="#0000ff", font="Helvetica 12 bold italic")
ld1.pack()
ld1.place(x=450, y=350)

btn = tkinter.Button(top, text=" Open image ", bg="#0fffff", font="Helvetica 12 bold italic", command=open_img)
btn.pack()
btn.place(x=342, y=220)  # x=135, y=200

l1 = tkinter.Label(top, text=" Chế Độ ", fg="black", bg="white", font="Verdana 16 bold")
l1.pack()
l1.place(x=585, y=150)

l1 = tkinter.Label(top, text=" Chương Trình ", fg="yellow", bg="#110fff", font="Verdana 20 bold")
l1.pack()
l1.place(x=400, y=1)

lc1 = tkinter.Label(top, text=" Phân loại sản phẩm theo hình dạng ", fg="yellow", bg="#110fff", font="Verdana 18 bold")
lc1.pack()
lc1.place(x=268, y=55)

RUN = tkinter.Button(top, text=" RUN ", fg="black", bg="#0fffff", font="Verdana 16 bold",command=Che_do_chay)
RUN.pack()
RUN.place(x=355, y=170)

top.title("DAMH - TS.TranHongVan - MinhMan,MinhHung,HongDao")
#top.geometry("1120x720+0+0")
top.geometry("1100x920+0+0")
top.configure(background='White')
top.mainloop()

########################################################################################################################

#def open_img():
#    x = openfn()
#    img = Image.open(x)
#    img = img.resize((360, 240), Image.ANTIALIAS)
#    img = ImageTk.PhotoImage(img)
#    panel = tkinter.Label(top, image=img)
#    panel.image = img
#    panel.pack()
#    panel.place(x=750, y=450)
#btn = tkinter.Button(top, text=" Open image ", bg="#0fffff", font="Helvetica 12 bold italic", command=open_img)

#btn.pack()
#btn.place(x=342, y=220)  # x=135, y=200

#la1 = tkinter.Label(top, text=" Output image ", fg="#0000ff", font="Helvetica 12 bold italic")
#la1.pack()
#la1.place(x=450, y=350)

#lb1 = tkinter.Label(top, text=" Input image ", fg="#0000ff", font="Helvetica 12 bold italic")
#lb1.pack()
#lb1.place(x=5, y=350)

#Stop = tkinter.Button(top, text=" Stop ", fg="black", bg="#0fffff", font="Verdana 16 bold")
#Stop.pack()
#Stop.place(x=355, y=260)
