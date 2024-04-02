from PyQt6.QtWidgets import QWidget, QHBoxLayout

from Components.Toggler import Toggler
from CustomWidget.ToggleButton import ToggleButton
from Stylesheet.HeaderBarStylesheet import *


class HeaderBar:
    def __init__(self, main=None):
        self.main = main
        self.header_bar_widget: QWidget = QWidget()
        self.header_bar_layout: QHBoxLayout = QHBoxLayout()
        self.header_bar_layout.setContentsMargins(2, 2, 2, 2)
        self.header_bar_widget.setLayout(self.header_bar_layout)
        self.header_bar_widget.setStyleSheet(HEADER_BAR_STYLE)
        self.header_bar_widget.setMaximumHeight(50)

        self.first_row_layout: QHBoxLayout = QHBoxLayout()
        self.second_row_layout: QHBoxLayout = QHBoxLayout()

        self.header_bar_layout.addLayout(self.first_row_layout)
        self.header_bar_layout.addLayout(self.second_row_layout)

        self.lab_clash_toggle = Toggler("Lab Clash")
        self.lab_clash_toggle.set_tooltip("Enable to disable lab clashes.")
        self.first_row_layout.addWidget(self.lab_clash_toggle.toggler_widget)

        self.theory_clash_toggle = Toggler("Theory Clash")
        self.theory_clash_toggle.set_tooltip(
            "Enable to disable theory clashes.")
        self.theory_clash_toggle.set_checked(True)
        self.first_row_layout.addWidget(
            self.theory_clash_toggle.toggler_widget)

        self.same_course_toggle = Toggler("Same Course Clash")
        self.same_course_toggle.set_tooltip("Enable to disable same course.")
        self.same_course_toggle.set_checked(True)
        self.first_row_layout.addWidget(self.same_course_toggle.toggler_widget)

        self.exam_day_toggle = Toggler("Exam Day Clash")
        self.exam_day_toggle.set_tooltip("Enable to disable exam day clashes.")
        self.first_row_layout.addWidget(self.exam_day_toggle.toggler_widget)

        self.exam_time_toggle = Toggler("Exam Time Clash")
        self.exam_time_toggle.set_tooltip(
            "Enable to disable exam time clashes.")
        self.exam_time_toggle.set_checked(True)
        self.first_row_layout.addWidget(self.exam_time_toggle.toggler_widget)

        self.pre_requisite_toggle = Toggler("Pre-requisite Clash")
        self.pre_requisite_toggle.set_tooltip(
            "Enable to disable pre-requisite clashes.")
        self.pre_requisite_toggle.set_checked(True)
        self.first_row_layout.addWidget(
            self.pre_requisite_toggle.toggler_widget)

        self.first_row_layout.addStretch()
