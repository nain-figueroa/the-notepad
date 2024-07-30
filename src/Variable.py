import wx
app = wx.App()
largo = 800
ancho = 600
#FUENTE==================================================================================
font = wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

#ARCHIVOS================================================================================
abierto = False
archivo_abierto = ''
guardado = False

idioma = 'ES'

#ESPACIO DE TRABAJO======================================================================
lin = 1
col = 1
lin_col = (lin, col)