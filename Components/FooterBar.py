from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QCursor
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QPushButton, QLabel, QApplication

from CustomWidget.LoginPushButton import LoginPushButton
from Dialogs.AboutMeDialog import AboutMeDialog
from Dialogs.HistoryDialog import HistoryDialog
from Dialogs.ProfileDialog import ProfileDialog
from Dialogs.UserManualDialog import UserManualDialog
from Entity.Profile import Profile
from Functions.logout import logout
from Settings.SettingsData import get_setting, current_semester_name_contains, get_current_semester_name, \
    next_semester_name_contains, get_next_semester_name
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

        self.user_manual_button: QPushButton = QPushButton()
        self.user_manual_button.setIcon(
            QIcon("./Assets/Icons/user-manual.png"))
        self.user_manual_button.setIconSize(QSize(40, 40))
        self.user_manual_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.user_manual_button.setToolTip("View the user manual")
        self.user_manual_button.setMaximumHeight(40)
        self.user_manual_button.enterEvent = self.user_manual_on_hover_enter
        self.user_manual_button.leaveEvent = self.user_manual_on_hover_leave
        self.user_manual_button.mousePressEvent = self.user_manual_mouse_press_vent
        self.user_manual_button.mouseReleaseEvent = self.user_manual_on_hover_enter

        self.about_me_button: QPushButton = QPushButton()
        self.about_me_button.setIcon(QIcon("./Assets/Icons/about-me.png"))
        self.about_me_button.setIconSize(QSize(34, 34))
        self.about_me_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.about_me_button.setToolTip("Learn about the developer")
        self.about_me_button.setMaximumHeight(40)
        self.about_me_button.enterEvent = self.about_me_on_hover_enter
        self.about_me_button.leaveEvent = self.about_me_on_hover_leave
        self.about_me_button.mousePressEvent = self.about_me_mouse_press_vent
        self.about_me_button.mouseReleaseEvent = self.about_me_on_hover_enter

        self.history_button: QPushButton = QPushButton("History")
        self.history_button.setIcon(QIcon("./Assets/Icons/history.png"))
        self.history_button.setIconSize(QSize(28, 28))
        self.history_button.setStyleSheet(HISTORY_BUTTON_STYLE)
        self.history_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.history_button.setToolTip("View your history")
        self.history_button.setMaximumHeight(40)
        self.history_button.clicked.connect(self.history_button_clicked)

        self.current_semester_label: QLabel = QLabel()
        self.current_semester_label.setStyleSheet(CURRENT_SEMESTER_LABEL_STYLE)
        self.current_semester_label.setMaximumHeight(40)
        if current_semester_name_contains():
            name, year = get_current_semester_name()
            self.current_semester_label.setText(
                f"Showing data for: {name} {year}")
        else:
            self.current_semester_label.hide()
            self.history_button.hide()
        self.next_semester_label: QLabel = QLabel()
        self.next_semester_label.setStyleSheet(CURRENT_SEMESTER_LABEL_STYLE)
        self.next_semester_label.setMaximumHeight(40)
        if next_semester_name_contains():
            name, year = get_next_semester_name()
            self.next_semester_label.setText(
                f"Current semester: {name} {year}")
        else:
            self.next_semester_label.hide()

        self.footer_bar_layout.addWidget(self.login_button)
        self.footer_bar_layout.addWidget(self.profile_button)
        self.footer_bar_layout.addWidget(self.logout_button)
        self.footer_bar_layout.addStretch()
        self.footer_bar_layout.addWidget(self.about_me_button)
        self.footer_bar_layout.addWidget(self.user_manual_button)
        self.footer_bar_layout.addWidget(self.history_button)
        self.footer_bar_layout.addWidget(self.current_semester_label)
        self.footer_bar_layout.addWidget(self.next_semester_label)
        self.profile_info_thread = None
        self.is_logged_in()
        self.history_dialog = HistoryDialog(self.main)
        self.user_manual = UserManualDialog(self.main)
        self.about_me = AboutMeDialog(self.main)

    def about_me_mouse_press_vent(self, event):
        self.about_me_button.setIcon(
            QIcon("./Assets/Icons/about-me-clicked.png"))

    def about_me_on_hover_enter(self, event):
        self.about_me_button.setIcon(
            QIcon("./Assets/Icons/about-me-hover.png"))
        if event.type() == 3:
            self.about_me.exec()

    def about_me_on_hover_leave(self, event):
        self.about_me_button.setIcon(
            QIcon("./Assets/Icons/about-me.png"))

    def user_manual_mouse_press_vent(self, event):
        self.user_manual_button.setIcon(
            QIcon("./Assets/Icons/user-manual-clicked.png"))

    def user_manual_on_hover_enter(self, event):
        self.user_manual_button.setIcon(
            QIcon("./Assets/Icons/user-manual-hover.png"))
        if event.type() == 3:
            self.user_manual.exec()

    def user_manual_on_hover_leave(self, event):
        self.user_manual_button.setIcon(
            QIcon("./Assets/Icons/user-manual.png"))

    def history_button_clicked(self):
        if not self.history_dialog.body_generated:
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
            self.history_dialog.generate_course_list()
            QApplication.restoreOverrideCursor()
        self.history_dialog.exec()

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
