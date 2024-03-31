from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel

from Entity.Course import Course
from Functions.get_date_tooltip import get_date_tooltip
from Stylesheet.ExamViewerStylesheet import *
from Stylesheet.ListViewerStylesheet import LIST_VIEWER_WIDGET_STYLE

from datetime import datetime


class ExamViewer:
    def __init__(self, main):
        self.main = main
        self.course_labels: list[tuple[Course, QLabel]] = []
        self.exam_viewer_widget: QWidget = QWidget()
        self.exam_viewer_layout: QVBoxLayout = QVBoxLayout()
        self.exam_viewer_layout.setContentsMargins(0, 2, 0, 0)
        self.exam_viewer_layout.setSpacing(0)
        self.exam_viewer_widget.setLayout(self.exam_viewer_layout)
        self.exam_viewer_widget.setMinimumWidth(330)
        self.exam_viewer_widget.setMaximumHeight(350)
        self.exam_viewer_widget.setStyleSheet(LIST_VIEWER_WIDGET_STYLE)

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
        self.scroll_area_layout.setContentsMargins(2, 2, 2, 2)
        self.scroll_area_layout.setSpacing(2)
        self.scroll_area_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.title_label = QLabel("Exam Dates")
        self.title_label.setStyleSheet(TITLE_LABEL_STYLE)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.exam_viewer_layout.addWidget(self.title_label)

        self.exam_viewer_layout.addWidget(self.scroll_area)

    def duplicate_check(self) -> None:
        for course in self.course_labels:
            course[1].setStyleSheet(COURSE_LABEL_STYLE)
        for idx, course in enumerate(self.course_labels):
            course_1 = course[0]
            label_1 = course[1]
            for i in range(len(self.course_labels)):
                if i == idx:
                    continue
                course_2 = self.course_labels[i][0]
                label_2 = self.course_labels[i][1]
                if course_1.schedule.exam_date == course_2.schedule.exam_date:
                    if "#fc8d8d" and "#fa7a7a" not in label_2.styleSheet():
                        label_2.setStyleSheet(
                            DUPLICATE_DATE_COURSE_LABEL_STYLE)
                    if "#fc8d8d" and "#fa7a7a" not in label_1.styleSheet():
                        label_1.setStyleSheet(
                            DUPLICATE_DATE_COURSE_LABEL_STYLE)
                    if (course_1.schedule.exam_start_time and course_1.schedule.exam_end_time and
                            course_2.schedule.exam_start_time and course_2.schedule.exam_end_time):
                        if (datetime.strptime(course_1.schedule.exam_start_time, "%I:%M %p") <
                                datetime.strptime(course_2.schedule.exam_end_time, "%I:%M %p") and
                                datetime.strptime(course_1.schedule.exam_end_time, "%I:%M %p") >
                                datetime.strptime(course_2.schedule.exam_start_time, "%I:%M %p")):
                            label_1.setStyleSheet(
                                DUPLICATE_TIME_COURSE_LABEL_STYLE)
                            label_2.setStyleSheet(
                                DUPLICATE_TIME_COURSE_LABEL_STYLE)

    def add_course(self, course: Course):
        if course.schedule.exam_date and course.schedule.exam_day:
            label_text = (f"{course.course_code} [{course.section}] - {course.schedule.exam_date} "
                          f"({course.schedule.exam_day if 'No' not in course.schedule.exam_day else 'N/A'})")
            label = QLabel(label_text)
            label.setStyleSheet(COURSE_LABEL_STYLE)
            label.setToolTip(get_date_tooltip(course))
            label.setFixedHeight(30)
            label.mousePressEvent = lambda _: self.main.card_clicked.emit([
                                                                          course])
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.course_labels.append((course, label))
            self.scroll_area_layout.insertWidget(
                self.scroll_area_layout.count() - 1, label)
            self.duplicate_check()

    def remove_course(self, course: Course):
        for course_label in self.course_labels:
            if course_label[0] == course:
                course_label[1].deleteLater()
                self.course_labels.remove(course_label)
                break
        self.duplicate_check()
