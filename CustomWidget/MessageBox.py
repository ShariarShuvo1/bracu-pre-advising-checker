from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox


def message_dialog(message: str, title):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Icon.Warning)
    message_box.setText(message)
    message_box.setWindowTitle(title)
    message_box.setWindowIcon(QIcon("./Assets/logo.png"))
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()
