'''
The login window class that is opened when the program is first started
'''

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont

from os import getenv
from os.path import join
from Crypto.Hash import SHA256

from common import setColor, buttonStylesheet

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.password = None
        self.initUI()
    
    def initUI(self):
        font = QFont("Arial", 12)

        #Labels
        passwordLabel = QLabel("<font color='white'>Enter your password:</font>")
        passwordLabel.setFont(font)
        passwordLabel.setFixedWidth(200)
        passwordLabel.setAlignment(Qt.AlignCenter)

        wrongPasswordLabel = QLabel("<font color='red'>Incorrect Password</font>")
        wrongPasswordLabel.setFont(font)
        wrongPasswordLabel.setFixedWidth(200)
        wrongPasswordLabel.setAlignment(Qt.AlignCenter)
        wrongPasswordLabel.setVisible(False)
        self.wrongPasswordLabel = wrongPasswordLabel

        #Text Box
        passwordBox = QLineEdit()
        passwordBox.setFont(QFont("Arial", 15))
        passwordBox.setEchoMode(QLineEdit.Password)
        self.passwordBox = passwordBox

        #Buttons
        exitButton = QPushButton('Exit')
        exitButton.setFont(font)
        exitButton.setStyleSheet(buttonStylesheet)
        exitButton.clicked.connect(lambda x: self.close())

        okayButton = QPushButton('Enter')
        okayButton.setFont(font)
        okayButton.setStyleSheet(buttonStylesheet)
        okayButton.clicked.connect(lambda x: self.checkPassword(passwordBox, wrongPasswordLabel))

        #Layout setup
        grid = QGridLayout()
        grid.setSpacing(20)

        grid.addWidget(passwordLabel, 0, 1)
        grid.addWidget(passwordBox, 1, 0, 1, 3)
        grid.addWidget(wrongPasswordLabel, 2, 1)
        grid.addWidget(exitButton, 2, 0)
        grid.addWidget(okayButton, 2, 2)

        #Set up the window
        setColor(self, 51, 51, 51)

        self.setLayout(grid)
        self.setWindowTitle("Login")
        self.setFixedSize(350, 150)
        self.show()

    def checkPassword(self, box, label):        
        """Reads the hashed password from a file and checks it against the entered password"""

        password = box.text()
        savedPass = ""

        with open(join(join(getenv('APPDATA'), 'PassManData'),
            'savedpassword'), 'rb') as file:
            savedPass = file.read()

        sha3_256 = SHA256.new()
        sha3_256.update(password.encode())
        if sha3_256.digest() == savedPass:
            self.password = password.encode()
            self.close()
        else:
            label.setVisible(True)

    def event(self, event):
        """Checks to see one of the enter keys were pressed, and passes it to the
        default event method if it wasn't"""

        if event.type() == QEvent.KeyRelease and 16777221 >= event.key() >= 16777220:
            self.checkPassword(self.passwordBox, self.wrongPasswordLabel)
            return True
        else:
            return QWidget.event(self, event)

    def closeEvent(self, event):
        """Closes the application if the password was not entered, or
        closes the window so that the next window may open if the password
        was entered"""

        if self.password == None:
            exit()
        else:
            self.close()