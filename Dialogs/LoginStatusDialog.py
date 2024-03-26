from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox, QPushButton

from Functions.logout import logout
from Settings.SettingsData import set_setting, get_setting
from Stylesheet.LoginStatusDialogStylesheet import STATUS_LABEL_STYLE, STATUS_LABEL_ERROR_STYLE, \
    STATUS_LABEL_SUCCESS_STYLE, TRY_AGAIN_BUTTON_STYLE
from Stylesheet.ProfileDialogStylesheet import DIALOG_STYLE
from Threads.LoginThread import LoginThread


class LoginStatusDialog(QDialog):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.setWindowTitle("Log in to USIS")
        self.setMinimumWidth(600)
        self.setWindowIcon(QIcon("./Assets/logo.png"))
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)
        self.setStyleSheet(DIALOG_STYLE)

        self.status_label: QLabel = QLabel()
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.try_again_button: QPushButton = QPushButton("Try again")
        self.try_again_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.try_again_button.clicked.connect(self.login_begun)
        self.try_again_button.setStyleSheet(TRY_AGAIN_BUTTON_STYLE)
        self.try_again_button.setIcon(QIcon("./Assets/Icons/retry.png"))
        self.try_again_button.setIconSize(QSize(20, 20))
        self.try_again_button.setDisabled(True)

        self.main_layout.addWidget(self.status_label)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.try_again_button)

        self.login_thread: LoginThread | None = None
        self.login_begun()
        self.exec()

    def login_begun(self):
        self.try_again_button.setHidden(True)
        self.try_again_button.setDisabled(False)
        email = get_setting("EMAIL")
        password = get_setting("PASSWORD")
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)

        self.login_thread = LoginThread(self.main, email, password)
        self.login_thread.status_update.connect(self.login_thread_status_update)
        self.login_thread.start()

    def login_thread_status_update(self, status):
        self.status_label.setText(status)
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        if (status == "No internet connection" or
                status == "USIS connection failed" or
                status == "Login failed. Invalid email or password"):
            self.status_label.setStyleSheet(STATUS_LABEL_ERROR_STYLE)
            msg_box = QMessageBox()
            msg_box.setWindowTitle(status)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setText(status)
            if status == "No internet connection":
                msg_box.setInformativeText("Please check your internet connection and try again")
            elif status == "USIS connection failed":
                msg_box.setInformativeText("USIS is down right now. Use offline mode or try again later")
            elif status == "Login failed. Invalid email or password":
                msg_box.setInformativeText("Please check your email and password and try again")
            msg_box.setWindowIcon(QIcon("./Assets/logo.png"))
            msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            self.login_failed()
        elif status == "USIS connection found" or status == "Internet connection found" or status == "Login successful":
            self.status_label.setStyleSheet(STATUS_LABEL_SUCCESS_STYLE)
            if status == "Login successful":
                self.login_success()

    def login_success(self):
        self.try_again_button.setHidden(False)
        set_setting("IS_LOGGED_IN", True)
        self.try_again_button.setDisabled(True)
        self.main.logged_in(True)
        self.close()

    def login_failed(self):
        self.try_again_button.setHidden(False)
        self.status_label.setStyleSheet(STATUS_LABEL_ERROR_STYLE)
        self.try_again_button.setDisabled(False)

    def closeEvent(self, event):
        if self.login_thread:
            self.login_thread.terminate()
        self.status_label.setText("")
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        if self.try_again_button.isEnabled():
            self.main.logged_in(False)
            logout(self.main)
            self.try_again_button.setDisabled(True)
        event.accept()
