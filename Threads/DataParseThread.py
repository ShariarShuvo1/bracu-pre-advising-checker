from PyQt6.QtCore import QThread, pyqtSignal
from typing import List

from Entity.Course import Course
from Functions.course_data_fetch import get_courses_guest, get_courses_user
from Functions.prediction import get_course_data
from Functions.usis_login import check_usis_connection, check_internet_connection
from Settings.SettingsData import get_setting, set_pre_requisite_data


class DataParseThread(QThread):
    status_update: pyqtSignal = pyqtSignal(str)
    data_found: pyqtSignal = pyqtSignal(list)

    def __init__(self, main):
        super().__init__()
        self.main = main

    def run(self):
        self.status_update.emit("Checking for internet connection...")
        if check_internet_connection(self.main.session):
            self.status_update.emit("Internet connection found")
        else:
            self.status_update.emit("No internet connection")
            self.data_found.emit([])
            return
        self.status_update.emit("Checking for USIS connection...")
        if check_usis_connection(self.main.session):
            self.status_update.emit("USIS connection found")
        else:
            self.status_update.emit("USIS connection failed")
            self.data_found.emit([])
            return
        data: List[Course] = []
        if get_setting("IS_LOGGED_IN_INFO_SAVED") or get_setting("IS_LOGGED_IN"):
            get_course_data(self.main, self.status_update)
            self.main.footer_bar.get_resource()
            data, pre_req = get_courses_user(self.main, self.status_update)
        else:
            data, pre_req = get_courses_guest(self.main, self.status_update)
        set_pre_requisite_data(pre_req)
        self.data_found.emit(data)
