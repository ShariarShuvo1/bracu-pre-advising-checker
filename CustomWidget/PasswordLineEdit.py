from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout

from Stylesheet.LoginDialogStylesheet import TOGGLE_BUTTON_STYLE


class PasswordLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.toggle_button = QPushButton()
        self.toggle_button.setToolTip("Show")
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.toggle_button.setIcon(QIcon("./Assets/Icons/show.png"))
        self.toggle_button.setIconSize(QSize(20, 20))
        self.toggle_button.setMaximumHeight(60)
        self.toggle_button.setMaximumWidth(60)
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.setStyleSheet(TOGGLE_BUTTON_STYLE)
        self.toggle_button.toggled.connect(self.toggle_visibility)

        self.layout = QHBoxLayout()
        self.layout.addStretch()
        self.layout.addWidget(self.toggle_button)
        self.setLayout(self.layout)

    def hide_text(self):
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.toggle_button.setIcon(QIcon("./Assets/Icons/show.png"))
        self.toggle_button.setToolTip("Show")

    def show_text(self):
        self.setEchoMode(QLineEdit.EchoMode.Normal)
        self.toggle_button.setIcon(QIcon("./Assets/Icons/hide.png"))
        self.toggle_button.setToolTip("Hide")

    def toggle_visibility(self):
        if self.toggle_button.isChecked():
            self.hide_text()
        else:
            self.show_text()
