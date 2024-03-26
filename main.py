import sys

import requests
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from Components.FooterBar import FooterBar
from Dialogs.LoginStatusDialog import LoginStatusDialog
from Entity.Profile import Profile
from Settings.SettingsData import get_setting
from Stylesheet.MainWindowStylesheet import *
from Components.LoginBar import LoginBar


class MainWindow(QMainWindow):
    is_already_logged_in: pyqtSignal = pyqtSignal()

    def already_logged_in(self):
        if get_setting("IS_LOGGED_IN_INFO_SAVED"):
            LoginStatusDialog(self)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BRACU Pre Advising Checker")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon("./Assets/logo.png"))
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(1, 1, 1, 0)
        self.main_layout.setSpacing(1)
        self.main_widget: QWidget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.session: requests.sessions = requests.Session()
        self.profile: Profile | None = None
        self.current_session_id: str = "627123"

        self.login_bar: LoginBar = LoginBar(self)

        self.footer_bar: FooterBar = FooterBar(self)

        self.main_layout.addWidget(self.login_bar.login_bar_widget)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.footer_bar.footer_bar_widget)
        self.is_already_logged_in.connect(self.already_logged_in)

    def logged_in(self, login: bool):
        if login:
            self.login_bar.login_bar_widget.hide()
            self.footer_bar.login_button.hide()
            self.footer_bar.profile_button.show()
            self.footer_bar.logout_button.show()
            self.footer_bar.get_resource()
        else:
            self.login_bar.login_bar_widget.show()
            self.footer_bar.login_button.show()
            self.footer_bar.profile_button.hide()
            self.footer_bar.logout_button.hide()


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.setStyleSheet(MAIN_WINDOW_STYLE)
    window.showMaximized()
    window.show()
    window.is_already_logged_in.emit()
    sys.exit(app.exec())
