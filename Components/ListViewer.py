from PyQt6.QtCore import Qt, QMutexLocker, QMutex
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QScrollArea, QApplication

from Components.CourseCard import CourseCard
from Stylesheet.ListViewerStylesheet import *
from Threads.SearchThread import SearchThread


def process_search_results(success, results):
    if success:
        for card, result in results:
            if result:
                card.course_card_widget.show()
            else:
                card.course_card_widget.hide()


class ListViewer:
    def __init__(self, main):
        self.thread: SearchThread | None = None
        self.search_in_progress = False
        self.search_mutex = QMutex()
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
        self.search_bar.textChanged.connect(self.search)

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

    def search(self):
        search_text = self.search_bar.text().strip().lower()
        if len(search_text) >= 2 or len(search_text) == 0:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            locker = QMutexLocker(self.search_mutex)
            if self.search_in_progress:
                return

            self.search_in_progress = True
            self.thread = SearchThread(self.course_card_list, search_text)
            self.thread.search_finished.connect(process_search_results)
            self.thread.finished.connect(self.search_finished_handler)
            self.thread.start()

    def search_finished_handler(self):
        QApplication.restoreOverrideCursor()
        with QMutexLocker(self.search_mutex):
            self.search_in_progress = False

    def generate_course_cards(self):
        for card in self.course_card_list:
            card.course_card_widget.deleteLater()

        for course in self.main.courses:
            self.course_card_list.append(CourseCard(course))
            self.scroll_area_layout.insertWidget(
                self.scroll_area_layout.count() - 1, self.course_card_list[-1].course_card_widget)
