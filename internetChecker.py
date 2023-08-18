import requests
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMessageBox


def internetActive(url="https://www.google.com", timeout=10):
    try:
        requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False


def warningMessageBox(text_message="No Internet", title_message="No Internet"):
    msg = QMessageBox()
    msg.resize(250, 160)
    msg.setMinimumSize(QtCore.QSize(250, 160))
    msg.setBaseSize(QtCore.QSize(250, 160))
    msg.setText(text_message)
    msg.setWindowTitle(title_message)
    msg.setStandardButtons(QMessageBox.StandardButton.Close)
    if text_message != "No Internet":
        msg.setIcon(QMessageBox.Icon.Warning)
    else:
        msg.setIcon(QMessageBox.Icon.Critical)
    msg.exec()


def internet_checker():
    if not internetActive():
        warningMessageBox()
        return False
    if not internetActive("https://usis.bracu.ac.bd/academia/"):
        warningMessageBox("USIS server down!", "USIS down!")
        return False
    return True
