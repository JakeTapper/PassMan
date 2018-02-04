'''
The class that is run when the "New Password" button is pressed. Is a new 
window that contains a couple of fields, buttons, and check boxes.
'''

from sys import argv, exit
from PyQt5.QtWidgets import (QWidget, 
    QLabel, QLineEdit, QGridLayout, QMenu, QApplication, qApp, QPushButton,
    QCheckBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QCoreApplication, QEvent

from common import setColor, buttonStylesheet
from passwordbutton import PasswordButton
from string import ascii_letters, digits, punctuation
from random import choice
from os import getenv
from os.path import join
from pyperclip import copy
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import Salsa20

class AddPasswordScreen(QWidget):
    lettersCheck = True
    digitsCheck = True
    symbolsCheck = True
    def __init__(self, parent):
        super().__init__()
        self.password = None
        self.key = parent.password
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        font = QFont("Arial", 12)
        boxFont = QFont("Arial", 15)
        
        #Labels
        self.userLabel = QLabel(
            "<font color='white'>Website/Application:</font>")
        self.userLabel.setFont(font)

        passLabel = QLabel(
            "<font color='white'>Password:</font>")
        passLabel.setFont(font)

        #TextBoxes
        self.userBox = QLineEdit()
        self.userBox.setFont(boxFont)

        self.passBox = QLineEdit()
        self.passBox.setFont(boxFont)

        #Buttons
        exitButton = QPushButton('Exit')
        exitButton.setFont(font)
        exitButton.setStyleSheet(buttonStylesheet)
        exitButton.clicked.connect(lambda x: self.close())

        okayButton = QPushButton('Enter')
        okayButton.setFont(font)
        okayButton.setStyleSheet(buttonStylesheet)
        okayButton.clicked.connect(self.savePassword)

        genButton = QPushButton('Generate password')
        genButton.setFont(font)
        genButton.setStyleSheet(buttonStylesheet)
        genButton.clicked.connect(self.genPassword)

        #Radio Buttons
        self.lettersRB = QCheckBox('Letters')
        self.lettersRB.setChecked(AddPasswordScreen.lettersCheck)
        self.lettersRB.setFont(font)
        self.lettersRB.setStyleSheet('color: white')
        self.lettersRB.clicked.connect(
            lambda x: self.setState('letters', self.lettersRB))

        self.digitsRB = QCheckBox('Digits')
        self.digitsRB.setChecked(AddPasswordScreen.digitsCheck)
        self.digitsRB.setFont(font)
        self.digitsRB.setStyleSheet('color: white')
        self.digitsRB.clicked.connect(
            lambda x: self.setState('digits', self.digitsRB))

        self.symbolsRB = QCheckBox('Symbols')
        self.symbolsRB.setChecked(AddPasswordScreen.symbolsCheck)
        self.symbolsRB.setFont(font)
        self.symbolsRB.setStyleSheet('color: white')
        self.symbolsRB.clicked.connect(
            lambda x: self.setState('symbols', self.symbolsRB))

        #Layout
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.userLabel, 0, 0)
        grid.addWidget(passLabel, 1, 0)
        grid.addWidget(self.userBox, 0, 1)
        grid.addWidget(self.passBox, 1, 1)
        grid.addWidget(exitButton, 2, 0)
        grid.addWidget(okayButton, 2, 1)
        grid.addWidget(self.lettersRB, 3, 0)
        grid.addWidget(self.digitsRB, 3, 1)
        grid.addWidget(self.symbolsRB, 4, 0)
        grid.addWidget(genButton, 4, 1)


        setColor(self, 75, 75, 75)
        self.setLayout(grid)
        self.resize(500, 150)
        self.setWindowTitle("Add New Password")
        self.show()


    def savePassword(self, **kwargs):
        '''
        Saves the currently entered password
        '''
        cleanedTitle = ''.join(filter(
            lambda x: x in ascii_letters + digits + ' ', self.userBox.text()))
        if self.passBox.text() == '' or cleanedTitle == '':
            return

        try:
            with open(join(join(getenv('APPDATA'), 'PassManData'),
            cleanedTitle), 'xb') as file:
                salt = "".join([choice(ascii_letters + digits) for _ in range(16)])
                derivedKey = PBKDF2(
                    self.key,
                    salt.encode(),
                    dkLen=32
                    )

                cipher = Salsa20.new(derivedKey)
                data = cipher.encrypt(self.passBox.text().encode())
                string = cipher.nonce + salt.encode() + data

                file.write(string)
                self.parent.files.append(cleanedTitle)
                self.parent.updateButtons()
                self.close()

        except FileExistsError:
            self.userLabel.setText(
                "<font color='red'>Name already exsists</font>")

    def genPassword(self, **kwargs):
        '''
        Generates a random password
        '''
        chars = ''
        chars += ascii_letters if self.lettersRB.isChecked() else ''
        chars += digits if self.digitsRB.isChecked() else ''
        chars += punctuation if self.symbolsRB.isChecked() else ''

        if chars == '':
            return
        
        password= ''.join([choice(chars) for _ in range(24)])
        self.password = password
        self.passBox.setText(password)
        copy(password)

    def setState(self, boxName, box):
        '''
        Sets the state of the check box when it is pressed
        '''
        if boxName == 'letters':
            AddPasswordScreen.lettersCheck = box.isChecked()
        if boxName == 'digits':
            AddPasswordScreen.digitsCheck = box.isChecked()
        if boxName == 'symbols':
            AddPasswordScreen.symbolsCheck = box.isChecked()

    def event(self, event):
        """Checks to see one of the enter keys were pressed, and passes it to 
        the default event method if it wasn't"""

        if (event.type() == QEvent.KeyRelease 
            and 16777221 >= event.key() >= 16777220):

            self.savePassword()
            return True
        else:
            return QWidget.event(self, event)
