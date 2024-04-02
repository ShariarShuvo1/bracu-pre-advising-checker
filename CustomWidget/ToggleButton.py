from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt


class ToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setChecked(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.isChecked() and self.isEnabled():
            bg_color = QColor("#9a00bd")
            circle_color = QColor("#FFFFFF")
        elif not self.isEnabled():
            bg_color = QColor("#7d7d7d")
            circle_color = QColor("#9e9e9e")
        elif self.underMouse():
            bg_color = QColor("#e15cff")
            circle_color = QColor("#FFFFFF")
        else:
            bg_color = QColor("#BDBDBD")
            circle_color = QColor("#FFFFFF")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(self.rect(), 13, 13)

        circle_radius = min(self.rect().width(), self.rect().height()) / 2 - 4
        if self.isChecked():
            circle_x = int(self.rect().width() - circle_radius * 2 - 4)
        else:
            circle_x = 4
        circle_y = int((self.rect().height() - circle_radius * 2) / 2)
        painter.setBrush(QBrush(circle_color))
        painter.drawEllipse(circle_x, circle_y, int(
            circle_radius * 2), int(circle_radius * 2))

        painter.end()
