from PyQt6.QtCore import QThread, pyqtSignal

from Entity.Profile import Profile
from Functions.get_profile_info import get_profile_info


class ProfileInfoThread(QThread):
    info_found: pyqtSignal = pyqtSignal(Profile)

    def __init__(self, main):
        super().__init__()
        self.main = main

    def run(self):
        profile: Profile = get_profile_info(self.main)
        self.info_found.emit(profile)
