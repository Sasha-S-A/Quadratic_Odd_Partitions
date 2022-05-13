import const
from tkinter import *
from tkinter import ttk
from profileset import *
from main import MainInstance
from tab1 import Tab1Instance
from tab2 import Tab2Instance
from tab3 import Tab3Instance

IRoot = Tk()
IProfile = ProfileSet()

def close():
    IProfile.SaveToFile()
    IRoot.destroy()
    IRoot.quit()

IRoot.title("Quadratic Odd Partitions")
IRoot.protocol('WM_DELETE_WINDOW', close)
x = IRoot.winfo_screenwidth() // 2 - const.width // 2
y = IRoot.winfo_screenheight() // 2 - const.height // 2
IRoot.geometry('{}x{}+{}+{}'.format(const.width, const.height, x, y))
IRoot.resizable(0, 0)

s = ttk.Style()
s.theme_use('clam')

IMain = MainInstance(IRoot)
Tab1Instance(IMain, IProfile)
Tab2Instance(IMain, IProfile, IRoot)
Tab3Instance(IMain, IProfile, IRoot)

IRoot.mainloop()