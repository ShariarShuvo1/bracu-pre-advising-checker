from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton

from Dialogs.LoginDialog import LoginDialog
from Stylesheet.LoginBarStylesheet import *


class LoginPushButton(QPushButton):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.setText("Login to USIS")
        self.setToolTip("Click here to login to your USIS account\n"
                        "This will ensure up-to-date data\n"
                        "It will also enable features like TBA prediction")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMaximumWidth(200)
        self.setStyleSheet(LOGIN_BUTTON_STYLE)
        self.setIcon(QIcon("./Assets/Icons/profile-black.png"))
        self.setIconSize(QSize(20, 20))
        self.login_dialog = LoginDialog(self.main)
