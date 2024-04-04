from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from CustomWidget.ToggleButton import ToggleButton


class Toggler:
    def __init__(self, text: str):
        self.toggler_widget: QWidget = QWidget()
        self.toggler_layout: QHBoxLayout = QHBoxLayout()
        self.toggler_layout.setContentsMargins(2, 2, 2, 2)
        self.toggler_widget.setLayout(self.toggler_layout)

        self.toggle_text = QLabel(text)
        self.toggle_text.setStyleSheet("font-size: 18px;")
        self.toggler_layout.addWidget(self.toggle_text)
        self.toggle_text.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignHCenter)

        self.toggle_button = ToggleButton()
        self.toggle_button.setChecked(False)
        self.toggle_button.setFixedWidth(50)
        self.toggler_layout.addWidget(self.toggle_button)
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_text(self, text: str):
        self.toggle_text.setText(text)

    def set_tooltip(self, tooltip: str):
        self.toggle_button.setToolTip(tooltip)

    def set_checked(self, checked: bool):
        self.toggle_button.setChecked(checked)

    def set_unchecked(self):
        self.toggle_button.setChecked(False)

    def toggle(self):
        self.toggle_button.toggle()

    def is_checked(self) -> bool:
        return self.toggle_button.isChecked()
