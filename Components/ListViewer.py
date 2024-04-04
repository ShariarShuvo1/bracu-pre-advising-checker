from PyQt6.QtCore import Qt, QMutexLocker, QMutex
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QScrollArea

from Components.CourseCard import CourseCard
from CustomWidget.MessageBox import message_dialog
from Entity.Course import Course
from Entity.ProfileCourse import ProfileCourse
from Settings.SettingsData import get_setting
from Stylesheet.ListViewerStylesheet import *
from Threads.SearchThread import SearchThread
from datetime import datetime


def process_search_results(success, results):
    if success:
        for card, result in results:
            if result:
                card.course_card_widget.show()
            else:
                card.course_card_widget.hide()


class ListViewer:
    def __init__(self, main, right=False):
        self.thread: SearchThread | None = None
        self.search_in_progress = False
        self.search_mutex = QMutex()
        self.main = main
        self.right = right
        self.list_viewer_widget: QWidget = QWidget()
        self.list_viewer_layout: QVBoxLayout = QVBoxLayout()
        self.list_viewer_layout.setContentsMargins(5, 0, 5, 0)
        self.list_viewer_layout.setSpacing(3)
        self.list_viewer_widget.setLayout(self.list_viewer_layout)
        self.list_viewer_widget.setFixedWidth(315)
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
            # QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            locker = QMutexLocker(self.search_mutex)
            if self.search_in_progress:
                return

            self.search_in_progress = True
            self.thread = SearchThread(self.course_card_list, search_text)
            self.thread.search_finished.connect(process_search_results)
            self.thread.finished.connect(self.search_finished_handler)
            self.thread.start()

    def search_finished_handler(self):
        with QMutexLocker(self.search_mutex):
            self.search_in_progress = False

    def generate_course_cards(self):
        for card in self.course_card_list:
            card.course_card_widget.deleteLater()
        self.course_card_list.clear()

        for course in self.main.courses:
            self.course_card_list.append(CourseCard(course, self.main))
            self.scroll_area_layout.insertWidget(
                self.scroll_area_layout.count() - 1, self.course_card_list[-1].course_card_widget)

    def is_duplicate(self, course: Course) -> bool:
        for card in self.course_card_list:
            if card.course == course:
                return True
        return False

    def seat_limit_reached(self, course: Course) -> bool:
        is_booked_seat_allowed = self.main.header_bar.is_booked_seat_allowed()
        if is_booked_seat_allowed:
            return False
        else:
            if course.seats_remaining <= 0:
                message_dialog(
                    f"Seat limit reached for {course.course_code}[{course.section}]", "Seat Limit Reached")
                return True
        return False

    def is_same_course(self, course: Course) -> bool:
        is_theory_clash_allowed = self.main.header_bar.is_same_course_clash_allowed()
        if is_theory_clash_allowed:
            return False
        else:
            for card in self.course_card_list:
                if card.course.course_code == course.course_code:
                    message_dialog(
                        f"Clash between {course.course_code}[{course.section}] and {
                            card.course.course_code} [{card.course.section}]\n"
                        f"Clash Reason: Same Course", "Same Course Clash")
                    return True
        return False

    def is_lab_clash(self, course: Course) -> bool:
        is_lab_clash_allowed = self.main.header_bar.is_lab_clash_allowed()
        if is_lab_clash_allowed:
            return False
        else:
            for card in self.course_card_list:
                matched = False
                if card.course.schedule.lab_day_1 and course.schedule.lab_day_1:
                    if card.course.schedule.lab_day_1 == course.schedule.lab_day_1 and datetime.strptime(
                            card.course.schedule.lab_day_1_start_time, "%I:%M %p") <= datetime.strptime(
                            course.schedule.lab_day_1_end_time, "%I:%M %p") and datetime.strptime(
                            card.course.schedule.lab_day_1_end_time, "%I:%M %p") >= datetime.strptime(
                            course.schedule.lab_day_1_start_time, "%I:%M %p"):
                        matched = True
                if matched:
                    message_dialog(
                        f"Clash between {course.course_code}[{course.section}] and {
                            card.course.course_code} [{card.course.section}]\n"
                        f"Clash Reason: Lab Clash", "Lab Clash")
                    return True
                if card.course.schedule.lab_day_2 and course.schedule.lab_day_2:
                    if card.course.schedule.lab_day_2 == course.schedule.lab_day_2 and datetime.strptime(
                            card.course.schedule.lab_day_2_start_time, "%I:%M %p") <= datetime.strptime(
                            course.schedule.lab_day_2_end_time, "%I:%M %p") and datetime.strptime(
                            card.course.schedule.lab_day_2_end_time, "%I:%M %p") >= datetime.strptime(
                            course.schedule.lab_day_2_start_time, "%I:%M %p"):
                        matched = True
                if matched:
                    message_dialog(
                        f"Clash between {course.course_code}[{course.section}] and {
                            card.course.course_code} [{card.course.section}]\n"
                        f"Clash Reason: Lab Clash", "Lab Clash")
                    return True
        return False

    def is_theory_clash(self, course: Course) -> bool:
        is_theory_clash_allowed = self.main.header_bar.is_theory_clash_allowed()
        if is_theory_clash_allowed:
            return False
        else:
            for card in self.course_card_list:
                matched = False
                if card.course.schedule.class_day_1 and course.schedule.class_day_1:
                    if card.course.schedule.class_day_1 == course.schedule.class_day_1 and datetime.strptime(
                            card.course.schedule.class_day_1_start_time, "%I:%M %p") <= datetime.strptime(
                            course.schedule.class_day_1_end_time, "%I:%M %p") and datetime.strptime(
                            card.course.schedule.class_day_1_end_time, "%I:%M %p") >= datetime.strptime(
                            course.schedule.class_day_1_start_time, "%I:%M %p"):
                        matched = True
                if matched:
                    message_dialog(
                        f"Clash between {course.course_code}[{course.section}] and {
                            card.course.course_code} [{card.course.section}]\n"
                        f"Clash Reason: Theory Clash", "Theory Clash")
                    return True
                if card.course.schedule.class_day_2 and course.schedule.class_day_2:
                    if card.course.schedule.class_day_2 == course.schedule.class_day_2 and datetime.strptime(
                            card.course.schedule.class_day_2_start_time, "%I:%M %p") <= datetime.strptime(
                            course.schedule.class_day_2_end_time, "%I:%M %p") and datetime.strptime(
                            card.course.schedule.class_day_2_end_time, "%I:%M %p") >= datetime.strptime(
                            course.schedule.class_day_2_start_time, "%I:%M %p"):
                        matched = True
                if matched:
                    message_dialog(
                        f"Clash between {course.course_code}[{course.section}] and {
                            card.course.course_code} [{card.course.section}]\n"
                        f"Clash Reason: Theory Clash", "Theory Clash")
                    return True
        return False

    def is_exam_day_clash(self, course: Course) -> bool:
        is_exam_day_clash_allowed = self.main.header_bar.is_exam_day_clash_allowed()
        if is_exam_day_clash_allowed:
            return False
        else:
            for card in self.course_card_list:
                if card.course.schedule.exam_date == course.schedule.exam_date:
                    message_dialog(
                        f"Clash between {course.course_code}[{course.section}] and {
                            card.course.course_code} [{card.course.section}]\n"
                        f"Clash Reason: Exam Day Clash", "Exam Day Clash")
                    return True
        return False

    def is_exam_time_clash(self, course: Course) -> bool:
        is_exam_time_clash_allowed = self.main.header_bar.is_exam_time_clash_allowed()
        if is_exam_time_clash_allowed:
            return False
        else:
            for card in self.course_card_list:
                matched = False
                if card.course.schedule.exam_date == course.schedule.exam_date:
                    if datetime.strptime(card.course.schedule.exam_start_time, "%I:%M %p") <= datetime.strptime(
                            course.schedule.exam_end_time, "%I:%M %p") and datetime.strptime(
                            card.course.schedule.exam_end_time, "%I:%M %p") >= datetime.strptime(
                            course.schedule.exam_start_time, "%I:%M %p"):
                        matched = True
                if matched:
                    message_dialog(
                        f"Clash between {course.course_code}[{course.section}] and {
                            card.course.course_code} [{card.course.section}]\n"
                        f"Clash Reason: Exam Time Clash", "Exam Time Clash")
                    return True
        return False

    def is_prerequisite_clash(self, course: Course) -> bool:
        is_prerequisite_clash_allowed = self.main.header_bar.is_pre_requisite_clash_allowed()
        if is_prerequisite_clash_allowed:
            return False
        else:
            if get_setting("IS_LOGGED_IN") and self.main.pre_requisite_data and self.main.profile:
                course_code = course.course_code
                print(course_code)
                pre_req: dict[str, list[str]] = self.main.pre_requisite_data
                pre_req_for_course = pre_req.get(course_code)
                if pre_req_for_course:
                    completed_courses: list[ProfileCourse] = self.main.profile.courses
                    clashed = []
                    for pre_req_course in pre_req_for_course:
                        if pre_req_course not in [course.course_code for course in completed_courses]:
                            clashed.append(pre_req_course)
                            continue
                        clash = False
                        for completed_course in completed_courses:
                            if pre_req_course == completed_course.course_code:
                                if completed_course.grade_point <= 0 and "Pending" not in completed_course.grade:
                                    clash = True
                                    break
                        if clash:
                            clashed.append(pre_req_course)
                    if len(clashed) > 0:
                        message_dialog(
                            f"You have not completed the following pre-requisite courses for {
                                course_code}:\n"
                            f"{', '.join(clashed)}", "Pre-requisite Clash")
                        return True
        return False

    def validator(self, course: Course) -> bool:
        return (
            not self.is_duplicate(course) and
            not self.seat_limit_reached(course) and
            not self.is_same_course(course) and
            not self.is_lab_clash(course) and
            not self.is_theory_clash(course) and
            not self.is_exam_day_clash(course) and
            not self.is_exam_time_clash(course) and
            not self.is_prerequisite_clash(course)
        )

    def add_course(self, course: Course | None):
        if course:
            if self.validator(course):
                if self.right:
                    self.course_card_list.append(
                        CourseCard(course, self.main, True))
                    self.main.schedule_table.add_course(course)
                    self.main.exam_viewer.add_course(course)
                else:
                    self.course_card_list.append(CourseCard(course, self.main))
                self.scroll_area_layout.insertWidget(
                    self.scroll_area_layout.count() - 1, self.course_card_list[-1].course_card_widget)

    def remove_course(self, course: Course | None):
        if course:
            for card in self.course_card_list:
                if card.course == course:
                    card.course_card_widget.deleteLater()
                    self.course_card_list.remove(card)
                    if self.right:
                        self.main.schedule_table.remove_course(course)
                        self.main.exam_viewer.remove_course(course)
                    break

    def clear_courses(self):
        for card in self.course_card_list:
            card.course_card_widget.deleteLater()
            if self.right:
                self.main.schedule_table.remove_course(card.course)
                self.main.exam_viewer.remove_course(card.course)
        self.course_card_list.clear()
        self.search_bar.clear()
        self.search()
