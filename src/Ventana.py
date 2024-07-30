import wx
import time
import pandas as pd

import Variable
from notepad import *

delay = 1.0
idiomas = pd.read_excel('Archives/Lenguajes.xlsx')

#////////////////////////////////////////////////////////////////////////////////////////
class Window(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.main()
    #////////////////////////////////////////////////////////////////////////////////////    
    def main(self):
        self.CenterOnScreen()
        Variable.abierto = False
        Variable.archivo_abierto = ''

        #ID´s============================================================================
        self.espanol_ID = self.NewControlId()
        self.ingles_ID = self.NewControlId()

        tem_osc_ID = self.NewControlId()
        tem_lig_ID = self.NewControlId()


        #BARRA DE MENUS==================================================================
        bar_menu = wx.MenuBar()

        #==MENUS=========================================================================
        #===MENU DE ARCHIVO==============================================================
        file_menu = wx.Menu()

        file_menu.Append(wx.ID_NEW, idiomas.loc[idiomas['ID'] == 'NEW_FILE', Variable.idioma].values[0])   
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_OPEN, idiomas.loc[idiomas['ID'] == 'OPEN_FILE', Variable.idioma].values[0] +'\tCtrl+N')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_SAVE, idiomas.loc[idiomas['ID'] == 'SAVE_FILE', Variable.idioma].values[0] +'\tCtrl+G')   
        file_menu.Append(wx.ID_SAVEAS, idiomas.loc[idiomas['ID'] == 'SAVE_AS', Variable.idioma].values[0])   

        #===MENU DE PREFERENCIAS=========================================================
        ajustes_menu = wx.Menu()
    
        #===SUBMENUS=====================================================================
        #====IDIOMAS=====================================================================
        idiom = wx.Menu()
        idiom.Append(self.espanol_ID, idiomas.loc[idiomas['ID'] == 'SPANISH', Variable.idioma].values[0])
        idiom.Append(self.ingles_ID, idiomas.loc[idiomas['ID'] == 'ENGLISH', Variable.idioma].values[0])

        #===TEMAS========================================================================
        temas = wx.Menu()
        temas.Append(tem_lig_ID, idiomas.loc[idiomas['ID'] == 'LIGHT', Variable.idioma].values[0])
        temas.Append(tem_osc_ID, idiomas.loc[idiomas['ID'] == 'DARK', Variable.idioma].values[0])

        ajustes_menu.AppendSubMenu(idiom, idiomas.loc[idiomas['ID'] == 'LANGUAGES', Variable.idioma].values[0])
        ajustes_menu.AppendSubMenu(temas, idiomas.loc[idiomas['ID'] == 'THEMES', Variable.idioma].values[0])

        bar_menu.Append(file_menu, idiomas.loc[idiomas['ID'] == 'FILE_MENU', Variable.idioma].values[0])
        bar_menu.Append(ajustes_menu, idiomas.loc[idiomas['ID'] == 'SETTINGS', Variable.idioma].values[0])

        self.SetMenuBar(bar_menu)

        #STATUS BAR======================================================================
        bar_estado = self.CreateStatusBar(6)
        self.SetStatusBar(bar_estado)

        self.SetStatusText(idiomas.loc[idiomas['ID'] == 'LINE', Variable.idioma].values[0] + str(Variable.lin_col[1]),0)
        self.SetStatusText(idiomas.loc[idiomas['ID'] == 'COLUM', Variable.idioma].values[0] + str(Variable.lin_col[0]), 1)

        #ESPACIO DE TRABAJO==============================================================
        self.escribir = Notepad(self, size=self.GetSize())

        #TIMER===========================================================================
        self.timer = wx.Timer(self.escribir)


        #EVENTOS=========================================================================
        file_menu.Bind(wx.EVT_MENU, self.onFileMenu)
        idiom.Bind(wx.EVT_MENU,self.onIdiomasMenu )
        self.escribir.Bind(wx.EVT_TIMER, self.lin_col, self.timer)

        #INICIO DEL TIMER================================================================
        self.timer.Start(250)


        if self.escribir.espacio_escritura.IsModified():
            self.SetStatusText(idiomas.loc[idiomas['ID'] == 'EDIT', Variable.idioma].values[0], 5)
            self.Bind(wx.EVT_CLOSE, self.cambiosCerrar)
 
        self.Layout()
        self.Show(True)

    #////////////////////////////////////////////////////////////////////////////////////
    def onFileMenu(self, evt):
        event_ID = evt.GetId()

        if event_ID == wx.ID_OPEN:
            self.onAbrirArchivo()
        elif event_ID == wx.ID_SAVE:
            self.onGuardarArchivo()
        elif event_ID == wx.ID_SAVEAS:
            self.onGuardarComo()
        elif event_ID == wx.ID_NEW:
            self.onNuevo()


    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\    
    def onAbrirArchivo(self): 
        self.cambios()

        with wx.FileDialog(self, message=idiomas.loc[idiomas['ID'] == 'WIN_OPEN_FILE', Variable.idioma].values[0], style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as new_file:
            if new_file.ShowModal() == wx.ID_CANCEL:
                return
            
            path_name = new_file.GetPath()
            try:
                self.timer.Stop()
                new_ventana = Window(None, title='The Notepad', size=(Variable.largo, Variable.ancho))
    
                new_ventana.escribir.espacio_escritura.LoadFile(path_name)
                Variable.abierto = True
                Variable.archivo_abierto = path_name
                    
                #ELIMINAR VENTANA ANTERIOR
                self.Destroy()
            except IOError:
                wx.LogError(idiomas.loc[idiomas['ID'] == 'NO_OPEN', Variable.idioma].values[0] + '%s.' % path_name)

        # new_file = wx.FileDialog(self, message='Abrir Nuevo Archivo', style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        # new_file.ShowModal()

    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\    
    def onGuardarArchivo(self):
        #SI EL ARCHIVO NO ES EDITADO(ES NUEVO) SE MUESTRA LA VENTANA PARA GUARDAR========

        if not Variable.abierto:
            #MOSTRAR VENTANA DE GUARDADO=================================================
            with wx.FileDialog(self, message=idiomas.loc[idiomas['ID'] == 'WIN_SAVE_FILE', Variable.idioma].values[0], style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as save_file:
                if save_file.ShowModal() == wx.ID_CANCEL:
                    return

                #OBTENER LA DIRECCION====================================================
                path_name = save_file.GetPath()
                try:
                    self.escribir.espacio_escritura.SaveFile(path_name)
                    Variable.abierto = True
                        
                    self.SetStatusText(idiomas.loc[idiomas['ID'] == 'SAVE', Variable.idioma].values[0], 5)
                    time.sleep(delay)
                    self.SetStatusText(idiomas.loc[idiomas['ID'] == 'EDIT', Variable.idioma].values[0], 5)
                except IOError:
                    wx.LogError(idiomas.loc[idiomas['ID'] == 'NO_SAVE', Variable.idioma].values[0] + '%s.' % path_name)
        #SI EL ARCHIVO ES UNO EDITADO NO SE HABRE LA VENTANA DE DIALOGO, SOLO SE GUARDA==
        else:
            try:
                self.escribir.espacio_escritura.SaveFile(Variable.archivo_abierto)

                self.SetStatusText(idiomas.loc[idiomas['ID'] == 'SAVE', Variable.idioma].values[0], 5)
                time.sleep(delay)
                self.SetStatusText(idiomas.loc[idiomas['ID'] == 'EDIT', Variable.idioma].values[0], 5)
                    
            except IOError:
                wx.LogError(idiomas.loc[idiomas['ID'] == 'NO_SAVE', Variable.idioma].values[0] + '%s.' % Variable.archivo_abierto)

        # save_file = wx.FileDialog(self, message='Guardar Archivo', wildcard='Documento de texto|*.txt', style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        # save_file.ShowModal()

    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\    
    def onGuardarComo(self):
        Variable.abierto = False
        self.onGuardarArchivo()

    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\    
    def onNuevo(self):
        self.cambios()
        self.escribir.espacio_escritura.Clear()

    #////////////////////////////////////////////////////////////////////////////////////
    def onIdiomasMenu(self, evt):
        event_ID = evt.GetId()

        if event_ID == self.espanol_ID:
            Variable.idioma = 'ES'
        elif event_ID == self.ingles_ID:
            Variable.idioma = 'ENG'
        
        self.cambios()
        self.timer.Stop()
        new_window = Window(None, title='The Notepad', size=(Variable.largo, Variable.ancho))
        self.Destroy()
    
    #////////////////////////////////////////////////////////////////////////////////////
    def cambios(self):
        if self.escribir.espacio_escritura.IsModified():
            if wx.MessageBox(idiomas.loc[idiomas['ID'] == 'NOT_SAVE', Variable.idioma].values[0], idiomas.loc[idiomas['ID'] == 'CAPTION_SAVE', Variable.idioma].values[0], wx.ICON_QUESTION|wx.YES_NO, self) == wx.NO: 
                return  
            else:
                self.onGuardarArchivo()

    #////////////////////////////////////////////////////////////////////////////////////
    def cambiosCerrar(self, evt):
        if wx.MessageBox(idiomas.loc[idiomas['ID'] == 'NOT_SAVE', Variable.idioma].values[0], idiomas.loc[idiomas['ID'] == 'CAPTION_SAVE', Variable.idioma].values[0], wx.ICON_QUESTION|wx.YES_NO, self) == wx.NO: 
            self.Destroy()
        else:
            self.onGuardarArchivo()
            self.Destroy()

    #////////////////////////////////////////////////////////////////////////////////////
    def lin_col(self, evt):
        Variable.lin_col = self.escribir.espacio_escritura.PositionToXY(self.escribir.espacio_escritura.GetInsertionPoint())

        self.SetStatusText(idiomas.loc[idiomas['ID'] == 'LINE', Variable.idioma].values[0] + str(Variable.lin_col[2] + 1),0)
        self.SetStatusText(idiomas.loc[idiomas['ID'] == 'COLUM', Variable.idioma].values[0] + str(Variable.lin_col[1] +1), 1)

        #evt.Skip()
        
