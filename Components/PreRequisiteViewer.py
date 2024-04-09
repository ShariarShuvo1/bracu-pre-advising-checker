from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from typing import Dict, List

from Entity.Course import Course
from Stylesheet.ExamViewerStylesheet import *
from Stylesheet.ListViewerStylesheet import LIST_VIEWER_WIDGET_STYLE


class PreRequisiteViewer:
    def __init__(self, main):
        self.main = main
        self.course_labels: List[QLabel] = []
        self.pre_requisite_viewer_widget: QWidget = QWidget()
        self.pre_requisite_viewer_layout: QVBoxLayout = QVBoxLayout()
        self.pre_requisite_viewer_layout.setContentsMargins(2, 2, 0, 0)
        self.pre_requisite_viewer_layout.setSpacing(0)
        self.pre_requisite_viewer_widget.setLayout(
            self.pre_requisite_viewer_layout)
        self.pre_requisite_viewer_widget.setStyleSheet(
            LIST_VIEWER_WIDGET_STYLE)

        self.scroll_area: QScrollArea = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet(SCROLL_AREA_STYLE)
        self.scroll_area_widget: QWidget = QWidget()
        self.scroll_area_layout: QVBoxLayout = QVBoxLayout()
        self.scroll_area_widget.setLayout(self.scroll_area_layout)
        self.scroll_area_layout.setContentsMargins(2, 2, 2, 2)
        self.scroll_area_layout.setSpacing(2)
        self.scroll_area_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.title_label = QLabel("Pre Requisite")
        self.title_label.setStyleSheet(TITLE_LABEL_STYLE)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pre_requisite_viewer_layout.addWidget(self.title_label)

        self.pre_requisite_viewer_layout.addWidget(self.scroll_area)

    def set_course(self, course: Course):
        self.clear_course()
        self.title_label.setText(f"Pre Requisite for {course.course_code}")
        pre_req: Dict[str, List[str]] = self.main.pre_requisite_data
        if pre_req.get(course.course_code):
            if len(pre_req[course.course_code]) == 0:
                self.clear_course()
            else:
                for pre_req_course_code in pre_req[course.course_code]:
                    label = QLabel(pre_req_course_code)
                    label.setStyleSheet(COURSE_LABEL_STYLE)
                    label.setToolTip("Click to search")
                    label.setCursor(Qt.CursorShape.PointingHandCursor)
                    label.mousePressEvent = lambda _, pre_req_course=pre_req_course_code: (
                        self.course_clicked(pre_req_course))
                    self.course_labels.append(label)
                    self.scroll_area_layout.insertWidget(
                        self.scroll_area_layout.count() - 1, label)
        else:
            self.clear_course()

    def course_clicked(self, pre_req_course_code):
        self.main.left_list_viewer.search_bar.setText(
            f"c={pre_req_course_code}")

    def clear_course(self):
        self.title_label.setText("Pre Requisite")
        for course_label in self.course_labels:
            course_label.deleteLater()
        self.course_labels.clear()
