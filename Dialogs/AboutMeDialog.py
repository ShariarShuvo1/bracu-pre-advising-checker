import webbrowser

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from Stylesheet.ProfileDialogStylesheet import DIALOG_STYLE


def open_url(url: str):
    webbrowser.open(url)


class AboutMeDialog(QDialog):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.setWindowTitle(f"About the Developer")
        self.setWindowIcon(QIcon("./Assets/logo.png"))
        # set not resizable
        self.setFixedSize(500, 150)
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)
        self.setStyleSheet(DIALOG_STYLE)

        self.title_label = QLabel("Hello there!")
        self.title_label.setStyleSheet("font-size: 40px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.name_label = QLabel("I am Shariar Islam Shuvo")
        self.name_label.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.name_label)

        self.main_layout.addSpacing(20)

        self.row = QHBoxLayout()
        self.main_layout.addLayout(self.row)
        self.row.setContentsMargins(0, 0, 0, 0)
        self.row.setSpacing(10)

        self.github_button = QPushButton("GitHub")
        self.github_button.setToolTip("View the source code on GitHub")
        self.github_button.setIcon(QIcon("./Assets/Icons/github.png"))
        self.github_button.setIconSize(QSize(40, 40))
        self.github_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.github_button.clicked.connect(lambda: open_url(
            "https://github.com/ShariarShuvo1/bracu-pre-advising-checker"))
        self.github_button.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.row.addWidget(self.github_button)

        self.facebook_button = QPushButton("Facebook")
        self.facebook_button.setToolTip("Connect with me on Facebook")
        self.facebook_button.setIcon(QIcon("./Assets/Icons/facebook.png"))
        self.facebook_button.setIconSize(QSize(40, 40))
        self.facebook_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.facebook_button.clicked.connect(lambda: open_url(
            "https://www.facebook.com/ShariarShuvo01/"))
        self.facebook_button.setStyleSheet(
            "font-size: 16px; font-weight: bold;")
        self.row.addWidget(self.facebook_button)

        self.linkedin_button = QPushButton("LinkedIn")
        self.linkedin_button.setToolTip("Connect with me on LinkedIn")
        self.linkedin_button.setIcon(QIcon("./Assets/Icons/linkedin.png"))
        self.linkedin_button.setIconSize(QSize(40, 40))
        self.linkedin_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.linkedin_button.clicked.connect(lambda: open_url(
            "https://www.linkedin.com/in/shariarshuvo1/"))
        self.linkedin_button.setStyleSheet(
            "font-size: 16px; font-weight: bold;")
        self.row.addWidget(self.linkedin_button)

        self.main_layout.addStretch()
