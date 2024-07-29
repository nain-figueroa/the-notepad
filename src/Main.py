import wx

import Variable
from notepad import *

class Window(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.main()
    #////////////////////////////////////////////////////////////////////////////////////    
    def main(self):
        self.CenterOnScreen()

if __name__ == '__main__':
    app = wx.App()

    ventana = Window(None, title='The Notepad', size=(Variable.largo, Variable.ancho))
    ventana.Show()

    app.MainLoop()