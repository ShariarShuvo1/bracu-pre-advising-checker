from PyQt6.QtCore import QThread, pyqtSignal

from Functions.usis_login import check_internet_connection, check_usis_connection, login_to_usis


class LoginThread(QThread):
    status_update: pyqtSignal = pyqtSignal(str)

    def __init__(self, main, email: str, password: str):
        super().__init__()
        self.main = main
        self.email: str = email
        self.password: str = password

    def run(self):
        self.status_update.emit("Checking for internet connection...")
        if check_internet_connection(self.main.session):
            self.status_update.emit("Internet connection found")
        else:
            self.status_update.emit("No internet connection")
            return

        self.status_update.emit("Checking for USIS connection...")
        if check_usis_connection(self.main.session):
            self.status_update.emit("USIS connection found")
        else:
            self.status_update.emit("USIS connection failed")
            return

        self.status_update.emit("Logging in to USIS...")

        login_status = login_to_usis(
            self.main.session, self.email, self.password)

        if type(login_status) is str:
            self.status_update.emit(login_status)
        elif login_status:
            self.status_update.emit("Login successful")
        else:
            self.status_update.emit("Login failed. Invalid email or password")
