from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QScrollArea, QHBoxLayout
from typing import List

from Components.YourCourseCard import YourCourseCard
from Entity.Profile import Profile
from Stylesheet.YourCourseCardStylesheet import COURSE_NAME_STYLE, COURSE_NAME_SMALL_STYLE
from Stylesheet.YourCoursesStylesheet import *


class YourCourses:
    def __init__(self, main=None):
        self.main = main
        self.profile: Profile = main.profile
        self.your_courses_widget: QWidget = QWidget()
        self.your_courses_layout: QVBoxLayout = QVBoxLayout()
        self.your_courses_layout.setContentsMargins(0, 0, 0, 0)
        self.your_courses_layout.setSpacing(1)
        self.your_courses_widget.setLayout(self.your_courses_layout)

        self.course_card: List[YourCourseCard] = []

        self.title_label: QLabel = QLabel("Your Courses")
        self.title_label.setStyleSheet(TITLE_LABEL_STYLE)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.course_search_input: QLineEdit = QLineEdit()
        self.course_search_input.setPlaceholderText("Search your courses")
        self.course_search_input.setStyleSheet(COURSE_SEARCH_INPUT_STYLE)
        self.course_search_input.setMaximumHeight(40)
        self.course_search_input.textChanged.connect(self.search_course)

        self.scroll_area: QScrollArea = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(SCROLL_AREA_STYLE)

        self.scroll_area_widget: QWidget = QWidget()
        self.scroll_area_layout: QVBoxLayout = QVBoxLayout()
        self.scroll_area_widget.setLayout(self.scroll_area_layout)

        self.scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area_layout.setSpacing(2)

        self.course_code: QLabel = QLabel("Course Code")
        self.course_code.setStyleSheet(COURSE_NAME_STYLE)
        self.course_code.setFixedWidth(120)

        self.course_name: QLabel = QLabel("Course Name")
        self.course_name.setStyleSheet(COURSE_NAME_STYLE)
        self.course_name.setWordWrap(True)

        self.course_credit: QLabel = QLabel("Course Credit")
        self.course_credit.setStyleSheet(COURSE_NAME_STYLE)
        self.course_credit.setFixedWidth(120)
        self.course_credit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.credit_earned: QLabel = QLabel("Credit Earned")
        self.credit_earned.setStyleSheet(COURSE_NAME_STYLE)
        self.credit_earned.setFixedWidth(120)
        self.credit_earned.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grade: QLabel = QLabel("Grade Name")
        self.grade.setStyleSheet(COURSE_NAME_STYLE)
        self.grade.setFixedWidth(120)
        self.grade.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grade_point: QLabel = QLabel("Grade Point")
        self.grade_point.setStyleSheet(COURSE_NAME_STYLE)
        self.grade_point.setFixedWidth(120)
        self.grade_point.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.total_credit_earned_label: QLabel = QLabel(
            f"Total Credit Earned: {str(self.profile.total_credit())}")
        self.total_credit_earned_label.setStyleSheet(COURSE_NAME_SMALL_STYLE)

        self.total_grade_point_label: QLabel = QLabel(
            f"CGPA: {self.profile.total_grade_point()}")
        self.total_grade_point_label.setStyleSheet(COURSE_NAME_SMALL_STYLE)

        self.top_bar: QHBoxLayout = QHBoxLayout()
        self.top_bar.setContentsMargins(0, 0, 0, 0)
        self.top_bar.setSpacing(10)

        self.top_bar.addWidget(self.course_code)
        self.top_bar.addWidget(self.course_name)
        self.top_bar.addStretch()
        self.top_bar.addWidget(self.course_credit)
        self.top_bar.addWidget(self.credit_earned)
        self.top_bar.addWidget(self.grade)
        self.top_bar.addWidget(self.grade_point)

        for course in self.profile.courses:
            course_card = YourCourseCard(course)
            self.course_card.append(course_card)
            self.scroll_area_layout.insertWidget(
                0, course_card.your_course_card_widget)
        self.scroll_area_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_area_widget)

        self.your_courses_layout.addWidget(self.title_label)
        self.your_courses_layout.addWidget(self.course_search_input)
        self.your_courses_layout.addLayout(self.top_bar)
        self.your_courses_layout.addWidget(self.scroll_area)

        self.bottom_bar: QHBoxLayout = QHBoxLayout()
        self.bottom_bar.setContentsMargins(0, 0, 0, 0)
        self.bottom_bar.setSpacing(10)

        self.bottom_bar.addWidget(self.total_credit_earned_label)
        self.bottom_bar.addWidget(self.total_grade_point_label)
        self.bottom_bar.addStretch()
        self.your_courses_layout.addLayout(self.bottom_bar)

    def search_course(self):
        for course in self.course_card:
            course.your_course_card_widget.hide()
            if (self.course_search_input.text().lower() in course.course.course_code.lower() or
                    self.course_search_input.text().lower() in course.course.course_name.lower() or
                    self.course_search_input.text().lower() in course.course.grade.lower() or
                    self.course_search_input.text().lower() in str(course.course.course_credit) or
                    self.course_search_input.text().lower() in str(course.course.credit_earned) or
                    self.course_search_input.text().lower() in str(course.course.grade_point)):
                course.your_course_card_widget.show()
