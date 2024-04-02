from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from Stylesheet.CourseCardStylesheet import COURSE_CARD_STYLE, BOLD_LABEL_STYLE, NOT_BOLD_LABEL_STYLE


class HistoryCard:
    def __init__(self, semester, course_code, section, instructor):
        self.course_code = course_code
        self.section = section
        self.instructor = instructor
        self.semester = semester
        self.history_card_widget: QWidget = QWidget()
        self.history_card_layout: QHBoxLayout = QHBoxLayout()
        self.history_card_layout.setContentsMargins(0, 0, 0, 0)
        self.history_card_layout.setSpacing(0)
        self.history_card_widget.setLayout(self.history_card_layout)
        self.history_card_widget.setStyleSheet(COURSE_CARD_STYLE)
        self.history_card_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.history_card_widget.setCursor(Qt.CursorShape.PointingHandCursor)

        self.course_code_label: QLabel = QLabel(course_code)
        self.course_code_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.course_code_label.setFixedWidth(100)
        self.course_code_label.setToolTip(course_code)
        self.course_code_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.section_label: QLabel = QLabel(section)
        self.section_label.setFixedWidth(100)
        self.section_label.setWordWrap(True)
        self.section_label.setStyleSheet(BOLD_LABEL_STYLE)
        self.section_label.setToolTip(section)
        self.section_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.instructor_initial_label: QLabel = QLabel(instructor)
        self.instructor_initial_label.setFixedWidth(100)
        self.instructor_initial_label.setToolTip(instructor)
        if instructor == "TBA":
            self.instructor_initial_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        else:
            self.instructor_initial_label.setStyleSheet(BOLD_LABEL_STYLE)
        self.instructor_initial_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.semester_label: QLabel = QLabel(semester)
        self.semester_label.setFixedWidth(100)
        self.semester_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.semester_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.history_card_layout.addWidget(self.course_code_label)
        self.history_card_layout.addWidget(self.section_label)
        self.history_card_layout.addWidget(self.instructor_initial_label)
        self.history_card_layout.addWidget(self.semester_label)
