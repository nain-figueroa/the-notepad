import wx
import time

import Variable
from notepad import *

delay = 1.0

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
        file_menu.Append(wx.ID_OPEN, 'Abrir\tCtrl+N')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_SAVE, 'Guardar\tCtrl+G')   
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

        #EVENTOS=========================================================================
        file_menu.Bind(wx.EVT_MENU, self.onFileMenu)

        self.escribir = Notepad(self, size=self.GetSize())

        if self.escribir.espacio_escritura.IsModified():
            self.SetStatusText('Editando', 3)


        self.Show(True)
        self.Layout()

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
        with wx.FileDialog(self, message='Abrir Archivo', style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as new_file:
            if new_file.ShowModal() == wx.ID_CANCEL:
                return
            
            path_name = new_file.GetPath()
            try:
                new_ventana = Window(None, title='The Notepad', size=(Variable.largo, Variable.ancho))
    
                new_ventana.escribir.espacio_escritura.LoadFile(path_name)
                Variable.abierto = True
                Variable.archivo_abierto = path_name
                    
                #ELIMINAR VENTANA ANTERIOR
                self.Destroy()
            except IOError:
                wx.LogError("No se pudo abrir el archivo '%s.'" % path_name)

        # new_file = wx.FileDialog(self, message='Abrir Nuevo Archivo', style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        # new_file.ShowModal()

    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\    
    def onGuardarArchivo(self):
        #SI EL ARCHIVO NO ES EDITADO(ES NUEVO) SE MUESTRA LA VENTANA PARA GUARDAR========
        if not Variable.abierto:
            #MOSTRAR VENTANA DE GUARDADO=================================================
            with wx.FileDialog(self, message='Guardar Archivo', style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as save_file:
                if save_file.ShowModal() == wx.ID_CANCEL:
                    return

                #OBTENER LA DIRECCION====================================================
                path_name = save_file.GetPath()
                try:
                    with open(path_name, 'w') as file:
                        text = self.escribir.espacio_escritura.GetValue()
                        text_lines = text.splitlines()

                        text_str = """"""
                        for line in text_lines:
                            text_str += line

                        file.write(text_str)
                        Variable.abierto = True
                        
                        self.SetStatusText('Guardado', 3)
                        time.sleep(delay)
                        self.SetStatusText('Editando', 3)
                except IOError:
                    wx.LogError("No se pudo guardar el archivo '%s." % path_name)
        #SI EL ARCHIVO ES UNO EDITADO NO SE HABRE LA VENTANA DE DIALOGO, SOLO SE GUARDA==
        else:
            try:
                with open(Variable.archivo_abierto, 'w') as file:
                    text = self.escribir.espacio_escritura.GetValue()
                    text_lines = text.splitlines()

                    text_str = """"""
                    for line in text_lines:
                        text_str += (line + '\n')
                    
                    file.write(text_str)
                    self.SetStatusText('Guardado', 3)
                    time.sleep(delay)
                    self.SetStatusText('Editando', 3)
                    
            except IOError:
                wx.LogError("No se pudo guardar el archivo '%s." % Variable.archivo_abierto)

        # save_file = wx.FileDialog(self, message='Guardar Archivo', wildcard='Documento de texto|*.txt', style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        # save_file.ShowModal()

    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\    
    def onGuardarComo(self):
        Variable.abierto = False
        self.onGuardarArchivo()

    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\    
    def onNuevo(self):
        self.escribir.espacio_escritura.Clear()

#////////////////////////////////////////////////////////////////////////////////////////        
if __name__ == '__main__':
    app = wx.App()

    ventana = Window(None, title='The Notepad', size=(Variable.largo, Variable.ancho))

    app.MainLoop()