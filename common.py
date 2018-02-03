from PyQt5.QtGui import QColor

def setColor(window, r, g, b):
    """Sets the window color to the given RGB value"""
    pal = window.palette()
    pal.setColor(window.backgroundRole(), QColor.fromRgb(r, g, b))
    window.setPalette(pal)

buttonStylesheet = """ QPushButton {
    background-color: #DDDDDD;
    border: 2px groove grey; border-radius: 3px;
    padding: 7px; }
    QPushButton:hover {
        background-color: #AAAACC
    }
    QPushButton:pressed {
        background-color: #8888AA;
    }
    """