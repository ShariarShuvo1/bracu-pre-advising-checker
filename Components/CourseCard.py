from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from Constants.day_data import get_short_day_name
from Entity.Course import Course
from Stylesheet.CourseCardStylesheet import *


def get_date_tooltip(course: Course) -> str:
    tooltip: str = ""
    if course.schedule.class_day_1:
        tooltip += (f"Class Day 1: {course.schedule.class_day_1} "
                    f"({course.schedule.class_day_1_start_time} - "
                    f"{course.schedule.class_day_1_end_time}) "
                    f"[{course.schedule.class_day_1_room}]")

    if course.schedule.class_day_2:
        tooltip += (f"\nClass Day 2: {course.schedule.class_day_2} "
                    f"({course.schedule.class_day_2_start_time} - "
                    f"{course.schedule.class_day_2_end_time}) "
                    f"[{course.schedule.class_day_2_room}]")

    if course.schedule.lab_day_1:
        if course.schedule.class_day_1:
            tooltip += (f"\n\nLab Day 1: {course.schedule.lab_day_1} "
                        f"({course.schedule.lab_day_1_start_time} - "
                        f"{course.schedule.lab_day_1_end_time}) "
                        f"[{course.schedule.lab_day_1_room}]")
        else:
            tooltip += (f"Lab Day 1: {course.schedule.lab_day_1} "
                        f"({course.schedule.lab_day_1_start_time} - "
                        f"{course.schedule.lab_day_1_end_time}) "
                        f"[{course.schedule.lab_day_1_room}]")

    if course.schedule.lab_day_2:
        tooltip += (f"\nLab Day 2: {course.schedule.lab_day_2} "
                    f"({course.schedule.lab_day_2_start_time} - "
                    f"{course.schedule.lab_day_2_end_time}) "
                    f"[{course.schedule.lab_day_2_room}]")

    if course.schedule.exam_day:
        tooltip += f"\n\nExam Day: {course.schedule.exam_day}"
        tooltip += (f"\nExam Date: {course.schedule.exam_date} "
                    f"({course.schedule.exam_start_time} - "
                    f"{course.schedule.exam_end_time})")

    return tooltip


class CourseCard:
    def __init__(self, course: Course):
        self.course: Course = course
        self.course_card_widget: QWidget = QWidget()
        self.course_card_layout: QHBoxLayout = QHBoxLayout()
        self.course_card_layout.setContentsMargins(0, 0, 0, 0)
        self.course_card_layout.setSpacing(0)
        self.course_card_widget.setLayout(self.course_card_layout)
        self.course_card_widget.setStyleSheet(COURSE_CARD_STYLE)
        self.course_card_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.course_card_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.course_card_widget.focusInEvent = self.focus_in_event
        self.course_card_widget.focusOutEvent = self.focus_out_event

        section = ""
        for char in self.course.section:
            if char.isdigit() and len(section) <= 2:
                section += char

        self.section_label: QLabel = QLabel(section)
        self.section_label.setFixedWidth(30)
        self.section_label.setWordWrap(True)
        self.section_label.setStyleSheet(BOLD_LABEL_STYLE)
        self.section_label.setToolTip(self.course.section)
        self.section_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.course_code_label: QLabel = QLabel(self.course.course_code)
        self.course_code_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.course_code_label.setFixedWidth(70)
        self.course_code_label.setToolTip(self.course.course_title)
        if "close" in self.course.course_code.lower():
            self.course_code_label.setStyleSheet(STRICKEN_LABEL_STYLE)
        self.course_code_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.instructor_initial_label: QLabel = QLabel(
            self.course.instructor_initial)
        self.instructor_initial_label.setFixedWidth(50)
        self.instructor_initial_label.setToolTip(self.course.instructor_name)
        if self.course.instructor_initial == "TBA":
            self.instructor_initial_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        else:
            self.instructor_initial_label.setStyleSheet(BOLD_LABEL_STYLE)
        self.instructor_initial_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.available_seats_label: QLabel = QLabel(
            str(self.course.seats_remaining))
        self.available_seats_label.setFixedWidth(30)
        self.available_seats_label.setToolTip(f"Available seats: {self.course.seats_remaining}\n"
                                              f"Total seats: {
                                                  self.course.total_seats}\n"
                                              f"Booked seats: {self.course.seats_booked}")
        if self.course.seats_remaining > 0:
            self.available_seats_label.setStyleSheet(SUCCESS_LABEL_STYLE)
        else:
            self.available_seats_label.setStyleSheet(ERROR_LABEL_STYLE)
        self.available_seats_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        date = ""
        if self.course.schedule.class_day_1:
            date += get_short_day_name(self.course.schedule.class_day_1)
            if self.course.schedule.class_day_2:
                if (get_short_day_name(self.course.schedule.class_day_2) !=
                        get_short_day_name(self.course.schedule.class_day_1)):
                    date += "," + \
                        get_short_day_name(self.course.schedule.class_day_2)
            date += "(" + self.course.schedule.class_day_1_start_time[:5] + ")"

        if not self.course.schedule.class_day_1 and self.course.schedule.lab_day_1:
            date += get_short_day_name(self.course.schedule.lab_day_1)
            if self.course.schedule.lab_day_2:
                if (get_short_day_name(self.course.schedule.lab_day_2) !=
                        get_short_day_name(self.course.schedule.lab_day_1)):
                    date += "," + \
                        get_short_day_name(self.course.schedule.lab_day_2)
            date += "(" + self.course.schedule.lab_day_1_start_time[:5] + ")"

        self.date_label: QLabel = QLabel(date)
        self.date_label.setFixedWidth(100)
        self.date_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.date_label.setToolTip(get_date_tooltip(self.course))
        self.date_label.setWordWrap(True)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.course_card_layout.addWidget(self.section_label)
        self.course_card_layout.addWidget(self.course_code_label)
        self.course_card_layout.addWidget(self.instructor_initial_label)
        self.course_card_layout.addWidget(self.available_seats_label)
        self.course_card_layout.addWidget(self.date_label)
        self.course_card_layout.addStretch()

    def focus_in_event(self, event):
        self.course_card_widget.setStyleSheet(COURSE_CARD_CLICKED_STYLE)
        event.accept()

    def focus_out_event(self, event):
        self.course_card_widget.setStyleSheet(COURSE_CARD_STYLE)
        event.accept()
