from os import path
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import tkinter.font as font
import cv2
from PIL import Image, ImageTk
import numpy as np
import tkinter.messagebox as mb


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title(f"Project")
        self.window.geometry('1200x750')
        self.window["bg"] = "gray94"
        self.window.resizable(False, False)
        self.myFont = font.Font(size=15)
        self.srez_dict = {"4":[],"3":[],"2":[],"1":[],"-1":[]}
        self.srez_count = 0
        self.need_save = False
        self.var_check = BooleanVar()

        self.btn1 = Button(self.window, text="Загрузить файл", command=self.clicked_btn1, width=20)
        self.btn1['font'] = self.myFont
        self.lbl1 = Label(self.window, text="Уровень слоя", font=("Arial Bold", 15))
        self.combo1 = Combobox(self.window)
        self.combo1['values'] = (4, 3, 2, 1, -1)
        self.combo1.configure(background="grey", font=("Arial Bold", 13))
        self.combo1.current(1)
        self.combo1.bind('<<ComboboxSelected>>', self.combo2_changed)
        self.lbl2 = Label(self.window, text="Цвет", font=("Arial Bold", 15))
        self.combo2 = Combobox(self.window)
        self.combo2['values'] = ("Зеленый", "Синий", "Красный", "Серый", "Фиолетовый", "Оранжевый", "Желтый")
        self.combo2.configure(foreground="green", font=("Arial Bold", 13))
        self.combo2.bind('<<ComboboxSelected>>', self.combo2_changed)
        self.combo2.current(0)
        self.btn2 = Button(self.window, text="Отобразить слои", command=self.clicked_btn2, width=20)
        self.btn2['font'] = self.myFont
        self.btn3 = Button(self.window, text="Сохранить результат", command=self.clicked_btn3, width=20)
        self.btn3['font'] = self.myFont
        self.canvas1 = Canvas(bg="gray94", width=512, height=220, bd=5, relief='ridge')
        self.lbl3 = Label(self.window, text="", font=("Arial Bold", 15))
        self.canvas2 = Canvas(bg="gray94", width=512, height=220, bd=5, relief='ridge')
        self.lbl4 = Label(self.window, text="", font=("Arial Bold", 15))
        self.btn4 = Button(self.window, text="Очистить результат", command=self.clicked_btn4, width=20)
        self.btn4['font'] = self.myFont
        self.lbl5 = Label(self.window, text="Уровень слоя:\n4: [M + 3σ; M + 4σ)\n3: [M + 2σ; M + 3σ)\n2: [M + σ; M + 2σ)"
                                            "\n1: [M; M + σ)\n-1: [M - σ; M)", font=("Arial Bold", 15), justify=LEFT)
        self.btn5 = Button(self.window, text="Добавить слой", command=self.clicked_btn5, width=20)
        self.btn5['font'] = self.myFont
        self.lbl6 = Label(self.window, text="", font=("Arial Bold", 15))
        self.lbl7 = Label(self.window, text="", font=("Arial Bold", 15))
        self.lbl8 = Label(self.window, text="", font=("Arial Bold", 15))
        self.lbl9 = Label(self.window, text="", font=("Arial Bold", 15))
        self.lbl10 = Label(self.window, text="", font=("Arial Bold", 15))
        self.lbl11 = Label(self.window, text="", font=("Arial Bold", 15), justify=LEFT)
        self.lbl12 = Label(self.window, text="M - Математическое ожидание яркости(у.е.)\nσ - Среднеквадратическое отклонение яркости(у.е.)",
                           font=("Arial Bold", 15), justify=LEFT)
        self.check_box = Checkbutton(text="ЧБ", font=("Arial Bold", 15), onvalue=True, offvalue=False, variable=self.var_check)

        self.btn1.place(x=35, y=600)
        self.lbl1.place(x=330, y=0)
        self.combo1.place(x=300, y=33)
        self.lbl2.place(x=610, y=0)
        self.combo2.place(x=540, y=33)
        self.btn2.place(x=940, y=75)
        self.btn3.place(x=300, y=600)
        self.canvas1.place(x=50, y=300)
        self.lbl3.place(x=200, y=250)
        self.canvas2.place(x=615, y=300)
        self.lbl4.place(x=750, y=250)
        self.btn4.place(x=940, y=125)
        self.lbl5.place(x=15, y=0)
        self.btn5.place(x=940, y=25)
        self.lbl6.place(x=615, y=540)
        self.lbl7.place(x=615, y=570)
        self.lbl8.place(x=615, y=600)
        self.lbl9.place(x=615, y=630)
        self.lbl10.place(x=615, y=660)
        self.lbl11.place(x=990, y=540)
        self.lbl12.place(x=15, y=140)
        self.check_box.place(x=750, y=25)
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.window.mainloop()

    def on_exit(self):
        if self.need_save:
            mb.showinfo("Предупреждение!", "Сохраните результат, иначе результат будет утерян!")
            self.need_save = False
        else:
            self.window.destroy()

    def combo2_changed(self, event):
        self.combo2.select_clear()
        if self.combo2.get() == "Зеленый":
            self.combo2.configure(foreground="green")
        if self.combo2.get() == "Синий":
            self.combo2.configure(foreground="blue")
        if self.combo2.get() == "Красный":
            self.combo2.configure(foreground="red")
        if self.combo2.get() == "Серый":
            self.combo2.configure(foreground="gray")
        if self.combo2.get() == "Фиолетовый":
            self.combo2.configure(foreground="purple")
        if self.combo2.get() == "Оранжевый":
            self.combo2.configure(foreground="orange")
        if self.combo2.get() == "Желтый":
            self.combo2.configure(foreground="yellow")

    def clicked_btn1(self):
        if self.need_save:
            mb.showinfo("Предупреждение!", "Сохраните результат, иначе результат будет утерян!")
            self.need_save = False
        else:
            file = filedialog.askopenfilename(filetypes=[("bmp Files", "*.bmp"), ("JPG Files", "*.JPG")])
            image = cv2.imread(f'{file}')
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.image = image[0:220]
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(image))
            self.first_img_id = self.canvas1.create_image(0, 0, anchor='nw', image=self.photo)
            self.res_image = self.image.copy()
            self.lbl3["text"] = "Исходное изображение"
            if hasattr(self, "secont_img_id"):
                self.lbl4["text"] = ""
                self.canvas2.delete(self.secont_img_id)
            self.lbl6["text"] = ""
            self.lbl7["text"] = ""
            self.lbl8["text"] = ""
            self.lbl9["text"] = ""
            self.lbl10["text"] = ""
            self.lbl11["text"] = ""
            self.srez_dict = {"4":[],"3":[],"2":[],"1":[],"-1":[]}
            self.srez_count = 0
            self.window.update_idletasks()

    def clicked_btn2(self):
        if not hasattr(self, "first_img_id"):
            mb.showerror("Ошибка", "Необходимо загрузить изображение!")
            return 0
        if self.srez_count == 0:
            mb.showerror("Ошибка", "Необходимо добавить как минимум 1 слой!")
            return 0
        if self.need_save:
            self.need_save = False
            mb.showinfo("Предупреждение!", "Сохраните результат,  иначе результат будет утерян!")
            return 0
        if hasattr(self, "image") and self.srez_count != 0:
            m_s = self.process_image()
            if hasattr(self, "secont_img_id"):
                self.canvas2.delete(self.secont_img_id)
            self.res_photo = ImageTk.PhotoImage(image=Image.fromarray(self.res_image))
            self.secont_img_id = self.canvas2.create_image(0, 0, anchor='nw', image=self.res_photo)
            self.lbl4["text"] = "Результирующее изображение"
            self.lbl11["text"] = f"M: {round(m_s[0],3)}\nσ: {round(m_s[1],3)}"
            self.window.update_idletasks()
            self.need_save = True

    def clicked_btn3(self):
        if not hasattr(self, "first_img_id"):
            mb.showerror("Ошибка", "Необходимо загрузить изображение!")
        elif not hasattr(self, "secont_img_id"):
            mb.showerror("Ошибка", "Необходимо выполнить обработку изображения!")
        else:
            dir = filedialog.asksaveasfilename(initialdir=path.dirname(__file__), defaultextension=".bmp",
                                               filetypes=[("bmp Files", ".bmp"), ("JPG Files", ".JPG")])
            self.res_image = cv2.cvtColor(self.res_image, cv2.COLOR_BGR2RGB)
            path_ar = dir.split("/")
            path_ar[-1] = "res_" + path_ar[-1]
            save_as = '/'.join(path_ar)
            print(save_as)
            cv2.imwrite(save_as, self.res_image)
            self.need_save = False

    def clicked_btn4(self):
        if self.need_save:
            self.need_save = False
            mb.showinfo("Предупреждение!", "Сохраните результат,  иначе результат будет утерян!")
            return 0
        if hasattr(self, "secont_img_id"):
            self.lbl4["text"] = ""
            self.canvas2.delete(self.secont_img_id)
            delattr(self, "secont_img_id")
        self.lbl6["text"] = ""
        self.lbl6["foreground"] = "black"
        self.lbl7["text"] = ""
        self.lbl7["foreground"] = "black"
        self.lbl8["text"] = ""
        self.lbl8["foreground"] = "black"
        self.lbl9["text"] = ""
        self.lbl9["foreground"] = "black"
        self.lbl10["text"] = ""
        self.lbl10["foreground"] = "black"
        self.lbl11["text"] = ""
        self.srez_dict = {"4": [], "3": [], "2": [], "1": [], "-1": []}
        self.srez_count = 0
        self.need_save = False
        self.res_image = self.image

    def clicked_btn5(self):
        if not hasattr(self, "first_img_id"):
            mb.showerror("Ошибка", "Необходимо загрузить изображение!")
        else:
            error = False
            for i in self.srez_dict:
                if len(self.srez_dict[i]) != 0:
                    if self.srez_dict[i][0] == "ЧБ" and not self.var_check.get()\
                            or self.srez_dict[i][0] != "ЧБ" and self.var_check.get():
                        mb.showerror("Ошибка", "Черно-белый формат не работает вместе с цветным, удалите "
                                               "выбранные слои или поставьте правильное значение для ЧБ функциональности!")
                        error = True
            if not error:
                if self.combo2.get() == "Зеленый":
                    fg = "green"
                if self.combo2.get() == "Синий":
                    fg = "blue"
                if self.combo2.get() == "Серый":
                    fg = "gray"
                if self.combo2.get() == "Фиолетовый":
                    fg = "purple"
                if self.combo2.get() == "Оранжевый":
                    fg = "orange"
                if self.combo2.get() == "Желтый":
                    fg = "yellow"
                if self.combo2.get() == "Красный":
                    fg = "red"

                if self.combo1.get() == "4":
                    if not self.var_check.get():
                        self.lbl6["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: {self.combo2.get()}"
                        self.lbl6["foreground"] = fg
                        self.srez_dict["4"] = [self.combo2.get()]
                    else:
                        self.lbl6["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: ЧБ"
                        self.srez_dict["4"] = ["ЧБ"]
                    self.srez_count += 1
                elif self.combo1.get() == "3":
                    if not self.var_check.get():
                        self.lbl7["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: {self.combo2.get()}"
                        self.lbl7["foreground"] = fg
                        self.srez_dict["3"] = [self.combo2.get()]
                    else:
                        self.lbl7["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: ЧБ"
                        self.srez_dict["3"] = ["ЧБ"]
                    self.srez_count += 1
                elif self.combo1.get() == "2":
                    if not self.var_check.get():
                        self.lbl8["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: {self.combo2.get()}"
                        self.lbl8["foreground"] = fg
                        self.srez_dict["2"] = [self.combo2.get()]
                    else:
                        self.lbl8["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: ЧБ"
                        self.srez_dict["2"] = ["ЧБ"]
                    self.srez_count += 1
                elif self.combo1.get() == "1":
                    if not self.var_check.get():
                        self.lbl9["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: {self.combo2.get()}"
                        self.lbl9["foreground"] = fg
                        self.srez_dict["1"] = [self.combo2.get()]
                    else:
                        self.lbl9["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: ЧБ"
                        self.srez_dict["1"] = ["ЧБ"]
                    self.srez_count += 1
                elif self.combo1.get() == "-1":
                    if not self.var_check.get():
                        self.lbl10["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: {self.combo2.get()}"
                        self.lbl10["foreground"] = fg
                        self.srez_dict["-1"] = [self.combo2.get()]
                    else:
                        self.lbl10["text"] = f"Уровень слоя:{self.combo1.get()} , Цвет: ЧБ"
                        self.srez_dict["-1"] = ["ЧБ"]
                    self.srez_count += 1

    def process_image(self):
        aver_bright = 0
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                aver_bright += 0.3 * self.image[i][j][0] + 0.59 * self.image[i][j][1] + 0.11 * self.image[i][j][2]
        aver_bright /= self.image.shape[0] * self.image.shape[1]
        sd_for_bright = 0
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                sd_for_bright += (0.3 * self.image[i][j][0] + 0.59 * self.image[i][j][1] + 0.11 * self.image[i][j][2] -
                                  aver_bright) ** 2
        sd_for_bright /= self.image.shape[0] * self.image.shape[1]
        sd_for_bright = sd_for_bright ** 0.5
        info_dic = {}
        for i in self.srez_dict:
            if len(self.srez_dict[i]) != 0:
                if self.srez_dict[i][0] == "Зеленый":
                    info_dic[i] = [0, 255, 0, self.image.copy()]
                elif self.srez_dict[i][0] == "Синий":
                    info_dic[i] = [0, 0, 255, self.image.copy()]
                elif self.srez_dict[i][0] == "Красный":
                    info_dic[i] = [255, 0, 0, self.image.copy()]
                elif self.srez_dict[i][0] == "Серый":
                    info_dic[i] = [128, 128, 128, self.image.copy()]
                elif self.srez_dict[i][0] == "Фиолетовый":
                    info_dic[i] = [139, 0, 255, self.image.copy()]
                elif self.srez_dict[i][0] == "Оранжевый":
                    info_dic[i] = [255, 165, 0, self.image.copy()]
                elif self.srez_dict[i][0] == "Желтый":
                    info_dic[i] = [255, 255, 0, self.image.copy()]
                elif self.srez_dict[i][0] == "ЧБ":
                    info_dic[i] = [255, 255, 255, self.image.copy()]
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                pix_bright = 0.3 * self.image[i][j][0] + 0.59 * self.image[i][j][1] + 0.11 * self.image[i][j][2]
                if "-1" in info_dic.keys():
                    if aver_bright - sd_for_bright <= pix_bright < aver_bright:
                        info_dic["-1"][-1][i][j] = [255, 255, 255]
                    else:
                        info_dic["-1"][-1][i][j] = [0, 0, 0]
                if "1" in info_dic.keys():
                    if aver_bright <= pix_bright < aver_bright + sd_for_bright:
                        info_dic["1"][-1][i][j] = [255, 255, 255]
                    else:
                        info_dic["1"][-1][i][j] = [0, 0, 0]
                if "2" in info_dic.keys():
                    if aver_bright + sd_for_bright <= pix_bright < aver_bright + 2*sd_for_bright:
                        info_dic["2"][-1][i][j] = [255, 255, 255]
                    else:
                        info_dic["2"][-1][i][j] = [0, 0, 0]
                if "3" in info_dic.keys():
                    if aver_bright + 2*sd_for_bright <= pix_bright < aver_bright + 3*sd_for_bright:
                        info_dic["3"][-1][i][j] = [255, 255, 255]
                    else:
                        info_dic["3"][-1][i][j] = [0, 0, 0]
                if "4" in info_dic.keys():
                    if aver_bright + 3*sd_for_bright <= pix_bright < aver_bright + 4*sd_for_bright:
                        info_dic["4"][-1][i][j] = [255, 255, 255]
                    else:
                        info_dic["4"][-1][i][j] = [0, 0, 0]
        flag = True
        for i in info_dic.keys():
            image = cv2.cvtColor(info_dic[i][-1], cv2.COLOR_BGR2GRAY)
            kernel = np.ones((1, 1), np.uint8)
            _, thresh_bin = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
            clean = cv2.morphologyEx(thresh_bin, cv2.MORPH_OPEN, kernel, iterations=2)
            erode = cv2.erode(clean, kernel, iterations=2)
            if self.srez_dict[i][0] == "ЧБ" and flag:
                self.res_image = cv2.cvtColor(erode, cv2.COLOR_GRAY2BGR)
                flag = False
            white_pixels = np.where(erode == 255)
            self.res_image[white_pixels] = info_dic[i][:-1]
        return [aver_bright, sd_for_bright]


app = App()
