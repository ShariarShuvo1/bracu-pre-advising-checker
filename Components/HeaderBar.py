from PyQt6.QtWidgets import QWidget, QHBoxLayout

from Components.Toggler import Toggler
from Settings.SettingsData import get_setting
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

        self.header_bar_layout.addLayout(self.first_row_layout)

        self.booked_seat_toggle = Toggler("Booked Seat")
        self.booked_seat_toggle.set_tooltip("Enable to allow booked seat.")
        self.first_row_layout.addWidget(self.booked_seat_toggle.toggler_widget)

        self.lab_clash_toggle = Toggler("Lab Clash")
        self.lab_clash_toggle.set_tooltip("Enable to allow lab clashes.")
        self.lab_clash_toggle.set_checked(True)
        self.first_row_layout.addWidget(self.lab_clash_toggle.toggler_widget)

        self.theory_clash_toggle = Toggler("Theory Clash")
        self.theory_clash_toggle.set_tooltip(
            "Enable to allow theory clashes.")
        self.first_row_layout.addWidget(
            self.theory_clash_toggle.toggler_widget)

        self.same_course_toggle = Toggler("Same Course Clash")
        self.same_course_toggle.set_tooltip("Enable to allow same course.")
        self.first_row_layout.addWidget(self.same_course_toggle.toggler_widget)

        self.exam_day_toggle = Toggler("Exam Day Clash")
        self.exam_day_toggle.set_tooltip("Enable to allow exam day clashes.")
        self.exam_day_toggle.set_checked(True)
        self.first_row_layout.addWidget(self.exam_day_toggle.toggler_widget)

        self.exam_time_toggle = Toggler("Exam Time Clash")
        self.exam_time_toggle.set_tooltip(
            "Enable to allow exam time clashes.")
        self.first_row_layout.addWidget(self.exam_time_toggle.toggler_widget)

        self.pre_requisite_toggle = Toggler("Pre-requisite Clash")
        self.pre_requisite_toggle.set_tooltip(
            "Enable to allow pre-requisite clashes.")
        self.first_row_layout.addWidget(
            self.pre_requisite_toggle.toggler_widget)

        self.first_row_layout.addStretch()
        if not get_setting("IS_LOGGED_IN"):
            self.pre_requisite_toggle.toggler_widget.hide()

    def is_booked_seat_allowed(self) -> bool:
        return self.booked_seat_toggle.is_checked()

    def is_lab_clash_allowed(self) -> bool:
        return self.lab_clash_toggle.is_checked()

    def is_theory_clash_allowed(self) -> bool:
        return self.theory_clash_toggle.is_checked()

    def is_same_course_clash_allowed(self) -> bool:
        return self.same_course_toggle.is_checked()

    def is_exam_day_clash_allowed(self) -> bool:
        return self.exam_day_toggle.is_checked()

    def is_exam_time_clash_allowed(self) -> bool:
        return self.exam_time_toggle.is_checked()

    def is_pre_requisite_clash_allowed(self) -> bool:
        return self.pre_requisite_toggle.is_checked()
