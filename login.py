from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel
from bs4 import BeautifulSoup
from ObjectBuilder import object_builder
import requests


class Ui_LoginWindow(object):

    def __init__(self):
        self.main_ui = None
        self.MainWindow = None
        self.message: QLabel = None
        self.LoginWindow = None
        self.s = None
        self.login: QPushButton = None
        self.password: QLineEdit = None
        self.email: QLineEdit = None
        self.centralwidget = None

    def setupUi(self, LoginWindow, MainWindow, main_ui):
        icon_path = "./icon.png"  # Replace with the actual path to your icon file
        icon = QIcon(icon_path)
        LoginWindow.setWindowIcon(icon)
        self.LoginWindow = LoginWindow
        self.MainWindow = MainWindow
        self.main_ui = main_ui
        self.s = requests.Session()
        LoginWindow.setStyleSheet("background-color: black; color: yellow")
        LoginWindow.setWindowTitle("Sign In")
        LoginWindow.setFixedSize(450, 220)
        self.centralwidget = QtWidgets.QWidget(parent=LoginWindow)

        self.email = object_builder(QtWidgets.QLineEdit(parent=self.centralwidget), (20, 20, 400, 40), "USIS Email (ex: iub.an.nasser@gmail.com)", 15,
                                    True, "background-color: rgba(23, 23, 23, 1); border: 1px solid darkgray;")

        self.password: QtWidgets.QLineEdit = object_builder(QtWidgets.QLineEdit(parent=self.centralwidget), (20, 70, 400, 40),
                                       "USIS Password", 15, True, "background-color: rgba(23, 23, 23, 1); border: 1px solid darkgray;")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (175, 120, 100, 40), "Login", 15,
                                    True,
                                    "QPushButton::!hover{border: 2px solid yellow; background-color: rgba(0, 0, 0, 0);} QPushButton::hover{border : 2px solid red; background-color: rgba(0, 0, 0, 0);};",
                                    self.loginClicked)

        self.message = object_builder(QtWidgets.QLabel(parent=self.centralwidget), (20, 170, 350, 20), "", 13, False,
                                      "background-color: black;")

        LoginWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def loginChecker(self):
        loginPage = self.s.get('https://usis.bracu.ac.bd/academia/dashBoard/show')
        html = BeautifulSoup(loginPage.content, 'html.parser')
        if len(str(html)) < 20000:
            return False
        else:
            return True

    def do_login(self):
        email = self.email.text()
        password = self.password.text()
        self.s.get("https://usis.bracu.ac.bd/academia/j_spring_security_check")
        self.s.post("https://usis.bracu.ac.bd/academia/j_spring_security_check",
                    data={'j_username': email, 'j_password': password})
        if self.loginChecker():
            self.LoginWindow.hide()
            self.main_ui.loggedIn(self.s)
        else:
            self.message.setText("Wrong Email/Password. Try Again!")

    def loginClicked(self):
        self.message.setText("")
        self.do_login()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    screenSize = app.screens()[0].availableGeometry()
    ui.height = screenSize.height()
    ui.width = screenSize.width()
    ui.setupUi(LoginWindow, None, ui)
    LoginWindow.show()
    sys.exit(app.exec())
