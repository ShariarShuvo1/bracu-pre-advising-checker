from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from Entity.ProfileCourse import ProfileCourse
from Stylesheet.YourCourseCardStylesheet import *


class YourCourseCard:
    def __init__(self, course: ProfileCourse):
        self.course: ProfileCourse = course
        self.your_courses_card_widget: QWidget = QWidget()
        self.your_courses_card_layout: QHBoxLayout = QHBoxLayout()
        self.your_courses_card_layout.setContentsMargins(0, 0, 0, 0)
        self.your_courses_card_layout.setSpacing(10)
        self.your_courses_card_widget.setLayout(self.your_courses_card_layout)
        if "F" in self.course.grade:
            self.your_courses_card_widget.setStyleSheet(YOUR_COURSE_CARD_FAIL_STYLE)
        elif "Pending" in self.course.grade:
            self.your_courses_card_widget.setStyleSheet(YOUR_COURSE_CARD_PENDING_STYLE)
        else:
            self.your_courses_card_widget.setStyleSheet(YOUR_COURSE_CARD_STYLE)

        self.course_code: QLabel = QLabel(self.course.course_code)
        self.course_code.setStyleSheet(COURSE_CODE_STYLE)
        self.course_code.setFixedWidth(120)

        self.course_name: QLabel = QLabel(self.course.course_name)
        self.course_name.setStyleSheet(COURSE_NAME_STYLE)
        self.course_name.setWordWrap(True)

        self.course_credit: QLabel = QLabel(str(self.course.course_credit))
        self.course_credit.setStyleSheet(COURSE_NAME_STYLE)
        self.course_credit.setFixedWidth(120)
        self.course_credit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.credit_earned: QLabel = QLabel(str(self.course.credit_earned))
        self.credit_earned.setStyleSheet(COURSE_NAME_STYLE)
        self.credit_earned.setFixedWidth(120)
        self.credit_earned.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grade: QLabel = QLabel(self.course.grade)
        self.grade.setStyleSheet(COURSE_NAME_STYLE)
        self.grade.setFixedWidth(120)
        self.grade.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grade_point: QLabel = QLabel(str(self.course.grade_point))
        self.grade_point.setStyleSheet(COURSE_NAME_STYLE)
        self.grade_point.setFixedWidth(120)
        self.grade_point.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.your_courses_card_layout.addWidget(self.course_code)
        self.your_courses_card_layout.addWidget(self.course_name)
        self.your_courses_card_layout.addStretch()
        self.your_courses_card_layout.addWidget(self.course_credit)
        self.your_courses_card_layout.addWidget(self.credit_earned)
        self.your_courses_card_layout.addWidget(self.grade)
        self.your_courses_card_layout.addWidget(self.grade_point)
