from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import sys

class signUp(QMainWindow):
    def __init__(self):
        super(signUp, self).__init__()
        uic.loadUi('./assets/Signup.ui', self)

        self.username = self.findChild(QLineEdit, 'lineEdit')
        self.password = self.findChild(QLineEdit, 'lineEdit_2')
        self.password2 = self.findChild(QLineEdit, 'lineEdit_3')
        self.login_btn = self.findChild(QPushButton, 'pushButton_2')
        self.signUp_btn = self.findChild(QPushButton, 'pushButton')

        self.setWindowIcon(QtGui.QIcon('./assets/lock.png'))
        # self.show()

if __name__ == '__main__':       
    app = QApplication(sys.argv)
    main = signUp()
    main.show()
    app.exec_()