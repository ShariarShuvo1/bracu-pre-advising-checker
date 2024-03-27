from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QScrollArea

from Components.CourseCard import CourseCard
from Stylesheet.ListViewerStylesheet import *


class ListViewer:
    def __init__(self, main):
        self.main = main
        self.list_viewer_widget: QWidget = QWidget()
        self.list_viewer_layout: QVBoxLayout = QVBoxLayout()
        self.list_viewer_layout.setContentsMargins(5, 0, 0, 0)
        self.list_viewer_layout.setSpacing(3)
        self.list_viewer_widget.setLayout(self.list_viewer_layout)
        self.list_viewer_widget.setFixedWidth(315)
        self.list_viewer_widget.setMinimumHeight(600)
        self.list_viewer_widget.setStyleSheet(LIST_VIEWER_WIDGET_STYLE)

        self.course_card_list: list[CourseCard] = []

        self.search_bar: QLineEdit = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.setStyleSheet(SEARCH_BAR_STYLE)
        self.search_bar.setClearButtonEnabled(True)

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
        self.scroll_area_layout.addStretch()
        self.scroll_area_layout.setContentsMargins(2, 2, 2, 2)
        self.scroll_area_layout.setSpacing(2)
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.list_viewer_layout.addWidget(self.search_bar)
        self.list_viewer_layout.addWidget(self.scroll_area)

    def generate_course_cards(self):
        for course in self.main.courses:
            self.course_card_list.append(CourseCard(course))
            self.scroll_area_layout.insertWidget(
                self.scroll_area_layout.count()-1, self.course_card_list[-1].course_card_widget)
