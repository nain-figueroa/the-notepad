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
        #ID´s============================================================================
        espanol_ID = self.NewControlId()
        ingles_ID = self.NewControlId()

        tem_osc_ID = self.NewControlId()
        tem_lig_ID = self.NewControlId()


        #BARRA DE MENUS==================================================================
        bar_menu = wx.MenuBar()

        #==MENUS=========================================================================
        #===MENU DE ARCHIVO==============================================================
        file_menu = wx.Menu()

        file_menu.Append(wx.ID_NEW, 'Nuevo')   
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_OPEN, 'Abrir')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_SAVE, 'Guardar')   
        file_menu.Append(wx.ID_SAVEAS, 'Guardar como...')   

        #===MENU DE PREFERENCIAS=========================================================
        ajustes_menu = wx.Menu()
    
        #===SUBMENUS=====================================================================
        #====IDIOMAS=====================================================================
        idiomas = wx.Menu()
        idiomas.Append(espanol_ID, 'Español')
        idiomas.Append(ingles_ID, 'Ingles')

        #===TEMAS========================================================================
        temas = wx.Menu()
        temas.Append(tem_lig_ID, 'Claro')
        temas.Append(tem_osc_ID, 'Oscuro')

        ajustes_menu.AppendSubMenu(idiomas, 'Idioma')
        ajustes_menu.AppendSubMenu(temas, 'Temas')

        bar_menu.Append(file_menu, 'Archivo')
        bar_menu.Append(ajustes_menu, 'Preferencias')

        self.SetMenuBar(bar_menu)

        #STATUS BAR======================================================================
        bar_estado = self.CreateStatusBar(4)
        self.SetStatusBar(bar_estado)

        escribir = Notepad(self, size=self.GetSize())  

#////////////////////////////////////////////////////////////////////////////////////////        
if __name__ == '__main__':
    app = wx.App()

    ventana = Window(None, title='The Notepad', size=(Variable.largo, Variable.ancho))
    ventana.Show()

    app.MainLoop()