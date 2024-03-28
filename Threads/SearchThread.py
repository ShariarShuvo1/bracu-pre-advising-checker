from PyQt6.QtCore import QThread, pyqtSignal

from Components.CourseCard import CourseCard


class SearchThread(QThread):
    search_finished = pyqtSignal(bool, object)

    def __init__(self, card_list: list[CourseCard], search_text):
        super().__init__()
        self.card_list = card_list
        self.search_text = search_text

    def run(self):
        results = []
        for card in self.card_list:
            if (
                    self.search_text in card.course.course_code.lower() or
                    self.search_text in card.course.course_title.lower() or
                    self.search_text in card.course.instructor_initial.lower() or
                    self.search_text in card.course.instructor_name.lower() or
                    self.search_text == "free" and card.course.seats_remaining > 0 or
                    self.search_text == "full" and card.course.seats_remaining < 0 or
                    self.search_text == "closed" and "close" in card.course.section.lower() or
                    self.search_text in card.course.faculty.lower() or
                    self.search_text in card.course.program.lower() or
                    self.search_text in card.course.schedule.class_day_1.lower()
                    if card.course.schedule.class_day_1 else "" or
                    self.search_text in card.course.schedule.class_day_2.lower()
                    if card.course.schedule.class_day_2 else "" or
                    self.search_text in card.course.schedule.lab_day_1.lower()
                    if card.course.schedule.lab_day_1 else "" or
                    self.search_text in card.course.schedule.lab_day_2.lower()
                    if card.course.schedule.lab_day_2 else "" or
                    self.search_text in card.course.schedule.class_day_1_start_time.lower()
                    if card.course.schedule.class_day_1_start_time else "" or
                    self.search_text in card.course.schedule.class_day_2_start_time.lower()
                    if card.course.schedule.class_day_2_start_time else "" or
                    self.search_text in card.course.schedule.class_day_1_end_time.lower()
                    if card.course.schedule.class_day_1_end_time else "" or
                    self.search_text in card.course.schedule.class_day_2_end_time.lower()
                    if card.course.schedule.class_day_2_end_time else "" or
                    self.search_text in card.course.schedule.lab_day_1_start_time.lower()
                    if card.course.schedule.lab_day_1_start_time else "" or
                    self.search_text in card.course.schedule.lab_day_2_start_time.lower()
                    if card.course.schedule.lab_day_2_start_time else "" or
                    self.search_text in card.course.schedule.lab_day_1_end_time.lower()
                    if card.course.schedule.lab_day_1_end_time else "" or
                    self.search_text in card.course.schedule.lab_day_2_end_time.lower()
                    if card.course.schedule.lab_day_2_end_time else "" or
                    self.search_text in card.course.schedule.class_day_1_room.lower()
                    if card.course.schedule.class_day_1_room else "" or
                    self.search_text in card.course.schedule.class_day_2_room.lower()
                    if card.course.schedule.class_day_2_room else "" or
                    self.search_text in card.course.schedule.lab_day_1_room.lower()
                    if card.course.schedule.lab_day_1_room else "" or
                    self.search_text in card.course.schedule.lab_day_2_room.lower()
                    if card.course.schedule.lab_day_2_room else ""
            ):
                results.append((card, True))
            else:
                results.append((card, False))
        self.search_finished.emit(True, results)
