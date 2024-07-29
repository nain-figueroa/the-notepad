import wx
import Variable

class Notepad(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.main()

    def main(self):
        pantalla = wx.ScreenDC()
        #SIZERS==========================================================================
        sizer_general = wx.BoxSizer(wx.VERTICAL)

        #CUADRO DE TEXTO=================================================================
        self.espacio_escritura = wx.TextCtrl(self,size=pantalla.GetSize() ,style=wx.TE_RICH2|wx.TE_DONTWRAP|wx.TE_MULTILINE)
        self.espacio_escritura.SetFont(Variable.font)

        #ACOMODO=========================================================================
        sizer_general.Add(self.espacio_escritura, flag=wx.EXPAND|wx.ALL)

        self.SetSizer(sizer_general)

        self.Layout()
