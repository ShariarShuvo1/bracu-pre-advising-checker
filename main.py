import webbrowser
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon
from basic import Ui_BasicWindow
from advance import Ui_AdvanceWindow
from login import Ui_LoginWindow
from internetChecker import internet_checker
from ObjectBuilder import object_builder


def myNameClicked():
    webbrowser.open_new('https://www.facebook.com/ShariarShuvo01/')


def githubClicked():
    webbrowser.open_new('https://github.com/ShariarShuvo1/bracu-pre-advising-checker')


class Ui_MainWindow(object):
    def __init__(self):
        self.github = None
        self.my_name = None
        self.main_ui = None
        self.login_ui = None
        self.LoginWindow = None
        self.login_window_generated = False
        self.width = None
        self.height = None
        self.pointingHandMouse = QCursor(Qt.CursorShape.PointingHandCursor)
        self.advance_ui = None
        self.advanceWindow = None
        self.basic_ui = None
        self.basicWindow = None
        self.myName = None
        self.advance_button = None
        self.comment_text_2 = None
        self.heading_text_2 = None
        self.basic_button = None
        self.comment_text_1 = None
        self.heading_text_1 = None
        self.centralwidget = None
        self.header = None
        self.basic_window_generated = False
        self.advance_window_generated = False

    def setupUi(self, MainWindow, main_ui):

        icon_path = "./icon.png"  # Replace with the actual path to your icon file
        icon = QIcon(icon_path)
        MainWindow.setWindowIcon(icon)

        self.main_ui = main_ui
        MainWindow.resize(900, 600)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))
        MainWindow.setBaseSize(QtCore.QSize(900, 600))
        MainWindow.setStyleSheet("background-color: black; color: yellow")
        MainWindow.setWindowTitle("Pre Advising")

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)

        # header
        self.header = object_builder(QtWidgets.QLabel(parent=self.centralwidget), (219, 69, 461, 101), "Pre Advising",
                                     60, True, "")
        self.header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Name
        self.myName: QtWidgets.QPushButton = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (506, 152, 151, 20),
                                     "by Shariar Islam Shuvo", None, True,
                                     "QPushButton::!hover{background-color: rgba(0, 0, 0, 0);} QPushButton::hover{background-color: rgba(0, 0, 0, 0); color:red;}",
                                     myNameClicked, None, "You are welcome :)")

        # Heading Text 1
        self.heading_text_1 = object_builder(QtWidgets.QLabel(parent=self.centralwidget), (124, 280, 261, 71),
                                             "Basic Advising", 20, True, "background-color: rgba(23, 23, 23, 1);")
        self.heading_text_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Comment Text 1
        self.comment_text_1 = object_builder(QtWidgets.QLabel(parent=self.centralwidget), (124, 351, 261, 91),
                                             "This mode will only work during Pre Advising time [NO USIS SIGN IN REQUIRED]",
                                             None, True, "background-color: rgba(23, 23, 23, 1); color:white")
        self.comment_text_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.comment_text_1.setWordWrap(True)

        # Basic Button
        self.basic_button = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (124, 280, 265, 166), None,
                                           None, False,
                                           "QPushButton::!hover{border: 2px solid yellow; background-color: rgba(0, 0, 0, 0);} QPushButton::hover{border : 2px solid red; background-color: rgba(0, 0, 0, 0);};",
                                           self.basicButtonClicked, self.pointingHandMouse,
                                           "This mode will update data from https://admissions.bracu.ac.bd/academia/admissionRequirement/getAvailableSeatStatus which is not always accurate")

        # Heading Text 2
        self.heading_text_2 = object_builder(QtWidgets.QLabel(parent=self.centralwidget), (513, 280, 261, 71),
                                             "Advance Advising", 20, True, "background-color: rgba(23, 23, 23, 1);")
        self.heading_text_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Comment Text 2
        self.comment_text_2 = object_builder(QtWidgets.QLabel(parent=self.centralwidget), (513, 351, 261, 91),
                                             "This mode will always work [USIS SIGN IN REQUIRED]", None, True,
                                             "background-color: rgba(23, 23, 23, 1); color:white")
        self.comment_text_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.comment_text_2.setWordWrap(True)

        # Advance Button
        self.advance_button = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (511, 280, 265, 166),
                                             None, None, False,
                                             "QPushButton::!hover{border: 2px solid yellow; background-color: rgba(0, 0, 0, 0);} QPushButton::hover{border : 2px solid red; background-color: rgba(0, 0, 0, 0);};",
                                             self.advanceButtonClicked, self.pointingHandMouse,
                                             "This mode will update data directly from USIS which is much more accurate than basic mode")

        self.my_name = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (30, 560, 200, 20),
                                      "Created By: Shariar Islam Shuvo", 10, False,
                                      "QPushButton::hover{color:red}", myNameClicked, self.pointingHandMouse,
                                      "Click to visit my Facebook Profile")
        self.github = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (250, 560, 150, 20), "GitHub", 12,
                                     False, "QPushButton::hover{color:red}", githubClicked, self.pointingHandMouse,
                                     "Click to visit GitHub repo for this project")

        # Initiate texts
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def basicButtonClicked(self):
        if internet_checker():
            MainWindow.hide()
            if not self.basic_window_generated:
                self.basic_window_generated = True
                self.basicWindow = QtWidgets.QMainWindow()
                self.basic_ui = Ui_BasicWindow()
                self.basic_ui.height = self.height
                self.basic_ui.width = self.width
                self.basic_ui.setupUi(self.basicWindow, MainWindow, self.basic_ui)
            self.basicWindow.show()

    def loggedIn(self, session):
        if not self.advance_window_generated:
            self.advance_window_generated = True
            self.advanceWindow = QtWidgets.QMainWindow()
            self.advance_ui = Ui_AdvanceWindow()
            self.advance_ui.height = self.height
            self.advance_ui.width = self.width
            self.advance_ui.setupUi(self.advanceWindow, MainWindow, self.advance_ui, session)
        self.advanceWindow.show()

    def advanceButtonClicked(self):
        if internet_checker():
            MainWindow.hide()
            if not self.login_window_generated:
                self.login_window_generated = True
                self.LoginWindow = QtWidgets.QMainWindow()
                self.login_ui = Ui_LoginWindow()
                self.login_ui.height = self.height
                self.login_ui.width = self.width
                self.login_ui.setupUi(self.LoginWindow, MainWindow, self.main_ui)
                self.LoginWindow.show()
            else:
                self.advanceWindow.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    screenSize = app.screens()[0].availableGeometry()
    ui.height = screenSize.height()
    ui.width = screenSize.width()
    ui.setupUi(MainWindow, ui)
    MainWindow.show()
    sys.exit(app.exec())
