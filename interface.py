from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./assets/mainUI.ui', self)

        self.frame = self.findChild(QFrame, 'frame')
        self.frame_2 = self.findChild(QFrame, 'frame_2')
        self.lineEdit_search = self.findChild(QLineEdit, 'lineEdit_search')
        self.btn_exit = self.findChild(QPushButton, 'btn_exit')
        self.btn_addAccount= self.findChild(QPushButton, 'btn_addAccount')
        self.btn_edit= self.findChild(QPushButton, 'btn_edit')
        self.btn_delete= self.findChild(QPushButton, 'btn_delete')
        self.btn_show= self.findChild(QPushButton, 'btn_show')
        self.btn_copy= self.findChild(QPushButton, 'btn_copy')
        self.pushButton_close= self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_save = self.findChild(QPushButton, 'pushButton_save')
        self.btn_search = self.findChild(QPushButton, 'btn_search')
        self.lineEdit_search = self.findChild(QLineEdit, 'lineEdit_search')
        self.lineEdit_website= self.findChild(QLineEdit, 'lineEdit_website')
        self.lineEdit_password= self.findChild(QLineEdit, 'lineEdit_password')
        self.lineEdit_username= self.findChild(QLineEdit, 'lineEdit_username')
        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.textEdit_note = self.findChild(QTextEdit, 'textEdit')
        self.lineEdit_tag = self.findChild(QLineEdit, 'lineEdit')
        self.label_welcome = self.findChild(QLabel, 'label')
        self.label_edit = self.findChild(QLabel, 'label_3')
        self.btn_browser = self.findChild(QPushButton, 'btn_browser')
        self.progressBar_strength = self.findChild(QProgressBar, 'progressBar')
        self.label_strength = self.findChild(QLabel, 'label_7')
        self.btn_logout = self.findChild(QPushButton, 'btn_logout')
        self.lineEdit_category = self.findChild(QLineEdit, 'lineEdit_category')

        # Setup icons
        self.setWindowIcon(QtGui.QIcon('./assets/lock.png'))
        self.btn_edit.setIcon(QtGui.QIcon('./assets/editing.png'))
        self.btn_addAccount.setIcon(QtGui.QIcon('./assets/add.png'))
        self.btn_copy.setIcon(QtGui.QIcon('./assets/copy.png'))
        self.btn_delete.setIcon(QtGui.QIcon('./assets/close.png'))
        self.btn_show.setIcon(QtGui.QIcon('./assets/view.png'))
        self.btn_search.setIcon(QtGui.QIcon('./assets/search.png'))
        self.btn_exit.setIcon(QtGui.QIcon('./assets/exit.png'))
        self.btn_browser.setIcon(QtGui.QIcon('./assets/browser.png'))
        self.btn_logout.setIcon(QtGui.QIcon('./assets/logout.png'))



        # self.show()

if __name__ == '__main__':       
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()