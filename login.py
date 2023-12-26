from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import sys

class login(QMainWindow):
    def __init__(self):
        super(login, self).__init__()
        uic.loadUi('./assets/Login.ui', self)

        self.username = self.findChild(QLineEdit, 'lineEdit')
        self.password = self.findChild(QLineEdit, 'lineEdit_2')
        self.login_btn = self.findChild(QPushButton, 'pushButton')
        self.signUp_btn = self.findChild(QPushButton, 'pushButton_2')

        self.setWindowIcon(QtGui.QIcon('./assets/lock.png'))
        self.setTabOrder(self.username, self.password)
        self.setTabOrder(self.password, self.login_btn)

        # self.show()

if __name__ == '__main__':       
    app = QApplication(sys.argv)
    main = login()
    main.show()
    app.exec_()