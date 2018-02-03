from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt

from Crypto.Cipher import Salsa20
from Crypto.Protocol.KDF import PBKDF2

from os import getenv, listdir, makedirs, remove
from os.path import join, isfile
from pyperclip import copy
from codecs import decode

class PasswordButton(QPushButton):
    def __init__(self, text, password, parent, **kwargs):
        super().__init__()

        passBtnStyle = """QPushButton {
            background-color: #333333;
            border-left: 0px solid black;
            border-right: 0px solid black;
            border-bottom: 1px solid #555555;
            border-top: 0px solid #555555;
            color: white;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QPushButton:pressed {
            background-color: #404040;
        }
        """

        self.setText(text)
        self.password = password
        self.setFont(QFont("Arial", 18))
        self.setShortcut('Ctrl-N')
        self.setStyleSheet(passBtnStyle)
        self.clicked.connect(self.loadPassword)
        self.parent = parent
        self.contextMenu = None

    def loadPassword(self, **kwargs):
        filename = self.text()
        if (filename == "File not found" or
            filename == "Password copied to clipboard" or 
            filename == "Incorrect login password. Unable to decode"):
            return
        try:
            with open(join(join(getenv('APPDATA'), 'PassManData'), 
            filename), 'rb') as file:
                data = file.read()
            nonce, salt, data = data[:8], data[8:24], data[24:]

            derivedKey = PBKDF2(
                self.password,
                salt,
                dkLen=32
            )
            cipher = Salsa20.new(derivedKey, nonce)
            decrypted = cipher.decrypt(data)
            copy(decode(decrypted, 'CP1252'))
            self.setText('Password copied to clipboard')
            QTimer.singleShot(2000, lambda: self.setText(filename))
        except FileNotFoundError:
            self.setText('File not found')
            QTimer.singleShot(2000, lambda: self.setText(filename))
        except UnicodeDecodeError:
            self.setText('Incorrect login password. Unable to decode')
            QTimer.singleShot(2000, lambda: self.setText(filename))

    def onContextMenu(self, point):
        self.contextMenu.exec(self.mapToGlobal(point))

    def remove(self, **kwargs):
        filename = self.text()
        if (filename == "File not found" or
            filename == "Password copied to clipboard" or 
            filename == "Incorrect login password. Unable to decode"):
            return
        msg = QMessageBox()
        msg.setText("Are you sure that you want to delete this password file?")
        msg.setInformativeText("This action cannot be undone")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        ret = msg.exec()

        if ret == QMessageBox.Ok:
            self.parent.files.remove(filename)
            remove(join(join(getenv('APPDATA'), 'PassManData'), filename))
            self.parent.updateButtons()
