from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout

from Components.YourCourses import YourCourses
from Entity.Profile import Profile
from Stylesheet.ProfileDialogStylesheet import *


class ProfileDialog(QDialog):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.profile: Profile = main.profile
        self.setWindowTitle(f"{self.profile.name}'s Profile")
        self.setMaximumHeight(600)
        self.setMinimumWidth(900)
        self.setWindowIcon(QIcon("./Assets/logo.png"))
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)
        self.setStyleSheet(DIALOG_STYLE)

        self.picture_label: QLabel = QLabel()
        pixmap = QPixmap()
        pixmap.loadFromData(self.profile.picture.content)
        pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.picture_label.setPixmap(pixmap)
        self.picture_label.setFixedSize(100, 100)

        self.name_label: QLabel = QLabel(self.profile.name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.name_label.setStyleSheet(NAME_LABEL_STYLE)

        self.id_label: QLabel = QLabel(self.profile.student_id)
        self.id_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.id_label.setStyleSheet(ID_LABEL_STYLE)

        self.department_label: QLabel = QLabel(self.profile.program)
        self.department_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.department_label.setStyleSheet(DEPARTMENT_LABEL_STYLE)

        self.your_courses = YourCourses(self.main)

        self.top_row: QHBoxLayout = QHBoxLayout()
        self.top_row.setContentsMargins(0, 0, 0, 0)
        self.top_row.setSpacing(0)

        self.right_column: QVBoxLayout = QVBoxLayout()
        self.right_column.setContentsMargins(10, 0, 0, 0)
        self.right_column.setSpacing(0)

        self.right_column.addWidget(self.name_label)
        self.right_column.addWidget(self.id_label)
        self.right_column.addWidget(self.department_label)
        self.right_column.addStretch()

        self.top_row.addWidget(self.picture_label)
        self.top_row.addLayout(self.right_column)
        self.top_row.addStretch()

        self.main_layout.addLayout(self.top_row)
        self.main_layout.addWidget(self.your_courses.your_courses_widget)
        self.main_layout.addStretch()
