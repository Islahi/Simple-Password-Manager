from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
import sys, pyperclip
from signup import signUp
from login import login
from interface import MainWindow
from data import data
from secure import HashEncryption as hash
import webbrowser

class window():
    def __init__(self) -> None:
        self.id = 0
        self.key = ''
        self.app = QApplication(sys.argv)

        self.main = MainWindow()
        self.loginWindow = login()
        self.signupWindow = signUp()

        # Login window
        self.loginWindow.show()
        self.loginWindow.signUp_btn.clicked.connect(self.open_signup)
        self.loginWindow.login_btn.clicked.connect(self.check_user)

        # Signup Window
        self.signupWindow.signUp_btn.clicked.connect(self.add_user)
        self.signupWindow.login_btn.clicked.connect(self.open_login)

        # Main Window
        self.passHiddenFlag = True
        self.addFlag = False
        self.editFlag = False
        self.main.frame.setHidden(True)
        self.main.treeWidget.clicked.connect(self.FrameShow)
        self.main.btn_addAccount.clicked.connect(self.Frame_addAcount)
        self.main.btn_exit.clicked.connect(self.exit_app)
        self.main.btn_edit.clicked.connect(self.edit_data)
        self.main.pushButton_close.clicked.connect(self.FrameClose)
        self.main.pushButton_save.clicked.connect(self.save_data)
        self.main.btn_show.clicked.connect(self.password_show)
        self.main.btn_copy.clicked.connect(self.password_copy)
        self.main.btn_delete.clicked.connect(self.delete_data)
        self.main.btn_search.clicked.connect(self.search)
        self.main.lineEdit_search.textChanged.connect(self.search)
        self.main.btn_browser.clicked.connect(self.open_link)
        self.main.lineEdit_password.textChanged.connect(self.pass_strength)
        self.main.btn_logout.clicked.connect(self.logout)

        self.app.exec_()

    def pass_strength(self):
        if self.passHiddenFlag and (self.main.lineEdit_password.text() != '') and not(self.addFlag) and not(self.editFlag):
            items = data().get_record(login_id= self.id,
                                      tag= self.main.treeWidget.currentItem().text(1),
                                      username= self.main.treeWidget.currentItem().text(2),
                                      website= self.main.treeWidget.currentItem().text(4),
                                      category= self.main.treeWidget.currentItem().parent().text(0))
            password = hash().decrypt(self.key, items[0].password)
            strength = hash().CheckPasswordStrength(password)

        else:
            password = self.main.lineEdit_password.text()
            strength = hash().CheckPasswordStrength(password)

        if strength == 'weak':
            self.main.progressBar_strength.setValue(30)
            self.main.progressBar_strength.setStyleSheet('''QProgressBar {
                                                                border: 1px solid rgb(0, 0, 0);
                                                                border-radius: 10px;
                                                                text-align: center;
                                                                background-color: rgb(217, 217, 217);
                                                                color: black;
                                                            }
                                                            QProgressBar::chunk {
                                                                border-radius: 10px;
                                                                background-color: rgb(255, 70, 68);
                                                            }''')
            self.main.label_strength.setText('weak')
            self.main.label_strength.setStyleSheet('''  QLabel{
                                                            color: rgb(255, 70, 68); 
                                                        }''')

        elif strength == 'medium':
            self.main.progressBar_strength.setValue(60)
            self.main.progressBar_strength.setStyleSheet('''QProgressBar {
                                                                border: 1px solid rgb(0, 0, 0);
                                                                border-radius: 10px;
                                                                text-align: center;
                                                                background-color: rgb(217, 217, 217);
                                                                color: black;
                                                            }
                                                            QProgressBar::chunk {
                                                                border-radius: 10px;
                                                                background-color: rgb(254, 227, 48);
                                                            }''')
            self.main.label_strength.setText('medium')
            self.main.label_strength.setStyleSheet('''  QLabel{
                                                            color: rgb(254, 227, 48); 
                                                        }''')
        else:
            self.main.progressBar_strength.setValue(90)
            self.main.progressBar_strength.setStyleSheet('''QProgressBar {
                                                                border: 1px solid rgb(0, 0, 0);
                                                                border-radius: 10px;
                                                                text-align: center;
                                                                background-color: rgb(217, 217, 217);
                                                                color: black;
                                                            }
                                                            QProgressBar::chunk {
                                                                border-radius: 10px;
                                                                background-color: rgb(42, 219, 164);
                                                            }''')
            self.main.label_strength.setText('strong')
            self.main.label_strength.setStyleSheet('''  QLabel{
                                                            color: rgb(42, 219, 164); 
                                                        }''')


    def open_link(self):
        if self.main.treeWidget.currentItem().text(1) != '':
            webbrowser.open(self.main.treeWidget.currentItem().text(4))

    def display_tree(self, list):
        isparent, i = self.find_parent(list[0])
        if isparent:
            parent = self.main.treeWidget.topLevelItem(i)
            child = QTreeWidgetItem(parent)
            child.setText(1, list[1])
            child.setText(2, list[2])
            child.setText(3, list[3])
            child.setText(4, list[4])
        else:
            parent = QTreeWidgetItem(self.main.treeWidget)
            parent.setText(0, list[0].lower().title())
            child = QTreeWidgetItem(parent)
            # child.setText(0, parent.text(0))
            child.setText(1, list[1])
            child.setText(2, list[2])
            child.setText(3, list[3])
            child.setText(4, list[4])
        self.main.treeWidget.expandAll()   


    def search(self):
        self.main.frame.hide()
        items = data().get_everything(word=self.main.lineEdit_search.text(), id= self.id)
        self.main.treeWidget.clear()
        for item in items:
            password = hash().decrypt(keyInput= self.key, data= item.password)
            passShow = '*' * len(password)
            self.display_tree([item.category, item.tag, item.username, passShow, item.website])
        self.main.treeWidget.expandAll()   

    def delete_data(self):
        isParent, i = self.find_parent(self.main.treeWidget.currentItem().text(0))
        if self.main.treeWidget.currentItem().text(1) == '':
            record = self.main.treeWidget.topLevelItem(i).text(0)
            data().delete_parent(category= record, id= self.id)
            self.main.treeWidget.takeTopLevelItem(i)
        else:
            data().delete_data(login_id= self.id,
                               category= self.main.treeWidget.currentItem().parent().text(0),
                               tag= self.main.treeWidget.currentItem().text(1),
                               username= self.main.treeWidget.currentItem().text(2),
                               website= self.main.treeWidget.currentItem().text(4))
            self.main.treeWidget.currentItem().removeChild(self.main.treeWidget.currentItem())
            self.main.frame.hide()
            self.main.statusBar().showMessage('The record is deleted!', 2000)

            if self.main.treeWidget.topLevelItem(i).childCount() == 0:
                self.main.treeWidget.takeTopLevelItem(i)      
    
    def password_copy(self):
        if self.main.treeWidget.currentItem().text(1) != '':
            items = data().get_record(login_id= self.id,
                                      category= self.main.treeWidget.currentItem().parent().text(0),
                                      tag= self.main.treeWidget.currentItem().text(1),
                                      username= self.main.treeWidget.currentItem().text(2),
                                      website= self.main.treeWidget.currentItem().text(4))
            pyperclip.copy(hash().decrypt(keyInput= self.key, data= items[0].password))
            self.main.statusBar().showMessage('Password is copied!', 2000)
        
    def password_hide(self):
        self.main.btn_show.setIcon(QtGui.QIcon('./assets/view.png'))
        self.passHiddenFlag = True

    def password_show(self):
        if self.main.treeWidget.currentItem().text(1) != '':
            if self.passHiddenFlag:
                self.passHiddenFlag = False
                items = data().get_record(login_id= self.id,
                                          category= self.main.treeWidget.currentItem().parent().text(0),
                                          tag= self.main.treeWidget.currentItem().text(1),
                                          username= self.main.treeWidget.currentItem().text(2),
                                          website= self.main.treeWidget.currentItem().text(4))
                self.main.lineEdit_password.setText(hash().decrypt(keyInput=self.key, data= items[0].password))
                self.main.btn_show.setIcon(QtGui.QIcon('./assets/hide.png'))
            else:
                self.passHiddenFlag = True
                password = self.main.treeWidget.currentItem().text(3)
                passShow = '*' * len(password)
                self.main.lineEdit_password.setText(passShow)
                self.main.btn_show.setIcon(QtGui.QIcon('./assets/view.png'))


    def find_parent(self, text):
        for i in range(self.main.treeWidget.topLevelItemCount()):
            item = self.main.treeWidget.topLevelItem(i)
            if item.text(0) == text:
                return True, i
        return False, 0
    
    def save_data(self):
        self.main.label_edit.setText('Account')
        if self.addFlag:
            data().add_data(login_id= self.id,
                            category= self.main.lineEdit_category.text().lower().title(),
                            tag= self.main.lineEdit_tag.text(),
                            username= self.main.lineEdit_username.text(),
                            password= hash().encrypt(keyInput= self.key, data= self.main.lineEdit_password.text()),
                            website= self.main.lineEdit_website.text(),
                            note= hash().encrypt(keyInput= self.key, data= self.main.textEdit_note.toPlainText()))
            self.addFlag = False
        else:
            oldRecord = [   self.id,
                            self.main.treeWidget.currentItem().text(1),
                            self.main.treeWidget.currentItem().text(2),
                            self.main.treeWidget.currentItem().text(4),
                            self.main.treeWidget.currentItem().parent().text(0)]
            newRecord = [   self.main.lineEdit_tag.text(),
                            self.main.lineEdit_username.text(),
                            hash().encrypt(keyInput= self.key, data= self.main.lineEdit_password.text()),
                            self.main.lineEdit_website.text(),
                            self.main.lineEdit_category.text().lower().title(),
                            hash().encrypt(keyInput= self.key, data= self.main.textEdit_note.toPlainText())]
            data().update_data(oldRecord, newRecord)
            self.main.treeWidget.currentItem().removeChild(self.main.treeWidget.currentItem())
            self.editFlag = False

        passShow = '*' * len(self.main.lineEdit_password.text())
        self.display_tree([self.main.lineEdit_category.text().lower().title(),
                           self.main.lineEdit_tag.text(),
                           self.main.lineEdit_username.text(),
                           passShow,
                           self.main.lineEdit_website.text()])
        self.main.frame.hide()   

    def open_login(self):
        self.signupWindow.hide()
        self.main.hide()
        self.loginWindow.show()

    def display_data(self):
        items = data().get_data(self.id)
        for item in items:
            password = hash().decrypt(keyInput= self.key, data= item.password)
            passShow = '*' * len(password)
            self.display_tree([item.category, item.tag, item.username, passShow, item.website])

    def check_user(self):
        try: 
            password = hash().hashcrypt(self.loginWindow.password.text())
            username = self.loginWindow.username.text()
            items = data().get_user(username)
            if items[0].password == password:
                self.id = items[0].id
                self.key = items[0].key
                self.loginWindow.hide()
                self.display_data()
                self.main.show()
                self.main.label_welcome.setText(f'Welcome back {items[0].username} ')
            else:
                QMessageBox.warning(None, 'Wrong Input', 'Incorrect username or password. Please try again!')
                self.loginWindow.username.setText('')
                self.loginWindow.password.setText('')
        except: 
            QMessageBox.warning(None, 'No user confirm', 'Create an account first!')
            self.loginWindow.username.setText('')
            self.loginWindow.password.setText('')

    def add_user(self):
        if self.signupWindow.password.text() == self.signupWindow.password2.text():
            password = hash().hashcrypt(self.signupWindow.password.text())
            username = self.signupWindow.username.text()
            encryptKey = hash().get_key()
            data().add_user(userInput= username, passInput= password, keyInput= encryptKey)
            self.signupWindow.hide()
            self.loginWindow.show()
        else:
            QMessageBox.warning(None, 'Wrong Input', 'Passwords are not match. Please try again!')
            self.signupWindow.password2.setText('')
            self.signupWindow.password.setText('')
        self.signupWindow.username.setText('')
        self.signupWindow.password.setText('')
        self.signupWindow.password2.setText('')

    def FrameShow(self):
        self.main.label_edit.setText('Account')
        self.password_hide()
        self.main.frame.setHidden(False)
        self.main.lineEdit_password.setText(self.main.treeWidget.currentItem().text(3))
        self.main.lineEdit_password.setReadOnly(True)
        self.main.lineEdit_username.setText(self.main.treeWidget.currentItem().text(2))
        self.main.lineEdit_username.setReadOnly(True)
        self.main.lineEdit_website.setText(self.main.treeWidget.currentItem().text(4))
        self.main.lineEdit_website.setReadOnly(True)
        self.main.lineEdit_tag.setText(self.main.treeWidget.currentItem().text(1))
        self.main.lineEdit_tag.setReadOnly(True)
        self.main.lineEdit_category.setReadOnly(True)
        self.main.textEdit_note.setReadOnly(True)
        self.main.pushButton_save.hide()
        if self.main.treeWidget.currentItem().text(2) != '':
            items = data().get_record(login_id= self.id,
                                    tag= self.main.treeWidget.currentItem().text(1),
                                    username= self.main.treeWidget.currentItem().text(2),
                                    website= self.main.treeWidget.currentItem().text(4),
                                    category= self.main.treeWidget.currentItem().parent().text(0))
            self.main.textEdit_note.setText(hash().decrypt(keyInput= self.key, data= items[0].note))
            self.main.lineEdit_category.setText(self.main.treeWidget.currentItem().parent().text(0))
        else:
            self.main.textEdit_note.setText('')
            self.main.lineEdit_tag.setText('')
            self.main.lineEdit_category.setText('')
        self.shown()

    def logout(self):
        self.id = 0
        self.key = ''
        self.loginWindow.username.setText('')
        self.loginWindow.password.setText('')
        self.main.treeWidget.clear()
        self.main.frame.hide()
        self.open_login()

    def exit_app(self):
       sys.exit()


    def FrameClose(self):
        self.editFlag = False
        self.addFlag = False
        self.password_hide()
        self.main.frame.setHidden(True)

    def Frame_addAcount(self):
        self.main.label_edit.setText('Add Account')
        self.addFlag = True
        self.main.frame.setHidden(False)
        self.main.lineEdit_tag.setReadOnly(False)
        self.main.lineEdit_tag.setText('')
        self.main.lineEdit_username.setText('')
        self.main.lineEdit_username.setReadOnly(False)
        self.main.lineEdit_password.setText('')
        self.main.lineEdit_password.setReadOnly(False)
        self.main.lineEdit_website.setText('')
        self.main.lineEdit_website.setReadOnly(False)
        self.main.lineEdit_category.setText('')
        self.main.lineEdit_category.setReadOnly(False)
        self.main.textEdit_note.setText('')
        self.main.textEdit_note.setReadOnly(False)
        self.main.pushButton_save.show()
        self.hidden()

    def hidden(self):
        self.main.btn_browser.hide()
        self.main.btn_show.hide()
        self.main.btn_copy.hide()
        self.main.btn_edit.hide()
        self.main.btn_delete.hide()

    def shown(self):
        self.main.btn_browser.show()
        self.main.btn_show.show()
        self.main.btn_copy.show()
        self.main.btn_edit.show()
        self.main.btn_delete.show()

    def edit_data(self):
        if self.main.treeWidget.currentItem().text(1) != '':
            self.editFlag = True
            self.addFlag = False
            self.main.label_edit.setText('Edit Account')
            self.main.pushButton_save.show()
            self.main.lineEdit_tag.setReadOnly(False)
            self.main.lineEdit_username.setReadOnly(False)
            self.main.lineEdit_password.setReadOnly(False)
            self.main.lineEdit_website.setReadOnly(False)
            self.main.lineEdit_category.setReadOnly(False)
            self.main.textEdit_note.setReadOnly(False)
            items = data().get_record(login_id= self.id,
                                      tag= self.main.treeWidget.currentItem().text(1),
                                      username= self.main.treeWidget.currentItem().text(2),
                                      website= self.main.treeWidget.currentItem().text(4),
                                      category= self.main.treeWidget.currentItem().parent().text(0))
            self.main.lineEdit_password.setText(hash().decrypt(keyInput= self.key, data= items[0].password))

    def open_signup(self):
        self.loginWindow.username.setText('')
        self.loginWindow.password.setText('')
        self.loginWindow.hide()
        self.signupWindow.show()


if __name__ == '__main__':
    window()