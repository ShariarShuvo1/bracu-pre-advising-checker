import sys

import requests
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSplitter, QPushButton

from Components.DetailsViewer import DetailsViewer
from Components.ExamViewer import ExamViewer
from Components.FooterBar import FooterBar
from Components.ListViewer import ListViewer
from Components.PreRequisiteViewer import PreRequisiteViewer
from Components.ScheduleTable import ScheduleTable
from Dialogs.DataLoadingDialog import DataLoadingDialog
from Dialogs.LoginStatusDialog import LoginStatusDialog
from Entity.Course import Course
from Entity.Profile import Profile
from Settings.SettingsData import get_setting
from Stylesheet.MainWindowStylesheet import *
from Components.LoginBar import LoginBar


class MainWindow(QMainWindow):
    is_already_logged_in: pyqtSignal = pyqtSignal()
    card_clicked: pyqtSignal = pyqtSignal(list)
    card_clicked_to_remove: pyqtSignal = pyqtSignal(list)

    def already_logged_in(self, later_call: bool = False):
        if get_setting("IS_LOGGED_IN_INFO_SAVED") and not later_call:
            LoginStatusDialog(self)
        DataLoadingDialog(self)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BRACU Pre Advising Checker")
        self.setMinimumSize(1280, 650)
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
        self.working_session_id: str = "627123"
        self.courses: list[Course] = []
        self.pre_requisite_data: dict[str, list[str]] = {}
        self.selected_course: Course | None = None
        self.selected_course_to_remove: Course | None = None

        self.login_bar: LoginBar = LoginBar(self)

        self.footer_bar: FooterBar = FooterBar(self)

        self.left_list_viewer: ListViewer = ListViewer(self)
        self.right_list_viewer: ListViewer = ListViewer(self, True)

        self.details_viewer: DetailsViewer = DetailsViewer(self)

        self.exam_viewer: ExamViewer = ExamViewer(self)
        self.pre_requisite_viewer: PreRequisiteViewer = PreRequisiteViewer(
            self)

        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet(ADD_BUTTON_STYLE)
        self.add_button.clicked.connect(
            lambda _: self.right_list_viewer.add_course(self.selected_course))
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.setMinimumHeight(50)
        self.add_button.setMaximumWidth(70)

        self.remove_button = QPushButton("Remove")
        self.remove_button.setStyleSheet(REMOVE_BUTTON_STYLE)
        self.remove_button.clicked.connect(
            lambda _: self.right_list_viewer.remove_course(self.selected_course_to_remove))
        self.remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_button.setMinimumHeight(50)
        self.remove_button.setMaximumWidth(70)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet(CLEAR_BUTTON_STYLE)
        self.clear_button.clicked.connect(self.right_list_viewer.clear_courses)
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_button.setMinimumHeight(50)
        self.clear_button.setMaximumWidth(70)

        self.middle_layout = QVBoxLayout()
        self.middle_layout.setContentsMargins(0, 0, 0, 0)
        self.middle_layout.setSpacing(3)
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.add_button)
        self.middle_layout.addSpacing(10)
        self.middle_layout.addWidget(self.remove_button)
        self.middle_layout.addWidget(self.clear_button)
        self.middle_layout.addStretch()

        self.list_viewer_layout: QHBoxLayout = QHBoxLayout()
        self.list_viewer_layout.addWidget(
            self.left_list_viewer.list_viewer_widget)
        self.list_viewer_layout.addLayout(self.middle_layout)

        self.splitter: QSplitter = QSplitter()
        self.splitter.addWidget(self.right_list_viewer.list_viewer_widget)
        self.splitter.addWidget(self.details_viewer.details_viewer_widget)
        self.splitter.setSizes([200, 500])
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setLineWidth(0)
        self.splitter.setMidLineWidth(0)
        self.splitter.setHandleWidth(1)
        self.splitter.setContentsMargins(0, 0, 0, 0)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setStyleSheet(SPLITTER_STYLE)

        self.schedule_extra_splitter: QSplitter = QSplitter()
        self.schedule_extra_splitter.setSizes([600, 100])
        self.schedule_extra_splitter.setChildrenCollapsible(False)
        self.schedule_extra_splitter.setLineWidth(0)
        self.schedule_extra_splitter.setMidLineWidth(0)
        self.schedule_extra_splitter.setHandleWidth(1)
        self.schedule_extra_splitter.setContentsMargins(0, 0, 0, 0)
        self.schedule_extra_splitter.setOrientation(Qt.Orientation.Vertical)
        self.schedule_extra_splitter.setStyleSheet(SPLITTER_STYLE)

        self.schedule_table: ScheduleTable = ScheduleTable(self)

        self.right_panel_layout: QVBoxLayout = QVBoxLayout()
        self.right_panel_layout.addWidget(self.splitter)
        self.right_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.right_panel_layout.setSpacing(0)
        self.list_viewer_layout.addLayout(self.right_panel_layout)

        self.schedule_layout = QVBoxLayout()
        self.schedule_layout.setContentsMargins(0, 0, 0, 0)
        self.schedule_layout.setSpacing(0)

        self.extra_info_layout = QHBoxLayout()
        self.extra_info_layout.setContentsMargins(0, 0, 0, 0)
        self.extra_info_layout.setSpacing(0)

        self.extra_info_layout.addWidget(self.exam_viewer.exam_viewer_widget)
        self.extra_info_layout.addWidget(
            self.pre_requisite_viewer.pre_requisite_viewer_widget)
        self.extra_info_widget = QWidget()
        self.extra_info_widget.setLayout(self.extra_info_layout)

        self.schedule_extra_splitter.addWidget(self.schedule_table.table)
        self.schedule_extra_splitter.addWidget(self.extra_info_widget)

        self.schedule_layout.addWidget(self.schedule_extra_splitter)
        self.list_viewer_layout.addLayout(self.schedule_layout)

        self.main_layout.addWidget(self.login_bar.login_bar_widget)
        self.main_layout.addLayout(self.list_viewer_layout)
        self.main_layout.addWidget(self.footer_bar.footer_bar_widget)
        self.is_already_logged_in.connect(self.already_logged_in)
        self.card_clicked.connect(self.card_selected)
        self.card_clicked_to_remove.connect(self.card_to_remove)

    def card_selected(self, lst: list):
        course = lst[0]
        self.selected_course = course
        self.details_viewer.set_course(course)
        self.pre_requisite_viewer.set_course(course)

    def card_to_remove(self, lst: list):
        course = lst[0]
        self.selected_course_to_remove = course
        self.details_viewer.set_course(course)
        # self.pre_requisite_viewer.add_course(course)

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
    # window.showMaximized()
    window.show()
    window.is_already_logged_in.emit()
    sys.exit(app.exec())
