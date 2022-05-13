import const
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

class Tab1Instance: 
    def UpdateResults(self):
        if len(self.IProfile.R4Data):
            self.buttonR4.config(state=NORMAL)
        else:
            self.buttonR4.config(state=DISABLED)
 
        if len(self.IProfile.QOPData):
            self.buttonQOP.config(state=NORMAL)
        else:
            self.buttonQOP.config(state=DISABLED)
            
        if len(self.IProfile.RANKData):
            self.buttonRank.config(state=NORMAL)
        else:
            self.buttonRank.config(state=DISABLED)   

    def Print(self, typeLoad):
        self.textOut.config(state=NORMAL)
        self.textOut.delete('1.0', END)
        if typeLoad == const.FOR_R4:
            self.textOut.insert('1.0', self.IProfile.DataPrint(self.IProfile.R4Data))
        elif typeLoad == const.FOR_QOP:
            self.textOut.insert('1.0', self.IProfile.DataPrint(self.IProfile.QOPData))
        elif typeLoad == const.FOR_RANK:
            self.textOut.insert('1.0', self.IProfile.DataPrint(self.IProfile.RANKData))
            
        self.textOut.see("end")
        self.textOut.config(state=DISABLED)
        return
    
    def SelectFile(self, typeLoad):
        filename = filedialog.askopenfilename(filetypes = const.typeTXT, defaultextension=const.typeTXT)
        if not filename:
            return
        
        if (len(self.IProfile.R4Data) and typeLoad == const.FOR_R4) or\
         (len(self.IProfile.QOPData) and typeLoad == const.FOR_QOP) or\
         (len(self.IProfile.RANKData) and typeLoad == const.FOR_RANK) or\
         ((len(self.IProfile.R4Data) or len(self.IProfile.QOPData) or\
          len(self.IProfile.RANKData)) and typeLoad == const.FOR_ALL):
             result = messagebox.askquestion("Изменить", "Вы действительно хотите изменить данные?", icon='warning')
             if result != 'yes':
                 return
      
        if self.IProfile.AppendData(filename, typeLoad) == 0:
            messagebox.showerror('Ошибка', 'Ошибка при чтении файла')
            return
        
        self.UpdateResults()
    
    def InitPanel1(self, p1):
        #==========================================================
        label = Label(p1, text="Результаты для r4(n):")
        label.grid(row=0, column=0, sticky=W, padx=(4, 0)) 
        button = Button(p1, text="Загрузить", command = lambda: self.SelectFile(const.FOR_R4))
        button.grid(row=1, column=0, sticky=W, padx=(4, 0))
        self.buttonR4 = Button(p1, text="Результаты", command = lambda: self.Print(const.FOR_R4))
        self.buttonR4.grid(row=1, column=0, sticky=W, padx=(72, 0))
        
        #==========================================================
        label = Label(p1, text="Результаты для qop(n):")
        label.grid(row=2, column=0, sticky=W, pady=(12, 0), padx=(4, 0)) 
        button = Button(p1, text="Загрузить", command = lambda: self.SelectFile(const.FOR_QOP))
        button.grid(row=3, column=0, sticky=W, padx=(4, 0))   
        self.buttonQOP = Button(p1, text="Результаты", command = lambda: self.Print(const.FOR_QOP))
        self.buttonQOP.grid(row=3, column=0, sticky=W, padx=(72, 0))   
        
        #==========================================================
        label = Label(p1, text="Результаты для rank(n):")
        label.grid(row=4, column=0, sticky=W, pady=(12, 0), padx=(4, 0)) 
        button = Button(p1, text="Загрузить", command = lambda: self.SelectFile(const.FOR_RANK))
        button.grid(row=5, column=0, sticky=W, padx=(4, 0))      
        self.buttonRank = Button(p1, text="Результаты", command = lambda: self.Print(const.FOR_RANK))
        self.buttonRank.grid(row=5, column=0, sticky=W, padx=(72, 0))
        
        #==========================================================
        label = Label(p1, text="Общие результаты:")
        label.grid(row=6, column=0, sticky=W, pady=(12, 0), padx=(4, 0)) 
        button = Button(p1, text="Загрузить", command = lambda: self.SelectFile(const.FOR_ALL))
        button.grid(row=7, column=0, sticky=W, padx=(4, 0))       
        
        #==========================================================
        text = Text(p1, width=64, height=4)
        text.grid(row=8, column=0, padx=(4, 0), pady=(12, 0), columnspan = (int)(const.width/2))
        text.insert('1.0', "Достаточно высчитать два значения, чтобы получить третье.\n"+
                    "Вывод программ должен быть следующий:\n" +
                    "Для одиночной: [число] [время] [значение]\n" +
                    "Для общей: [число] [время] [r4(n)] [qop(n)] [rank(n)].")
        text.config(state=DISABLED)
        self.UpdateResults()
    
    def InitPanel2(self, p2):
        label = Label(p2, text="Результаты:")
        label.grid(row=0, column=0, sticky=W)
        
        self.textOut = Text(p2, width=64, height=35)
        self.textOut.grid(row=1, column=0)
         
        scroll = ttk.Scrollbar(p2, orient=VERTICAL, command=self.textOut.yview)
        scroll.grid(row=1, column=1, sticky=N+S)
        self.textOut.config(yscrollcommand=scroll.set, state=DISABLED)

    def InitPanels(self, frame):
        panel1 = Frame(frame, width=const.width/2, height=const.height)
        panel1.place(x = 0, y = 0)
        
        panel2 = Frame(frame, width=472, height=const.height)
        panel2.place(x = const.width - 480, y = 0)
        return panel1, panel2

    def Tab1Init(self, frame):
        p1, p2 = self.InitPanels(frame)
        self.InitPanel1(p1)
        self.InitPanel2(p2)
    
    def __init__(self, IMain, IProfile):
        self.IProfile = IProfile
        self.Tab1Init(IMain.frame1)