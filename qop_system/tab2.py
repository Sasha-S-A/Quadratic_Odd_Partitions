import const

import numpy as np
import pandas as pd
from math import *

from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Tab2Instance: 
    def SaveFile(self):
        if self.comboDraw.current():
            filename = filedialog.asksaveasfilename(filetypes=const.typePNG, defaultextension=const.typePNG)
            if filename:
                self.plot.savefig(filename, dpi=300)
        else:
            filename = filedialog.asksaveasfilename(filetypes = const.typeXLSX, defaultextension=const.typeXLSX)
            if filename:
                self.df.to_excel(filename, index=False)
            
    def ColorSelect(self, index):
        color = colorchooser.askcolor()[1]
        if not color or color == "None":
            return
        
        self.colors[index].config(bg=color)
        self.IProfile.GraphsColors[index] = color
    
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
        self.IProfile.GraphsValues[0] = 1
        self.IProfile.GraphsValues[1] = self.maxX2
        self.IProfile.GraphsValues[2] = 10
        self.IProfile.GraphsValues[3] = 0
        self.IProfile.GraphsValues[4] = self.maxY2
        self.IProfile.GraphsValues[5] = 10
        
        #==========================================================
        self.ax.set_xlim([1, self.maxX2])
        self.ax.set_ylim([0, self.maxY2])
        self.ax.xaxis.set_ticks(np.arange(1, self.maxX2 + 5, ceil((self.maxX2 - 1) / 10)))
        self.ax.yaxis.set_ticks(np.arange(0, self.maxY2 + 5, ceil(self.maxY2 / 10)))
        self.canvas.draw()
    
    def UpdateTable(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        typeDraw = self.comboType.get()
        mod8Draw = self.comboTable.current()
        depend = self.comboDepend.current()
        
        if depend:
            strWhat = 'Time'
        else:
            strWhat = 'Value'
        
        if typeDraw == 'r4(n)':
            lookData = self.IProfile.R4Data
        elif typeDraw == 'qop(n)':
            lookData = self.IProfile.QOPData   
        elif typeDraw == 'rank(n)':
            lookData = self.IProfile.RANKData 
            
        data = np.zeros((0, 0), dtype=np.uint64)
        for item in lookData:
            if mod8Draw == 0 or mod8Draw == 9:
                data = np.append(data, [item['Number'], int(item[strWhat])])
            elif mod8Draw == 8:
                if (item['Number'] % 8) == 0:
                    data = np.append(data, [item['Number'], int(item[strWhat])])
            else:
                if (item['Number'] % 8) == mod8Draw:
                    data = np.append(data, [item['Number'], int(item[strWhat])])
                
        data = data.reshape((len(data) // 2, 2))
        if depend:
            self.df = pd.DataFrame(data, columns=['n', typeDraw + ', сек.'], dtype=np.uint64)
            self.tree.heading(1, text=typeDraw + ', сек.')
        else:
            self.df = pd.DataFrame(data, columns=['n', typeDraw], dtype=np.uint64)
            self.tree.heading(1, text=typeDraw)
            
        for item in data:
            self.tree.insert('', 'end', values=("{:,}".format(int(item[0])).replace(',', ' '), \
                                                "{:,}".format(int(item[1])).replace(',', ' ')))
    def UpdateGraph(self):  
        typeDraw = self.comboType.get()
        mod8Draw = self.comboTable.current()
        depend = self.comboDepend.current()
         
        if typeDraw == 'r4(n)':
            lookData = self.IProfile.R4Data
        elif typeDraw == 'qop(n)':
            lookData = self.IProfile.QOPData
        elif typeDraw == 'rank(n)':
            lookData = self.IProfile.RANKData
          
        if depend:
            strWhat = 'Time'
        else:
            strWhat = 'Value'
        
        self.ax.clear()
        #==========================================================
        if mod8Draw == 9:
            
            self.maxX2 = 0
            self.maxY2 = 0
            
            for i in range(8):
                x = np.zeros(0, dtype=np.uint64)
                y = np.zeros(0, dtype=np.uint64)
                for item in lookData:
                    if i == 7:
                        if (item['Number'] % 8) == 0:
                            x = np.append(x, item['Number'])
                            y = np.append(y, item[strWhat])
                    else:
                        if (item['Number'] % 8) == (i+1):
                            x = np.append(x, item['Number'])
                            y = np.append(y, item[strWhat])

                tmpMaxX = np.max(x)
                tmpMaxY = np.max(y)
                if tmpMaxX > self.maxX2:
                    self.maxX2 = tmpMaxX 
                if tmpMaxY > self.maxY2:
                    self.maxY2 = tmpMaxY
                    
                self.ax.plot(x, y, linewidth=2, color=self.IProfile.GraphsColors[i], label=const.mod8table[i + 1])
        else: #==========================================================
            x = np.zeros(0, dtype=np.uint64)
            y = np.zeros(0, dtype=np.uint64)
            for item in lookData:
                if mod8Draw == 0:
                    x = np.append(x, item['Number'])
                    y = np.append(y, item[strWhat])
                elif mod8Draw == 8:
                    if (item['Number'] % 8) == 0:
                        x = np.append(x, item['Number'])
                        y = np.append(y, item[strWhat])
                else:
                    if (item['Number'] % 8) == mod8Draw:
                        x = np.append(x, item['Number'])
                        y = np.append(y, item[strWhat])
             
            if mod8Draw == 0:
                 index = 0
            else:
                 index = mod8Draw - 1
            
            self.maxX2 = np.max(x)       
            self.maxY2 = np.max(y)
            self.ax.plot(x, y, linewidth=2, color=self.IProfile.GraphsColors[index], label=self.comboTable.get())
           
        self.maxX2 = int(self.maxX2)
        self.maxY2 = int(self.maxY2)
        #==========================================================
        self.ax.set_xlabel('n')
        if depend:
            self.ax.set_ylabel(typeDraw + ", сек")
        else:
            self.ax.set_ylabel(typeDraw)
           
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
        self.IProfile.GraphsValues[0] = lim1X
        self.IProfile.GraphsValues[1] = lim2X
        self.IProfile.GraphsValues[2] = lim3
        self.IProfile.GraphsValues[3] = lim1Y
        self.IProfile.GraphsValues[4] = lim2Y
        self.IProfile.GraphsValues[5] = lim4
           
        #==========================================================
        self.ax.set_xlim([lim1X, lim2X])
        self.ax.set_ylim([lim1Y, lim2Y])
        self.ax.xaxis.set_ticks(np.arange(lim1X, lim2X + 1, step1X))
        self.ax.yaxis.set_ticks(np.arange(lim1Y, lim2Y + 1, step1Y))
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()      
        
    def Update(self):
        if self.comboDraw.current():
            self.UpdateGraph()
            self.panel2.place_forget()
            self.panel3.place(x = const.width/2 - 40, y = 0)
        else:
            self.UpdateTable()
            self.panel3.place_forget()
            self.panel2.place(x = const.width - 384, y = 0)

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
        label = Label(p1, text="Показать:")
        label.grid(row=0, column=1, sticky=W, padx=(4, 0))
        self.comboTable = ttk.Combobox(p1, values=const.mod8table)
        self.comboTable.grid(row=1, column=1, sticky=W, padx=(4, 0))
        self.comboTable.current(0)
        
        #==========================================================
        label = Label(p1, text="В зависимости:")
        label.grid(row=0, column=3, sticky=W, padx=(4, 0))
        self.comboDepend = ttk.Combobox(p1, values=const.depend)
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
        curRow = 10
        i = 0
        while i < 8:
             label = Label(p1, text="n ≡ " + str(i+1) + " (mod 8):")
             label.grid(row=curRow, column=0, sticky=W, padx=(4, 0))
             self.colors[i] = Button(p1, text="                                    ", command=lambda i=i: self.ColorSelect(i))
             self.colors[i].config(bg=self.IProfile.GraphsColors[i])
             self.colors[i].grid(row=curRow + 1, column=0, sticky=W+S, padx=(4, 0))
             
             i = i + 1
             label = Label(p1, text="n ≡ " + str(i+1) + " (mod 8):")
             label.grid(row=curRow, column=1, sticky=W, padx=(4, 0))
             self.colors[i] = Button(p1, text="                                    ", command=lambda i=i: self.ColorSelect(i))
             self.colors[i].config(bg=self.IProfile.GraphsColors[i])
             self.colors[i].grid(row=curRow + 1, column=1, sticky=W+S, padx=(4, 0))
             
             i = i + 1
             curRow += 2
            
        #==========================================================
        button = Button(p1, text="Обновить", command=self.Update)
        button.grid(row=19, column=0, sticky=W+S, padx=(4, 0), pady=(12, 0))  
        button2 = Button(p1, text="Сохранить", command=self.SaveFile)
        button2.grid(row=19, column=0, sticky=W+S, padx=(72, 0)) 
      
    def InitPanel2(self, p2):
        self.df = pd.DataFrame(columns=['n', 'r4(n)'])
        cols = list(self.df)
        
        label = Label(p2, text="Набор:")
        label.grid(row=0, column=0, sticky=W)
        
        self.tree = ttk.Treeview(p2, height=26, columns=('n', 'r4(n)'))
        self.tree.grid(row=1, column=0)
        
        self.tree.column("#0", minwidth=0, width=0, stretch=NO)
        self.tree.heading("#0", text="")
        
        self.tree.column(0, minwidth=64, width=64, stretch=NO, anchor=CENTER)
        self.tree.heading(0, text='n')
        
        self.tree.column(1, minwidth=288, width=288, stretch=NO, anchor=CENTER)
        self.tree.heading(1, text='r4(n)')
        
        scrollbar = ttk.Scrollbar(p2, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky=N+S)
    
    def InitPanel3(self, p3):
        self.plot = Figure(figsize=(5.75, 5.75), dpi=100, tight_layout=True)
        self.ax = self.plot.add_subplot(111)
        
        step1X = (self.maxX2 - self.maxX1) // self.stepX
        step1Y = (self.maxY2 - self.maxY1) // self.stepY
        
        if step1X < 1:
            step1X = 1
            
        if step1Y < 1:
            step1Y = 1
        
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
        
        self.panel2 = Frame(frame, width=376, height=const.height)
        self.panel2.place(x = const.width - 384, y = 0)
        
        self.panel3 = Frame(frame, width=const.width/2, height=const.height)
        self.panel3.place(x = const.width/2 - 40, y = 0)
        return panel1, self.panel2, self.panel3
    
    def Tab2Init(self, frame):
        p1, p2, p3 = self.InitPanels(frame)
        self.InitPanel1(p1)
        self.InitPanel2(p2)
        self.InitPanel3(p3)
        
        self.panel3.place_forget()
        
    def __init__(self, IMain, IProfile, IRoot):
        self.maxX1 = int(IProfile.GraphsValues[0])
        self.maxX2 = int(IProfile.GraphsValues[1])
        self.stepX = int(IProfile.GraphsValues[2])
        self.maxY1 = int(IProfile.GraphsValues[3])
        self.maxY2 = int(IProfile.GraphsValues[4])
        self.stepY = int(IProfile.GraphsValues[5])
        self.colors = [0, 0, 0, 0, 0, 0, 0, 0]
        self.IProfile = IProfile
        self.IRoot = IRoot
        self.Tab2Init(IMain.frame2)