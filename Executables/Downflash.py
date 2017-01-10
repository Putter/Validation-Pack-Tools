from Tkinter import *
class Flash_Build():
    def __init__(self, path):
        self.path = path
        self.META = ''
        self.AU = ''
        self.OEM = ''
    def UI_Screen(self):
        self.top = Toplevel()
        self.top.title('Select path')
        Label(self.top, text="META").grid(sticky=E)
        Label(self.top, text="AU").grid(sticky=E)
        Label(self.top, text="OEM").grid(sticky=E)
        self.e1 = Entry(self.top, width=50)
        self.e2 = Entry(self.top, width=50)
        self.e3 = Entry(self.top, width=50)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        Button(self.top, text='OK', command=self.textdisplay).grid(row=3, column=3)
        self.top.protocol('WM_DELETE_WINDOW', self.donothing)
    def donothing(self):
        pass
    def textdisplay(self):
        self.path['META'] = self.e1.get()
        self.path['AU'] = self.e2.get()
        self.path['OEM'] = self.e3.get()
        self.top.withdraw()
        print self.path
        return self.path

