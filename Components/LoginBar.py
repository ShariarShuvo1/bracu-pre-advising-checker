from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QPushButton, QLabel

from CustomWidget.LoginPushButton import LoginPushButton
from Settings.SettingsData import get_setting
from Stylesheet.LoginBarStylesheet import *


class LoginBar:
    def __init__(self, main=None):
        self.main = main
        self.login_bar_widget: QWidget = QWidget()
        self.login_bar_layout: QHBoxLayout = QHBoxLayout()
        self.login_bar_layout.setContentsMargins(2, 2, 2, 2)
        self.login_bar_widget.setLayout(self.login_bar_layout)
        self.login_bar_widget.setStyleSheet(LOGIN_BAR_STYLE)
        self.login_bar_widget.setMaximumHeight(50)

        self.login_button: LoginPushButton = LoginPushButton(self.main)
        self.login_button.clicked.connect(self.login_button_clicked)

        self.login_bar_message: QLabel = QLabel(
            "Please login to your USIS account to access all features")
        self.login_bar_message.setStyleSheet(LOGIN_BAR_MESSAGE_STYLE)

        self.close_button: QPushButton = QPushButton()
        self.close_button.setToolTip("Remove this login message")
        self.close_button.setStyleSheet(CLOSE_BUTTON_STYLE)
        self.close_button.setIcon(QIcon("./Assets/Icons/close.png"))
        self.close_button.setIconSize(QSize(30, 30))
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.setFixedSize(30, 30)
        self.close_button.mouseMoveEvent = self.close_button_hover
        self.close_button.leaveEvent = self.close_button_leave
        self.close_button.clicked.connect(lambda: self.login_bar_widget.hide())

        self.login_bar_layout.addWidget(self.login_button)
        self.login_bar_layout.addWidget(self.login_bar_message)
        self.login_bar_layout.addStretch()
        self.login_bar_layout.addWidget(self.close_button)

        if get_setting("IS_LOGGED_IN"):
            self.login_bar_widget.hide()

    def login_button_clicked(self):
        self.login_button.login_dialog.exec()

    def close_button_hover(self, event: QMouseEvent):
        self.login_bar_widget.setStyleSheet(LOGIN_BAR_STYLE_HOVER)
        self.login_button.setStyleSheet(LOGIN_BUTTON_STYLE_HOVER)
        self.close_button.setStyleSheet(CLOSE_BUTTON_STYLE_HOVER)

    def close_button_leave(self, event: QMouseEvent):
        self.login_bar_widget.setStyleSheet(LOGIN_BAR_STYLE)
        self.login_button.setStyleSheet(LOGIN_BUTTON_STYLE)
        self.close_button.setStyleSheet(CLOSE_BUTTON_STYLE)
