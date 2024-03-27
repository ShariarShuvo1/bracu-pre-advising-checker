from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QPushButton

from CustomWidget.LoginPushButton import LoginPushButton
from Dialogs.ProfileDialog import ProfileDialog
from Entity.Profile import Profile
from Functions.logout import logout
from Settings.SettingsData import get_setting
from Stylesheet.FooterBarStylesheet import *
from Threads.ProfileInfoThread import ProfileInfoThread


class FooterBar:
    def __init__(self, main=None):
        self.main = main
        self.footer_bar_widget: QWidget = QWidget()
        self.footer_bar_layout: QHBoxLayout = QHBoxLayout()
        self.footer_bar_layout.setContentsMargins(2, 2, 2, 2)
        self.footer_bar_widget.setLayout(self.footer_bar_layout)
        self.footer_bar_widget.setStyleSheet(FOOTER_BAR_STYLE)
        self.footer_bar_widget.setMaximumHeight(50)

        self.login_button: LoginPushButton = LoginPushButton(self.main)
        self.login_button.clicked.connect(self.login_button_clicked)

        self.profile_button: QPushButton = QPushButton()
        self.profile_button.setStyleSheet(PROFILE_BUTTON_STYLE)
        self.profile_button.setIcon(QIcon("./Assets/Icons/profile-white.png"))
        self.profile_button.setText("Loading...")
        self.profile_button.setIconSize(QSize(28, 28))
        self.profile_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profile_button.setToolTip("View your profile")
        self.profile_button.setMaximumHeight(40)
        self.profile_button.hide()
        self.profile_button.setDisabled(True)
        self.profile_button.clicked.connect(self.profile_button_clicked)

        self.logout_button: QPushButton = QPushButton("Logout")
        self.logout_button.setStyleSheet(LOGOUT_BUTTON_STYLE)
        self.logout_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_button.setToolTip("Logout from your account")
        self.logout_button.clicked.connect(self.logout_button_clicked)
        self.logout_button.setMaximumHeight(40)
        self.logout_button.hide()

        self.footer_bar_layout.addWidget(self.login_button)
        self.footer_bar_layout.addWidget(self.profile_button)
        self.footer_bar_layout.addWidget(self.logout_button)
        self.footer_bar_layout.addStretch()
        self.profile_info_thread: ProfileInfoThread | None = None
        self.is_logged_in()

    def profile_button_clicked(self):
        profile_dialog = ProfileDialog(self.main)
        profile_dialog.exec()

    def logout_button_clicked(self):
        self.profile_button.setDisabled(True)
        self.profile_button.setIcon(QIcon("./Assets/Icons/profile-white.png"))
        self.profile_button.setText("Loading...")
        logout(self.main)

    def profile_info_found(self, profile: Profile):
        self.profile_button.setDisabled(False)
        self.main.profile = profile
        self.profile_button.setText(profile.name)
        pixmap = QPixmap()
        pixmap.loadFromData(profile.picture.content)
        self.profile_button.setIcon(QIcon(pixmap))

    def get_resource(self):
        self.profile_info_thread = ProfileInfoThread(self.main)
        self.profile_info_thread.info_found.connect(self.profile_info_found)
        self.profile_info_thread.start()

    def is_logged_in(self):
        if get_setting("IS_LOGGED_IN"):
            self.login_button.hide()
            self.profile_button.show()
            self.logout_button.show()
        else:
            self.login_button.show()
            self.profile_button.hide()
            self.logout_button.hide()

    def login_button_clicked(self):
        self.login_button.login_dialog.exec()
