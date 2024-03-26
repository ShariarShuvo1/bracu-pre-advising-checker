from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox


def security_info():
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon("./Assets/logo.png"))
    msg_box.setWindowTitle("Security Information")
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setText("This Application don't store your email and password\n"
                    "This Application use your email and password to login to USIS only\n"
                    "Checking Remember Me will store your email and password in your device\n"
                    "No data will be sent to any server\n"
                    "This Application is open source\n"
                    "You can check the source code in the GitHub Repository\n"
                    "However, if multiple users use the same device\n"
                    "it is recommended not to check Remember Me\n")
    msg_box.exec()
