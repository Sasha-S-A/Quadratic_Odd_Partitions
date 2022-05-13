import const
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog

import numpy as np
import pandas as pd
from math import *
from scipy.optimize import curve_fit

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#matplotlib.use('TkAgg')#todo???

class Tab3Instance: 
    def SaveFile(self):
        if self.comboDraw.current():
            filename = filedialog.asksaveasfilename(filetypes=const.typePNG, defaultextension=const.typePNG)
            if filename:
                self.plot.savefig(filename, dpi=300)
        else:
            filename = filedialog.asksaveasfilename(filetypes = const.typeXLSX, defaultextension=const.typeXLSX)
            if filename:
                self.df.to_excel(filename, index=False)

    def SqrtExp(self, x, a, b):
        return a * np.exp(b * np.sqrt(x))

    def ColorSelect(self, index):
        color = colorchooser.askcolor()[1]
        if not color or color == "None":
            return
        
        self.colors[index].config(bg=color)
        self.IProfile.AproxColors[index] = color
        
    def CalcVal(self, typeDraw, n):
        if typeDraw == 'r4(n)':
            lambdaVal = sqrt(n - (1/24))
            return exp((pi * lambdaVal) / sqrt(6)) / (4 * pow(lambdaVal, 3/2) * pow(24, 1/4))
        elif typeDraw == 'qop(n)':
            lambdaVal = sqrt(n - (1/24))
            r4 = exp((pi * lambdaVal) / sqrt(6)) / (4 * pow(lambdaVal, 3/2) * pow(24, 1/4))
            rank = exp(pi * sqrt(n/6)) / (4 * pow(24 * n * n * n, 1/4))
            return r4 - rank
        elif typeDraw == 'rank(n)':
            return exp(pi * sqrt(n/6)) / (4 * pow(24 * n * n * n, 1/4))
 
    def UpdateGraph(self):
        typeDraw = self.comboType.get()
        mod8Draw = self.comboTable.current()
        typeAprox = self.comboDepend.current()

        if typeDraw == 'r4(n)':
            lookData = self.IProfile.R4Data
        elif typeDraw == 'qop(n)':
            lookData = self.IProfile.QOPData
        elif typeDraw == 'rank(n)':
            lookData = self.IProfile.RANKData
          
        #==========================================================
        self.ax.clear()
        x = np.zeros(0, dtype=np.uint64)
        y = np.zeros(0, dtype=np.uint64)
        for item in lookData:
            if mod8Draw == 0:
                x = np.append(x, item['Number'])
                y = np.append(y, item['Value'])
            elif mod8Draw == 8:
                if (item['Number'] % 8) == 0:
                    x = np.append(x, item['Number'])
                    y = np.append(y, item['Value'])
            else:
                if (item['Number'] % 8) == mod8Draw:
                    x = np.append(x, item['Number'])
                    y = np.append(y, item['Value'])
         
        #==========================================================
        self.maxX2 = int(np.max(x))    
        self.maxY2 = int(np.max(y))
        self.ax.plot(x, y, linewidth=2, color=self.IProfile.AproxColors[0], label=self.comboTable.get())     
        self.ax.set_xlabel('n')
        self.ax.set_ylabel(typeDraw)
        
        #==========================================================
        if typeAprox:
            y1 = np.zeros(0, np.uint64)
            for item in x:
                y1 = np.append(y1, int(self.CalcVal(typeDraw, item)))
            
            self.ax.plot(x, y1, linewidth=1, color=self.IProfile.AproxColors[1], label=self.comboTable.get() + ' (оцен.)')
            #==========================================================
            self.text.config(state=NORMAL)
            self.text.delete('3.0', END)
            self.text.insert('3.0', '\na = ?\nb = ?')
            self.text.config(state=DISABLED)
        else:   
            inpX = np.array(x, dtype=np.longdouble)
            inpY = np.array(y, dtype=np.longdouble)
            [a, b], res1 = curve_fit(self.SqrtExp, inpX, inpY)
            y1 = a * np.exp(b * np.sqrt(x))
            self.ax.plot(x, y1, linewidth=1, color=self.IProfile.AproxColors[1], label=self.comboTable.get() + ' (аппрокс.)')
        
            #==========================================================
            self.text.config(state=NORMAL)
            self.text.delete('3.0', END)
            self.text.insert('3.0', '\na = ' + str(a) + '\nb = ' + str(b))
            self.text.config(state=DISABLED)
            
        #==========================================================
        lim1X = int(self.tbox1.get())
        lim2X = int(self.tbox1b.get())
        lim3 = int(self.tbox1c.get())
        if lim3 < 1:
            lim3 = 1
        
        step1X = (lim2X - lim1X) // lim3
        if step1X < 1:
            step1X = 1
        
        lim1Y = int(self.tbox2.get())
        lim2Y = int(self.tbox2b.get())
        lim4 = int(self.tbox2c.get())
        if lim4 < 1:
            lim4 = 1   
        
        step1Y = (lim2Y - lim1Y) // lim4
        if step1Y < 1:
            step1Y = 1
            
        if lim1X == lim2X:
            lim2X = lim2X + 1
            
        if lim1Y == lim2Y:
            lim2Y = lim2Y + 1
     
        #==========================================================
        self.IProfile.AproxValues[0] = lim1X
        self.IProfile.AproxValues[1] = lim2X
        self.IProfile.AproxValues[2] = lim3
        self.IProfile.AproxValues[3] = lim1Y
        self.IProfile.AproxValues[4] = lim2Y
        self.IProfile.AproxValues[5] = lim4
     
        #==========================================================
        self.ax.set_xlim([lim1X, lim2X])
        self.ax.set_ylim([lim1Y, lim2Y])
        self.ax.xaxis.set_ticks(np.arange(lim1X, lim2X + 1, step1X))
        self.ax.yaxis.set_ticks(np.arange(lim1Y, lim2Y + 1, step1Y))
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()
                    
    def UpdateTable(self):                    
        typeDraw = self.comboType.get()
        mod8Draw = self.comboTable.current()
        typeAprox = self.comboDepend.current()

        if typeDraw == 'r4(n)':
            lookData = self.IProfile.R4Data
        elif typeDraw == 'qop(n)':
            lookData = self.IProfile.QOPData
        elif typeDraw == 'rank(n)':
            lookData = self.IProfile.RANKData
          
        #==========================================================
        x = np.zeros(0, dtype=np.uint64)
        y = np.zeros(0, dtype=np.uint64)
        for item in lookData:
            if mod8Draw == 0:
                x = np.append(x, item['Number'])
                y = np.append(y, item['Value'])
            elif mod8Draw == 8:
                if (item['Number'] % 8) == 0:
                    x = np.append(x, item['Number'])
                    y = np.append(y, item['Value'])
            else:
                if (item['Number'] % 8) == mod8Draw:
                    x = np.append(x, item['Number'])
                    y = np.append(y, item['Value'])
         
        #==========================================================
        if typeAprox:
            typeWhat = ' оцен.'
            y1 = np.zeros(0, np.uint64)
            for item in x:
                y1 = np.append(y1, int(self.CalcVal(typeDraw, item)))
            
            #==========================================================
            self.text.config(state=NORMAL)
            self.text.delete('3.0', END)
            self.text.insert('3.0', '\na = ?\nb = ?')
            self.text.config(state=DISABLED)
        else:
            typeWhat = ' аппрокс.'
            inpX = np.array(x, dtype=np.longdouble)
            inpY = np.array(y, dtype=np.longdouble)
            [a, b], res1 = curve_fit(self.SqrtExp, inpX, inpY)
            y1 = a * np.exp(b * np.sqrt(x))
        
            #==========================================================
            self.text.config(state=NORMAL)
            self.text.delete('3.0', END)
            self.text.insert('3.0', '\na = ' + str(a) + '\nb = ' + str(b))
            self.text.config(state=DISABLED)
            
        #==========================================================
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        data = np.zeros(0)
        for i, item in enumerate(x):
            data = np.append(data, item)
            data = np.append(data, y[i])
            data = np.append(data, y1[i])
            data = np.append(data, abs(int(y[i]) - int(y1[i])))
            if int(y1[i]) == int(y[i]):
                data = np.append(data, float('{:.2f}'.format(0)))  
            elif int(y[i]) == 0:
                data = np.append(data, float('{:.2f}'.format(100)))
            else:
                data = np.append(data, float('{:.2f}'.format((100 * abs(int(y1[i]) - int(y[i]))) / int(y[i]))))
        
        data = data.reshape(len(x), 5)
        self.df = pd.DataFrame(data, columns=['n', typeDraw + ' текущ.', typeDraw + typeWhat, 'Абсол. погр.', 'Относ. погр., %'])
        self.tree.heading(1, text=typeDraw + ' текущ.')
        self.tree.heading(2, text=typeDraw + typeWhat)    
        for item in data:
            self.tree.insert('', 'end', values=("{:,}".format(int(item[0])).replace(',', ' '), \
                                            "{:,}".format(int(item[1])).replace(',', ' '),\
                                            "{:,}".format(int(item[2])).replace(',', ' '),\
                                            "{:,}".format(int(item[3])).replace(',', ' '),\
                                            str(item[4]) + ' %'))   
                   
    def Update(self):
        if self.comboDraw.current():
            self.UpdateGraph()
            self.panel2.place_forget()
            self.panel3.place(x = const.width/2 - 40, y = 0)
        else:
            self.UpdateTable()
            self.panel3.place_forget()
            self.panel2.place(x = const.width/2 - 56, y = 0)

    def AutoScale(self):
        #==========================================================
        self.tbox1.delete(0, END)
        self.tbox1.insert(0, 1)
        
        self.tbox1b.delete(0, END)
        self.tbox1b.insert(0, self.maxX2)

        self.tbox1c.delete(0, END)
        self.tbox1c.insert(0, 10)
        
        #==========================================================
        self.tbox2.delete(0, END)
        self.tbox2.insert(0, 0)
        
        self.tbox2b.delete(0, END)
        self.tbox2b.insert(0, self.maxY2)
        
        self.tbox2c.delete(0, END)
        self.tbox2c.insert(0, 10)
        
        #==========================================================
        self.IProfile.AproxValues[0] = 1
        self.IProfile.AproxValues[1] = self.maxX2
        self.IProfile.AproxValues[2] = 10
        self.IProfile.AproxValues[3] = 0
        self.IProfile.AproxValues[4] = self.maxY2
        self.IProfile.AproxValues[5] = 10
        
        #==========================================================
        self.ax.set_xlim([1, self.maxX2])
        self.ax.set_ylim([0, self.maxY2])
        self.ax.xaxis.set_ticks(np.arange(1, self.maxX2 + 5, ceil((self.maxX2 - 1) / 10)))
        self.ax.yaxis.set_ticks(np.arange(0, self.maxY2 + 5, ceil(self.maxY2 / 10)))
        self.canvas.draw()    
        
    def ValidateIfNum(self, s, S):
        valid = S == '' or S.isdigit()
        if not valid:
            self.IRoot.bell()
        return valid        
    
    def InitPanel1(self, p1): 
        #==========================================================
        label = Label(p1, text="Тип:")
        label.grid(row=0, column=0, sticky=W, padx=(4, 0))
        self.comboType = ttk.Combobox(p1, values=const.calcType)
        self.comboType.grid(row=1, column=0, sticky=W, padx=(4, 0))
        self.comboType.current(0)
        
        #==========================================================
        mod8cut = const.mod8table.copy()
        mod8cut.remove('По отдельности')
        label = Label(p1, text="Выполнить для:")
        label.grid(row=0, column=1, sticky=W, padx=(4, 0))
        self.comboTable = ttk.Combobox(p1, values=mod8cut)
        self.comboTable.grid(row=1, column=1, sticky=W, padx=(4, 0))
        self.comboTable.current(0)
        
        #==========================================================
        label = Label(p1, text="Выполнить:")
        label.grid(row=0, column=3, sticky=W, padx=(4, 0))
        self.comboDepend = ttk.Combobox(p1, values=const.typeAprox)
        self.comboDepend.grid(row=1, column=3, sticky=W, padx=(4, 0))
        self.comboDepend.current(0)        
        
        #==========================================================
        label = Label(p1, text="Отобразить:")
        label.grid(row=2, column=0, sticky=W, padx=(4, 0))
        self.comboDraw = ttk.Combobox(p1, values=const.typeDraw)
        self.comboDraw.grid(row=3, column=0, sticky=W, padx=(4, 0))
        self.comboDraw.current(0)
        
        #==========================================================
        buttonAuto = Button(p1, text="Автомасштаб", command=self.AutoScale)
        buttonAuto.grid(row=3, column=1, sticky=W+S, padx=(4, 0)) 
        
        validSpin = (self.IRoot.register(self.ValidateIfNum),'%s', '%S')
        #==========================================================
        label = Label(p1, text="Диапазон по х:")
        label.grid(row=4, column=0, sticky=W, padx=(4, 0))
        self.tbox1 = Spinbox(p1, from_= 1, to = 9999, increment = 10, width = 7, validate='all', validatecommand=validSpin)
        self.tbox1.grid(row=5, column=0, sticky=W, padx=(4, 0))
        self.tbox1.delete(0)
        self.tbox1.insert(0, self.maxX1)
        
        self.tbox1b = Spinbox(p1, from_= 1, to = 9999, increment = 10, width = 7, validate='all', validatecommand=validSpin)
        self.tbox1b.grid(row=5, column=0, sticky=W, padx=(68, 0), columnspan = (int)(const.width/2))
        self.tbox1b.delete(0)
        self.tbox1b.insert(0, self.maxX2)
        
        label = Label(p1, text="Делитель:")
        label.grid(row=6, column=0, sticky=W, pady=(4, 0), padx=(4, 0))
        self.tbox1c = Spinbox(p1, from_= 1, to = 1000, increment = 10, width = 7, validate='all', validatecommand=validSpin)
        self.tbox1c.grid(row=6, column=0, sticky=W, pady=(4, 0), padx=(64, 0), columnspan = (int)(const.width/2))
        self.tbox1c.delete(0)
        self.tbox1c.insert(0, self.stepX)
        
        #==========================================================
        label = Label(p1, text="Диапазон по у:")
        label.grid(row=7, column=0, sticky=W+S, padx=(4, 0))
        self.tbox2 = Spinbox(p1, from_=0, to = 999999999999999999, increment = 100000, width = 16, validate='all', validatecommand=validSpin)
        self.tbox2.grid(row=8, column=0, sticky=W, padx=(4, 0))
        self.tbox2.delete(0)
        self.tbox2.insert(0, self.maxY1)
        
        self.tbox2b = Spinbox(p1, from_= 0, to = 999999999999999999, increment = 100000, width = 16, validate='all', validatecommand=validSpin)
        self.tbox2b.grid(row=8, column=0, sticky=W, padx=(120, 0), columnspan = (int)(const.width/2))
        self.tbox2b.delete(0)
        self.tbox2b.insert(0, self.maxY2)
        
        label = Label(p1, text="Делитель:")
        label.grid(row=9, column=0, sticky=W, pady=(4, 0), padx=(4, 0))
        self.tbox2c = Spinbox(p1, from_= 1, to = 1000, increment = 10, width = 7, validate='all', validatecommand=validSpin)
        self.tbox2c.grid(row=9, column=0, sticky=W, pady=(4, 0), padx=(64, 0), columnspan = (int)(const.width/2))
        self.tbox2c.delete(0)
        self.tbox2c.insert(0, self.stepY)
        
        #==========================================================
        label = Label(p1, text="Цвета линии для текущего набора и аппроксимации:")
        label.grid(row=10, column=0, sticky=W, padx=(4, 0), pady=(4,0), columnspan = (int)(const.width/2))
        
        self.colors[0] = Button(p1, text="                                    ", command=lambda: self.ColorSelect(0))
        self.colors[0].config(bg=self.IProfile.AproxColors[0])
        self.colors[0].grid(row=11, column=0, sticky=W+S, padx=(4, 0))
        
        self.colors[1] = Button(p1, text="                                    ", command=lambda: self.ColorSelect(1))
        self.colors[1].config(bg=self.IProfile.AproxColors[1])
        self.colors[1].grid(row=11, column=1, sticky=W+S, padx=(4, 0))
    
        #==========================================================
        button = Button(p1, text="Выполнить", command=self.Update)
        button.grid(row=12, column=0, sticky=W, padx=(4, 0), pady=(12, 0)) 
        button2 = Button(p1, text="Сохранить", command=self.SaveFile)
        button2.grid(row=12, column=0, sticky=W+S, padx=(80, 0)) 
        
        #==========================================================
        self.text = Text(p1, width=60, height=4)
        self.text.grid(row=13, column=0, padx=(4, 0), pady=(12, 0), columnspan = (int)(const.width/2))
        self.text.insert('1.0', "Получившиеся значения для уравнения вида:\n"+
                    "y(n) = a * exp(b * sqrt(n))\n" +
                    "a = ?\nb = ?")
        self.text.config(state=DISABLED)
        
        text2 = Text(p1, width=60, height=5)
        text2.grid(row=14, column=0, padx=(4, 0), pady=(12, 0), columnspan = (int)(const.width/2))
        text2.insert('1.0', "Для сравнения с известной ипользуются следующий формулы:\n"+
                    "Для rank(n): exp(π*√(n/6)) / (4*∜(24 * n³))\n" +
                    "Для r4(n): exp((π*λ(n))/√6) / (4*√(λ³(n))*∜24)\n" +
                    "λ(n) = √(n - 1/24)\n" +
                    "Для qop(n): r4(n) - rank(n)")
        text2.config(state=DISABLED)        

    def InitPanel2(self, p2):
        self.df = pd.DataFrame(columns=['n', 'r4(n) текущ.', 'r4(n) аппрокс.', 'Абсол. погр.', 'Относ. погр.'])
        cols = list(self.df)
        
        label = Label(p2, text="Результаты:")
        label.grid(row=0, column=0, sticky=W)
        
        self.tree = ttk.Treeview(p2, height=26, columns=('n', 'r4(n) текущ.', 'r4(n) аппрокс.', 'Абсол. погр.', 'Относ. погр.'))
        self.tree.grid(row=1, column=0)
        
        self.tree.column("#0", minwidth=0, width=0, stretch=NO)
        self.tree.heading("#0", text="")
        
        self.tree.column(0, minwidth=56, width=56, stretch=NO, anchor=CENTER)
        self.tree.heading(0, text='n')
        
        self.tree.column(1, minwidth=144, width=144, stretch=NO, anchor=CENTER)
        self.tree.heading(1, text='r4(n) текущ.')
 
        self.tree.column(2, minwidth=144, width=144, stretch=NO, anchor=CENTER)
        self.tree.heading(2, text='r4(n) аппрокс.')       

        self.tree.column(3, minwidth=144, width=144, stretch=NO, anchor=CENTER)
        self.tree.heading(3, text='Абсол. погр.')        

        self.tree.column(4, minwidth=72, width=72, stretch=NO, anchor=CENTER)
        self.tree.heading(4, text='Относ. погр.')  

        scrollbar = ttk.Scrollbar(p2, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky=N+S)
    
    def InitPanel3(self, p3):
        self.plot = Figure(figsize=(5.75, 5.75), dpi=100, tight_layout=True)
        self.ax = self.plot.add_subplot(111)
        
        step1X = (self.maxX2 - self.maxX1) // self.stepX
        step1Y = (self.maxY2 - self.maxY1) // self.stepY
        
        self.ax.set_xlim([self.maxX1, self.maxX2])
        self.ax.set_ylim([self.maxY1, self.maxY2])
        self.ax.xaxis.set_ticks(np.arange(self.maxX1, self.maxX2 + 1, step1X))
        self.ax.yaxis.set_ticks(np.arange(self.maxY1, self.maxY2 + 1, step1Y))
        self.ax.set_xlabel('n')
        self.ax.set_ylabel('r4(n)')
        self.ax.grid(True)
        
        self.canvas = FigureCanvasTkAgg(self.plot, p3)
        self.canvas.get_tk_widget().pack()
    
    def InitPanels(self, frame):
        panel1 = Frame(frame, width=const.width/2, height=const.height)
        panel1.place(x = 0, y = 0)
        
        self.panel2 = Frame(frame, width=const.width/2, height=const.height)
        self.panel2.place(x = const.width/2 - 56, y = 0)
        
        self.panel3 = Frame(frame, width=const.width/2, height=const.height)
        self.panel3.place(x = const.width/2 - 40, y = 0)
        return panel1, self.panel2, self.panel3
    
    def Tab3Init(self, frame):
        p1, p2, p3 = self.InitPanels(frame)
        self.InitPanel1(p1)
        self.InitPanel2(p2)
        self.InitPanel3(p3)
        
        self.panel3.place_forget()
        
    def __init__(self, IMain, IProfile, IRoot):
        self.maxX1 = int(IProfile.AproxValues[0])
        self.maxX2 = int(IProfile.AproxValues[1])
        self.stepX = int(IProfile.AproxValues[2])
        self.maxY1 = int(IProfile.AproxValues[3])
        self.maxY2 = int(IProfile.AproxValues[4])
        self.stepY = int(IProfile.AproxValues[5])
        self.colors = [0, 0]
        self.IProfile = IProfile
        self.IRoot = IRoot
        self.Tab3Init(IMain.frame3)