from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QMovie
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox, QPushButton, QHBoxLayout

from Entity.Course import Course
from Settings.SettingsData import set_setting, get_setting, course_data_contains, get_backup_course_data, \
    set_backup_course_data
from Stylesheet.LoginStatusDialogStylesheet import STATUS_LABEL_STYLE, STATUS_LABEL_ERROR_STYLE, \
    STATUS_LABEL_SUCCESS_STYLE, TRY_AGAIN_BUTTON_STYLE
from Stylesheet.ProfileDialogStylesheet import DIALOG_STYLE
from Threads.DataParseThread import DataParseThread


class DataLoadingDialog(QDialog):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.setWindowTitle("Getting USIS data")
        self.setFixedWidth(600)
        self.setFixedHeight(350)
        self.setWindowIcon(QIcon("./Assets/logo.png"))
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowType.WindowCloseButtonHint)
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)
        self.setStyleSheet(DIALOG_STYLE)

        self.loading_label: QLabel = QLabel()
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label: QLabel = QLabel()
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)

        self.try_again_button: QPushButton = QPushButton("Restart")
        self.try_again_button.setToolTip("Restart the data fetching process\n"
                                         "Sometimes the process may fail due to network issues or server problems")
        self.try_again_button.setMaximumWidth(200)
        self.try_again_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.try_again_button.clicked.connect(self.parse_begun)
        self.try_again_button.setStyleSheet(TRY_AGAIN_BUTTON_STYLE)
        self.try_again_button.setIcon(QIcon("./Assets/Icons/retry.png"))
        self.try_again_button.setIconSize(QSize(30, 30))

        self.load_previous_data_button: QPushButton = QPushButton(
            "Load Previous Data")
        self.load_previous_data_button.setToolTip("Load the data that was fetched previously\n"
                                                  "This data may be outdated or incomplete")
        self.load_previous_data_button.setMaximumWidth(220)
        self.load_previous_data_button.setCursor(
            Qt.CursorShape.PointingHandCursor)
        self.load_previous_data_button.clicked.connect(self.load_previous_data)
        self.load_previous_data_button.setStyleSheet(TRY_AGAIN_BUTTON_STYLE)
        self.load_previous_data_button.setIcon(
            QIcon("./Assets/Icons/load-previous.png"))
        self.load_previous_data_button.setIconSize(QSize(30, 30))

        self.main_layout.addWidget(self.loading_label)
        self.main_layout.addWidget(self.status_label)
        self.bottom_layout: QHBoxLayout = QHBoxLayout()
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.try_again_button)
        self.bottom_layout.addWidget(self.load_previous_data_button)
        self.bottom_layout.addStretch()
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.addSpacing(10)

        self.data_parse_thread: DataParseThread | None = None
        self.parse_begun()
        self.exec()

    def parse_begun(self):
        self.load_previous_data_button.hide()
        movie = QMovie("./Assets/Icons/loading.gif")
        movie.setScaledSize(QSize(100, 100))
        self.loading_label.setMovie(movie)
        movie.start()
        if self.data_parse_thread and self.data_parse_thread.isRunning():
            self.data_parse_thread.terminate()
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.data_parse_thread = DataParseThread(self.main)
        self.data_parse_thread.status_update.connect(
            self.data_parsing_thread_status_update)
        self.data_parse_thread.data_found.connect(self.data_found)
        self.data_parse_thread.start()

    def data_parsing_thread_status_update(self, status):
        self.status_label.setText(status)
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        if (status == "No internet connection" or
                status.startswith("USIS connection failed") or
                status.startswith("GitFront connection failed") or
                status.startswith("Error:")):
            self.status_label.setStyleSheet(STATUS_LABEL_ERROR_STYLE)
            msg_box = QMessageBox()
            msg_box.setWindowTitle(status)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setText(status)
            if status == "No internet connection":
                movie = QMovie("./Assets/GIF/no-internet.gif")
                self.loading_label.setMovie(movie)
                movie.start()
                msg_box.setInformativeText(
                    "Please check your internet connection and try again")
            elif status.startswith("USIS connection failed" or status.startswith("GitFront connection failed")):
                movie = QMovie("./Assets/GIF/usis-down.gif")
                self.loading_label.setMovie(movie)
                movie.start()
                msg_box.setInformativeText(
                    "USIS is down right now. Use offline mode or try again later")
            msg_box.setWindowIcon(QIcon("./Assets/logo.png"))
            msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
            msg_box.exec()

    def load_previous_data(self):
        if self.data_parse_thread:
            self.data_parse_thread.terminate()
        data: list[Course] = get_backup_course_data()
        self.main.data_loaded.emit(data)
        self.close()

    def data_found(self, data):
        if len(data) > 0:
            set_backup_course_data(data)
            self.main.data_loaded.emit(data)
            self.close()
        else:
            if course_data_contains():
                self.load_previous_data_button.show()
