from PyQt6.QtCore import QThread, pyqtSignal

from Entity.Profile import Profile
from Functions.get_profile_info import get_profile_info


class ProfileInfoThread(QThread):

    def __init__(self, main):
        super().__init__()
        self.main = main

    def run(self):
        profile: Profile = get_profile_info(self.main)
        self.main.footer_bar.profile_info_found(profile)
