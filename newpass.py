'''
The class for the window that opens when so saved master password is found. It
will ask for a new password, check that it is the same in both boxes, and
saves it to disk
'''

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QFont

from Crypto.Hash import SHA256
from os.path import join
from os import getenv

from common import setColor, buttonStylesheet

class NewPasswordScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.password = None
        self.initUI()
    
    def initUI(self):
        font = QFont("Arial", 12)

         #Labels
        passwordLabel = QLabel(
            "<font color='white'>Enter a new password:</font>")
        passwordLabel.setFont(font)
        passwordLabel.setFixedWidth(200)
        passwordLabel.setAlignment(Qt.AlignCenter)

        differentPasswordLabel = QLabel(
                "<font color='red'>Passwords do not match</font>")
        differentPasswordLabel.setFont(font)
        differentPasswordLabel.setFixedWidth(200)
        differentPasswordLabel.setAlignment(Qt.AlignCenter)
        differentPasswordLabel.setVisible(False)
        self.differentPasswordLabel = differentPasswordLabel

        #Text Boxes
        passwordBox0 = QLineEdit()
        passwordBox0.setFont(QFont("Arial", 15))
        passwordBox0.setEchoMode(QLineEdit.Password)
        self.passwordBox0 = passwordBox0
        
        passwordBox1 = QLineEdit()
        passwordBox1.setFont(QFont("Arial", 15))
        passwordBox1.setEchoMode(QLineEdit.Password)
        self.passwordBox1 = passwordBox1

        #Buttons
        exitButton = QPushButton('Exit')
        exitButton.setFont(font)
        exitButton.setStyleSheet(buttonStylesheet)
        exitButton.clicked.connect(lambda x: exit())

        okayButton = QPushButton('Enter')
        okayButton.setFont(font)
        okayButton.setStyleSheet(buttonStylesheet)
        okayButton.clicked.connect(self.checkPassword)

        #Layout setup
        grid = QGridLayout()
        grid.setSpacing(20)

        grid.addWidget(passwordLabel, 0, 1)
        grid.addWidget(passwordBox0, 1, 0, 1, 3)
        grid.addWidget(passwordBox1, 2, 0, 1, 3)
        grid.addWidget(differentPasswordLabel, 3, 1)
        grid.addWidget(exitButton, 3, 0)
        grid.addWidget(okayButton, 3, 2)

        setColor(self, 51, 51, 51)
        self.setLayout(grid)
        self.setWindowTitle("Enter a New Password")
        self.setFixedSize(350, 200)
        self.show()

    def checkPassword(self, **kwargs):
        '''
        Checks to be sure that the password boxes match and saves it if
        they do.
        '''
        if self.passwordBox0.text() != self.passwordBox1.text():
            self.differentPasswordLabel.setVisible(True)
            return

        with open(join(join(getenv('APPDATA'), 'PassManData'),
            'savedpassword'), 'wb') as file:
            sha3_256 = SHA256.new()
            sha3_256.update(self.passwordBox0.text().encode())
            file.write(sha3_256.digest())

        self.password = self.passwordBox0.text().encode()
        self.close()


    def event(self, event):
        """Checks to see one of the enter keys were pressed, and passes it to 
        the default event method if it wasn't"""

        if (event.type() == QEvent.KeyRelease 
            and 16777221 >= event.key() >= 16777220):

            self.checkPassword()
            return True
        else:
            return QWidget.event(self, event)

    def closeEvent(self, event):
        """Closes the application if the password was not entered, or
        closes the window so that the next window may open if the password
        was entered"""

        if self.password == None:
            quit()
        else:
            self.close()