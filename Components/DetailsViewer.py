from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

from Entity.Course import Course
from Functions.prediction import predict_faculty
from Settings.SettingsData import prediction_data_contains
from Stylesheet.DetailsViewerStylesheet import *
from Stylesheet.ListViewerStylesheet import LIST_VIEWER_WIDGET_STYLE, SCROLL_AREA_STYLE


class DetailsViewer:
    def __init__(self, main):
        self.main = main
        self.course: Course | None = None
        self.details_viewer_widget: QWidget = QWidget()
        self.details_viewer_layout: QVBoxLayout = QVBoxLayout()
        self.details_viewer_layout.setContentsMargins(5, 0, 5, 0)
        self.details_viewer_layout.setSpacing(3)
        self.details_viewer_widget.setLayout(self.details_viewer_layout)
        self.details_viewer_widget.setFixedWidth(315)
        self.details_viewer_widget.setStyleSheet(LIST_VIEWER_WIDGET_STYLE)

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
        self.scroll_area_layout.setContentsMargins(2, 2, 2, 2)
        self.scroll_area_layout.setSpacing(2)
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.course_code_label = QLabel("")
        self.course_code_label.setStyleSheet(COURSE_CODE_LABEL_STYLE)
        self.course_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.course_code_label.hide()

        self.course_title_label = QLabel("")
        self.course_title_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.course_title_label.setWordWrap(True)
        self.course_title_label.hide()

        self.section_label = QLabel("")
        self.section_label.setStyleSheet(BOLD_LABEL_STYLE)
        self.section_label.hide()

        self.instructor_initial_label = QLabel("")
        self.instructor_initial_label.setStyleSheet(BOLD_LABEL_STYLE)
        self.instructor_initial_label.hide()

        self.prediction_label = QLabel("")
        self.prediction_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.prediction_label.hide()

        self.instructor_name_label = QLabel("")
        self.instructor_name_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.instructor_name_label.hide()
        self.instructor_name_label.setWordWrap(True)

        self.seats_remaining_label = QLabel("")
        self.seats_remaining_label.hide()

        self.total_seats_label = QLabel("")
        self.total_seats_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.total_seats_label.hide()

        self.seats_booked_label = QLabel("")
        self.seats_booked_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.seats_booked_label.hide()

        self.course_credit_label = QLabel("")
        self.course_credit_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.course_credit_label.hide()

        self.program_label = QLabel("")
        self.program_label.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.program_label.hide()

        self.faculty = QLabel("")
        self.faculty.setStyleSheet(NOT_BOLD_LABEL_STYLE)
        self.faculty.hide()

        self.class_day_1_label = QLabel("")
        self.class_day_1_label.setStyleSheet(CLASS_LABEL_STYLE)
        self.class_day_1_label.hide()

        self.class_day_1_time_label = QLabel("")
        self.class_day_1_time_label.setStyleSheet(CLASS_LABEL_STYLE)
        self.class_day_1_time_label.hide()
        self.class_day_1_time_label.setWordWrap(True)

        self.class_day_2_label = QLabel("")
        self.class_day_2_label.setStyleSheet(CLASS_LABEL_STYLE)
        self.class_day_2_label.hide()

        self.class_day_2_time_label = QLabel("")
        self.class_day_2_time_label.setStyleSheet(CLASS_LABEL_STYLE)
        self.class_day_2_time_label.hide()
        self.class_day_2_time_label.setWordWrap(True)

        self.lab_day_1_label = QLabel("")
        self.lab_day_1_label.setStyleSheet(LAB_LABEL_STYLE)
        self.lab_day_1_label.hide()

        self.lab_day_1_time_label = QLabel("")
        self.lab_day_1_time_label.setStyleSheet(LAB_LABEL_STYLE)
        self.lab_day_1_time_label.hide()
        self.lab_day_1_time_label.setWordWrap(True)

        self.lab_day_2_label = QLabel("")
        self.lab_day_2_label.setStyleSheet(LAB_LABEL_STYLE)
        self.lab_day_2_label.hide()

        self.lab_day_2_time_label = QLabel("")
        self.lab_day_2_time_label.setStyleSheet(LAB_LABEL_STYLE)
        self.lab_day_2_time_label.hide()
        self.lab_day_2_time_label.setWordWrap(True)

        self.exam_date_label = QLabel("")
        self.exam_date_label.setStyleSheet(EXAM_LABEL_STYLE)
        self.exam_date_label.hide()

        self.exam_time_label = QLabel("")
        self.exam_time_label.setStyleSheet(EXAM_LABEL_STYLE)
        self.exam_time_label.hide()
        self.exam_time_label.setWordWrap(True)

        self.scroll_area_layout.addWidget(self.course_code_label)
        self.scroll_area_layout.addWidget(self.course_title_label)
        self.scroll_area_layout.addWidget(self.section_label)
        self.scroll_area_layout.addWidget(self.instructor_initial_label)
        self.scroll_area_layout.addWidget(self.prediction_label)
        self.scroll_area_layout.addWidget(self.instructor_name_label)
        self.scroll_area_layout.addWidget(self.seats_remaining_label)
        self.scroll_area_layout.addWidget(self.total_seats_label)
        self.scroll_area_layout.addWidget(self.seats_booked_label)
        self.scroll_area_layout.addWidget(self.course_credit_label)
        self.scroll_area_layout.addWidget(self.program_label)
        self.scroll_area_layout.addWidget(self.faculty)

        self.scroll_area_layout.addWidget(self.class_day_1_label)
        self.scroll_area_layout.addWidget(self.class_day_1_time_label)
        self.scroll_area_layout.addWidget(self.class_day_2_label)
        self.scroll_area_layout.addWidget(self.class_day_2_time_label)
        self.scroll_area_layout.addWidget(self.lab_day_1_label)
        self.scroll_area_layout.addWidget(self.lab_day_1_time_label)
        self.scroll_area_layout.addWidget(self.lab_day_2_label)
        self.scroll_area_layout.addWidget(self.lab_day_2_time_label)
        self.scroll_area_layout.addWidget(self.exam_date_label)
        self.scroll_area_layout.addWidget(self.exam_time_label)

        self.details_viewer_layout.addWidget(self.scroll_area)
        self.scroll_area_layout.addStretch()

    def set_course(self, course: Course | None):
        if course is None:
            return
        self.course = course

        self.course_code_label.setText(course.course_code)
        if "closed" in course.section.lower():
            self.course_code_label.setStyleSheet(
                STRIKETHROUGH_COURSE_CODE_LABEL_STYLE)
        self.course_title_label.setText(f"Course Title: {course.course_title}")
        self.section_label.setText(f"Section: {course.section}")
        self.instructor_initial_label.setText(
            f"Faculty Initial: {course.instructor_initial}")

        if course.instructor_initial == "TBA" and prediction_data_contains():
            predict_faculty_dict = predict_faculty(
                course.course_code, course.section)
            prediction = "Prediction:"
            for key, value in predict_faculty_dict.items():
                prediction += f"\n{key}: {value:.2f}%"
            self.prediction_label.setText(prediction)
            self.prediction_label.show()
        else:
            self.prediction_label.hide()

        self.instructor_name_label.setText(
            f"Faculty Name: {course.instructor_name}")
        self.seats_remaining_label.setText(
            f"Seats Remaining: {course.seats_remaining}")
        if course.seats_remaining > 0:
            self.seats_remaining_label.setStyleSheet(BOLD_LABEL_SUCCESS_STYLE)
        else:
            self.seats_remaining_label.setStyleSheet(BOLD_LABEL_FAIL_STYLE)
        self.total_seats_label.setText(f"Total Seats: {course.total_seats}")
        self.seats_booked_label.setText(f"Seats Booked: {course.seats_booked}")
        self.course_credit_label.setText(f"Credit: {course.course_credit}")
        self.program_label.setText(f"Program: {course.program}")
        self.faculty.setText(f"Department: {course.faculty}")

        if course.schedule.class_day_1:
            self.class_day_1_label.setText(
                f"Class Day 1: {course.schedule.class_day_1}")
        if course.schedule.class_day_1_start_time:
            start_time_text = f"{course.schedule.class_day_1_start_time}"
            end_time_text = f" - {
                course.schedule.class_day_1_end_time}" if course.schedule.class_day_1_end_time else ""
            room_text = f" [Room: {
                course.schedule.class_day_1_room}]" if course.schedule.class_day_1_room else ""
            self.class_day_1_time_label.setText(f"Class Day 1 Time: {start_time_text}{
                                                end_time_text}{room_text}")

        if course.schedule.class_day_2:
            self.class_day_2_label.setText(
                f"Class Day 2: {course.schedule.class_day_2}")
        if course.schedule.class_day_2_start_time:
            start_time_text = f"{course.schedule.class_day_2_start_time}"
            end_time_text = f" - {
                course.schedule.class_day_2_end_time}" if course.schedule.class_day_2_end_time else ""
            room_text = f" [Room: {
                course.schedule.class_day_2_room}]" if course.schedule.class_day_2_room else ""
            self.class_day_2_time_label.setText(f"Class Day 2 Time: {start_time_text}{
                                                end_time_text}{room_text}")

        if course.schedule.lab_day_1:
            self.lab_day_1_label.setText(f"Lab 1: {course.schedule.lab_day_1}")

        if course.schedule.lab_day_1_start_time:
            start_time_text = f"{course.schedule.lab_day_1_start_time}"
            end_time_text = f" - {
                course.schedule.lab_day_1_end_time}" if course.schedule.lab_day_1_end_time else ""
            room_text = f" [Room: {
                course.schedule.lab_day_1_room}]" if course.schedule.lab_day_1_room else ""
            self.lab_day_1_time_label.setText(f"Lab 1 Time: {start_time_text}{
                                              end_time_text}{room_text}")

        if course.schedule.lab_day_2:
            self.lab_day_2_label.setText(f"Lab 2: {course.schedule.lab_day_2}")

        if course.schedule.lab_day_2_start_time:
            start_time_text = f"{course.schedule.lab_day_2_start_time}"
            end_time_text = f" - {
                course.schedule.lab_day_2_end_time}" if course.schedule.lab_day_2_end_time else ""
            room_text = f" [Room: {
                course.schedule.lab_day_2_room}]" if course.schedule.lab_day_2_room else ""
            self.lab_day_2_time_label.setText(f"Lab 2 Time: {start_time_text}{
                                              end_time_text}{room_text}")

        if course.schedule.exam_date:
            self.exam_date_label.setText(
                f"Exam Date: {course.schedule.exam_date}" +
                (f" ({course.schedule.exam_day})"
                 if course.schedule.exam_day else ""))

        if course.schedule.exam_start_time:
            start_time_text = f"{course.schedule.exam_start_time}"
            end_time_text = f" - {
                course.schedule.exam_end_time}" if course.schedule.exam_end_time else ""
            self.exam_time_label.setText(
                f"Exam Time: {start_time_text}{end_time_text}")

        self.course_code_label.show()
        self.course_title_label.show()
        self.section_label.show()
        self.instructor_initial_label.show()
        self.instructor_name_label.show()
        self.seats_remaining_label.show()
        self.total_seats_label.show()
        self.seats_booked_label.show()
        self.course_credit_label.show()
        self.program_label.show()
        self.faculty.show()
        if course.schedule.class_day_1:
            self.class_day_1_label.show()
        else:
            self.class_day_1_label.hide()
        if course.schedule.class_day_1_start_time:
            self.class_day_1_time_label.show()
        else:
            self.class_day_1_time_label.hide()
        if course.schedule.class_day_2:
            self.class_day_2_label.show()
        else:
            self.class_day_2_label.hide()
        if course.schedule.class_day_2_start_time:
            self.class_day_2_time_label.show()
        else:
            self.class_day_2_time_label.hide()
        if course.schedule.lab_day_1:
            self.lab_day_1_label.show()
        else:
            self.lab_day_1_label.hide()
        if course.schedule.lab_day_1_start_time:
            self.lab_day_1_time_label.show()
        else:
            self.lab_day_1_time_label.hide()
        if course.schedule.lab_day_2:
            self.lab_day_2_label.show()
        else:
            self.lab_day_2_label.hide()
        if course.schedule.lab_day_2_start_time:
            self.lab_day_2_time_label.show()
        else:
            self.lab_day_2_time_label.hide()
        if course.schedule.exam_date:
            self.exam_date_label.show()
        else:
            self.exam_date_label.hide()
        if course.schedule.exam_start_time:
            self.exam_time_label.show()
        else:
            self.exam_time_label.hide()
