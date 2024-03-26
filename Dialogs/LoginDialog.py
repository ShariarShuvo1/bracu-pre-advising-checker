from PyQt6.QtCore import Qt, QSize, QEvent
from PyQt6.QtGui import QIcon, QMovie
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QCheckBox, QPushButton, QMessageBox

from CustomWidget.PasswordLineEdit import PasswordLineEdit
from Functions.is_valid_email import is_valid_email
from Functions.security_info import security_info
from Settings.SettingsData import set_setting
from Stylesheet.LoginDialogStylesheet import *
from Stylesheet.ProfileDialogStylesheet import DIALOG_STYLE
from Threads.LoginThread import LoginThread


class LoginDialog(QDialog):
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

        self.email_label: QLabel = QLabel("Email")
        self.email_label.setStyleSheet(EMAIL_LABEL_STYLE)
        self.email_label.setFixedHeight(40)
        self.email_label.setFixedWidth(100)

        self.email_input: QLineEdit = QLineEdit()
        self.email_input.setToolTip("Enter your USIS email\n"
                                    "Remember your Gsuit email is not your USIS email")
        self.email_input.setFixedHeight(40)
        self.email_input.setStyleSheet(EMAIL_INPUT_STYLE)
        self.email_input.setPlaceholderText("Enter your USIS email")
        self.email_input.setClearButtonEnabled(True)
        self.email_input.installEventFilter(self)

        self.password_label: QLabel = QLabel("Password")
        self.password_label.setStyleSheet(EMAIL_LABEL_STYLE)
        self.password_label.setFixedHeight(40)
        self.password_label.setFixedWidth(100)

        self.password_input: PasswordLineEdit = PasswordLineEdit()
        self.password_input.setToolTip("Enter your USIS password")
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet(EMAIL_INPUT_STYLE)
        self.password_input.setPlaceholderText("Enter your USIS password")
        self.password_input.installEventFilter(self)

        self.remember_me_checkbox: QCheckBox = QCheckBox("Remember Me")
        self.remember_me_checkbox.setToolTip("Check this box to save your login credentials\n"
                                             "This will allow you to login automatically next time you open the app\n"
                                             "Click the info button to know more about security")
        self.remember_me_checkbox.setStyleSheet(REMEMBER_ME_CHECKBOX_STYLE)
        self.remember_me_checkbox.setMaximumHeight(40)
        self.remember_me_checkbox.setChecked(False)

        self.info_button: QPushButton = QPushButton()
        self.info_button.setIcon(QIcon("./Assets/Icons/info.png"))
        self.info_button.setIconSize(QSize(30, 30))
        self.info_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.info_button.setToolTip("Click here to know more about security")
        self.info_button.setFixedSize(30, 30)
        self.info_button.setStyleSheet(INFO_BUTTON_STYLE)
        self.info_button.clicked.connect(security_info)

        self.login_button: QPushButton = QPushButton("Login")
        self.login_button.setToolTip("Click here to login to your USIS account")
        self.login_button.setFixedHeight(40)
        self.login_button.setStyleSheet(LOGIN_BUTTON_STYLE)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setFixedWidth(200)
        self.login_button.clicked.connect(self.login_button_clicked)

        self.loading_label = QLabel()
        self.loading_label.setToolTip("Logging in... Please wait")
        self.loading_label.setStyleSheet(LOADING_LABEL_STYLE)
        self.loading_label.setFixedHeight(40)
        self.loading_label.setFixedWidth(200)
        self.loading_label.setVisible(False)
        loading_gif = QMovie("./Assets/Icons/loading.gif")
        loading_gif.setScaledSize(QSize(30, 30))
        self.loading_label.setMovie(loading_gif)
        loading_gif.start()
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()

        self.status_label: QLabel = QLabel()
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.status_label.setFixedHeight(20)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.email_row: QHBoxLayout = QHBoxLayout()
        self.email_row.addWidget(self.email_label)
        self.email_row.addWidget(self.email_input)

        self.password_row: QHBoxLayout = QHBoxLayout()
        self.password_row.addWidget(self.password_label)
        self.password_row.addWidget(self.password_input)

        self.main_layout.addLayout(self.email_row)
        self.main_layout.addLayout(self.password_row)

        self.remember_row: QHBoxLayout = QHBoxLayout()
        self.remember_row.addWidget(self.remember_me_checkbox)
        self.remember_row.addStretch()
        self.remember_row.addWidget(self.info_button)

        self.main_layout.addLayout(self.remember_row)

        self.login_row: QHBoxLayout = QHBoxLayout()
        self.login_row.addStretch()
        self.login_row.addWidget(self.login_button)
        self.login_row.addWidget(self.loading_label)
        self.login_row.addStretch()

        self.main_layout.addLayout(self.login_row)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addStretch()
        self.main_layout.addSpacing(10)

        self.login_thread: LoginThread | None = None

    def login_button_clicked(self):
        email = self.email_input.text()
        password = self.password_input.text()
        if not self.input_validation(email, password):
            return

        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.email_input.setStyleSheet(EMAIL_INPUT_STYLE)
        self.password_input.setStyleSheet(EMAIL_INPUT_STYLE)
        self.disable_all()

        self.login_thread = LoginThread(self.main, email, password)
        self.login_thread.status_update.connect(self.login_thread_status_update)
        self.login_thread.start()

    def enable_all(self):
        self.loading_label.hide()
        self.email_input.setEnabled(True)
        self.password_input.setEnabled(True)
        self.remember_me_checkbox.setEnabled(True)
        self.login_button.show()

    def disable_all(self):
        self.loading_label.show()
        self.email_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.remember_me_checkbox.setEnabled(False)
        self.login_button.hide()

    def login_thread_status_update(self, status):
        self.status_label.setText(status)
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        if (status == "No internet connection" or
                status == "USIS connection failed" or
                status == "Login failed. Invalid email or password"):
            self.status_label.setStyleSheet(STATUS_LABEL_ERROR_STYLE)
            self.enable_all()
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
                self.email_input.setStyleSheet(EMAIL_INPUT_ERROR_STYLE)
                self.password_input.setStyleSheet(EMAIL_INPUT_ERROR_STYLE)
            msg_box.setWindowIcon(QIcon("./Assets/logo.png"))
            msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        elif status == "USIS connection found" or status == "Internet connection found" or status == "Login successful":
            self.status_label.setStyleSheet(STATUS_LABEL_SUCCESS_STYLE)
            if status == "Login successful":
                self.login_success()

    def login_success(self):
        self.enable_all()
        set_setting("IS_LOGGED_IN", True)
        if self.remember_me_checkbox.isChecked():
            set_setting("IS_LOGGED_IN_INFO_SAVED", True)
            set_setting("EMAIL", self.email_input.text())
            set_setting("PASSWORD", self.password_input.text())
        else:
            set_setting("IS_LOGGED_IN_INFO_SAVED", False)
            set_setting("EMAIL", "")
            set_setting("PASSWORD", "")
        self.main.logged_in(True)
        self.close()

    def email_validation(self, email):
        if not email:
            self.status_label.setText("Please enter your email")
            self.status_label.setStyleSheet(STATUS_LABEL_ERROR_STYLE)
            self.email_input.setStyleSheet(EMAIL_INPUT_ERROR_STYLE)
            return False
        elif not is_valid_email(email):
            self.status_label.setText("Please enter a valid email")
            self.status_label.setStyleSheet(STATUS_LABEL_ERROR_STYLE)
            self.email_input.setStyleSheet(EMAIL_INPUT_ERROR_STYLE)
            return False
        elif email.split("@")[1] == "g.bracu.ac.bd":
            self.status_label.setText("Your Gsuit email is not your USIS email")
            self.status_label.setStyleSheet(STATUS_LABEL_ERROR_STYLE)
            self.email_input.setStyleSheet(EMAIL_INPUT_ERROR_STYLE)
            return False
        return True

    def password_validation(self, password):
        if not password:
            self.status_label.setText("Please enter your password")
            self.status_label.setStyleSheet(STATUS_LABEL_ERROR_STYLE)
            self.password_input.setStyleSheet(EMAIL_INPUT_ERROR_STYLE)
            return False
        return True

    def input_validation(self, email, password):
        if not email and not password:
            self.status_label.setText("Please enter your email and password")
            self.status_label.setStyleSheet(STATUS_LABEL_ERROR_STYLE)
            self.email_input.setFocus()
            self.email_input.setStyleSheet(EMAIL_INPUT_ERROR_STYLE)
            self.password_input.setStyleSheet(EMAIL_INPUT_ERROR_STYLE)
            return False
        elif not self.email_validation(email) or not self.password_validation(password):
            return False
        return True

    def eventFilter(self, obj, event):
        if obj == self.email_input or obj == self.password_input:
            if obj == self.email_input and event.type() == QEvent.Type.KeyRelease:
                if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                    self.password_input.toggle_button.setChecked(True)
                    if self.input_validation(self.email_input.text(), self.password_input.text()):
                        self.login_button_clicked()
                    elif self.email_validation(self.email_input.text()):
                        self.password_input.setFocus()

                if self.email_validation(self.email_input.text()):
                    obj.setStyleSheet(EMAIL_INPUT_STYLE)
                    self.status_label.setText("")
                    self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
            elif obj == self.password_input and event.type() == QEvent.Type.KeyRelease:
                if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                    self.login_button_clicked()
                    self.password_input.toggle_button.setChecked(True)
                elif self.password_validation(self.password_input.text()):
                    obj.setStyleSheet(EMAIL_INPUT_STYLE)
                    self.status_label.setText("")
                    self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
            return False
        return False

    def closeEvent(self, event):
        if self.login_thread:
            self.login_thread.terminate()
        self.email_input.clear()
        self.password_input.clear()
        self.status_label.setText("")
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.email_input.setStyleSheet(EMAIL_INPUT_STYLE)
        self.password_input.setStyleSheet(EMAIL_INPUT_STYLE)
        self.enable_all()
        event.accept()
