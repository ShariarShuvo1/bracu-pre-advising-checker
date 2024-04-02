from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QScrollArea, QWidget, QPushButton, QHBoxLayout

from Components.HistoryCard import HistoryCard
from Settings.SettingsData import prediction_data_contains, get_prediction_data
from Stylesheet.HistoryDialogStylesheet import *
from Stylesheet.ListViewerStylesheet import SEARCH_BAR_STYLE, SCROLL_AREA_STYLE


class HistoryDialog(QDialog):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.course_list: list = []
        self.setWindowTitle(f"View Data of Previous Semesters")
        self.setFixedHeight(600)
        self.setFixedWidth(500)
        self.setWindowIcon(QIcon("./Assets/logo.png"))
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)
        self.setStyleSheet(DIALOG_STYLE)

        self.search_bar: QLineEdit = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.setStyleSheet(SEARCH_BAR_STYLE)
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setToolTip(
            f"Accepted Filter: 'or', 'and', 's', 'c', 'i'")

        self.search_button: QPushButton = QPushButton("Search")
        self.search_button.setStyleSheet(SEARCH_BUTTON_STYLE)
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_button.setFixedHeight(34)
        self.search_button.clicked.connect(self.search)

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

        self.search_layout: QHBoxLayout = QHBoxLayout()
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_button)
        self.main_layout.addLayout(self.search_layout)
        self.main_layout.addWidget(self.scroll_area)
        self.body_generated = False

    def search(self):
        search_text = self.search_bar.text().strip().lower()
        is_regex = True
        is_or = False
        is_and = False
        terms = {}
        text = search_text.replace(" ", "").lower()
        text = text.replace("or", "|")
        text = text.replace("and", "&")
        commands = ["s", "c", "i"]
        if "=" in text:
            if "&" in text and "|" in text:
                is_regex = False
            if is_regex:
                if "&" in text:
                    is_and = True
                    terms_list = text.split("&")
                elif "|" in text:
                    terms_list = text.split("|")
                    is_or = True
                else:
                    is_and = True
                    terms_list = [text]
                for term in terms_list:
                    term = term.strip("=")
                    term = "=".join(part for part in term.split("=") if part)
                    if "=" in term:
                        name_value_list = term.split("=")
                        name, value = name_value_list[0], name_value_list[1]
                        if name != "" and value != "" and name in commands:
                            if name in ("ts", "sb", "sr") and value.isdigit():
                                value = int(value)
                            elif name in ("ts", "sb", "sr") and not value.isdigit():
                                continue
                            elif name == "s":
                                try:
                                    value = int(value)
                                except ValueError:
                                    continue
                            terms[name] = value
        else:
            is_regex = False
        if len(terms) == 0:
            is_regex = False
        for course in self.course_list:
            if not is_regex:
                if search_text in course.course_code.lower() or search_text in course.section.lower() or search_text in course.instructor.lower() or search_text in course.semester.lower():
                    course.history_card_widget.show()
                else:
                    course.history_card_widget.hide()
            else:
                if is_and:
                    section = course.section.lower()
                    if (
                            (str(terms["s"]).lower() == section.lower() if terms.get("s") else True) and
                            (terms["c"].lower() == course.course_code.lower() if terms.get("c") else True) and
                            (terms["i"].lower() == course.instructor.lower()
                             if terms.get("i") else True)
                    ):
                        course.history_card_widget.show()
                    else:
                        course.history_card_widget.hide()
                elif is_or:
                    section = course.section.lower()
                    if (
                            (str(terms["s"]).lower() == section.lower() if terms.get("s") else False) or
                            (terms["c"].lower() == course.course_code.lower() if terms.get("c") else False) or
                            (terms["i"].lower() == course.instructor.lower()
                             if terms.get("i") else False)
                    ):
                        course.history_card_widget.show()
                    else:
                        course.history_card_widget.hide()

    def generate_course_list(self):
        if not self.body_generated:
            self.body_generated = True
        if prediction_data_contains():
            prediction_list = get_prediction_data()
            for k, v in prediction_list.items():
                semester_name, semester_year, _ = k.split("_")
                semester = f"{semester_name} {semester_year}"
                for key, value in v.items():
                    course_code, section = key
                    instructor = value
                    history_card = HistoryCard(
                        semester, course_code, section, instructor)
                    history_card.history_card_widget.hide()
                    self.course_list.append(history_card)
                    self.scroll_area_layout.insertWidget(
                        self.scroll_area_layout.count() - 1, history_card.history_card_widget)
