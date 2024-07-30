import wx
from Ventana import *
#////////////////////////////////////////////////////////////////////////////////////////        
if __name__ == '__main__':
    app = wx.App()

    ventana = Window(None, title='The Notepad', size=(Variable.largo, Variable.ancho))
    app.MainLoop()