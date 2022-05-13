import const
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class MainInstance:
    def MainAbout(self):
        messagebox.showinfo('О программе', 'Quadratic Odd Partitions\nСаша С. 2022г., ЮУрГУ')
    
    def __init__(self, IRoot):
        notebook = ttk.Notebook(IRoot)
        notebook.pack()
        
        self.frame1 = Frame(notebook, width=const.width, height=const.height)
        self.frame2 = Frame(notebook, width=const.width, height=const.height)
        self.frame3 = Frame(notebook, width=const.width, height=const.height)
        
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        
        notebook.add(self.frame1, text='Данные')
        notebook.add(self.frame2, text='Таблицы и графики')
        notebook.add(self.frame3, text='Аппроксимация и оценка')
        
        menubar = Menu(IRoot)
        menubar.add_command(label="О программе", command=self.MainAbout)
        IRoot.config(menu=menubar)
    