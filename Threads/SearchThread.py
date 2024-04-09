from datetime import datetime

from PyQt6.QtCore import QThread, pyqtSignal
from typing import List

from Components.CourseCard import CourseCard


class SearchThread(QThread):
    search_finished = pyqtSignal(bool, object)

    def __init__(self, card_list: List[CourseCard], search_text):
        super().__init__()
        self.card_list = card_list
        self.search_text = search_text

    def run(self):
        is_regex = True
        is_or = False
        is_and = False
        terms = {}
        text = self.search_text.replace(" ", "").lower()
        text = text.replace("and", "&")
        text = text.replace("or", "|")
        commands = ["s", "c", "i", "p", "f", "in", "ct", "ts", "sb", "sr", "e", "ed", "es", "ee",
                    "c1", "c2", "l1", "l2", "c1s", "c2s", "c1e", "c2e", "l1s", "l2s", "l1e", "l2e",
                    "c1sr", "c1er", "c2sr", "c2er", "l1sr", "l1er", "l2sr", "l2er"]
        time_commands = ["es", "ee", "c1s", "c2s", "c1e", "c2e", "l1s", "l2s", "l1e", "l2e", "c1sr",
                         "c1er", "c2sr", "c2er", "l1sr", "l1er", "l2sr", "l2er"]

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
                            elif name in time_commands:
                                try:
                                    value = value[:-2] + " " + value[-2:]
                                    x = datetime.strptime(value, "%I:%M %p")
                                except ValueError:
                                    continue
                            terms[name] = value
        else:
            is_regex = False
        if len(terms) == 0:
            is_regex = False
        results = []
        for card in self.card_list:
            if not is_regex:
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
            else:
                if is_and:
                    section = card.course.section.lower()
                    sec = ""
                    for s in section:
                        if s.isdigit():
                            sec += s
                    section = int(sec)
                    if (
                            (terms["s"] == section if terms.get("s") else True) and
                            (terms["c"] in card.course.course_code.lower() if terms.get("c") else True) and
                            (terms["i"] in card.course.instructor_initial.lower() if terms.get("i") else True) and
                            (terms["p"] in card.course.program.lower() if terms.get("p") else True) and
                            ((terms["f"] in card.course.faculty.lower() if card.course.faculty else False) if terms.get("f") else True) and
                            (terms["in"] in card.course.instructor_name.replace(' ', "").lower() if terms.get("in") else True) and
                            (terms["ct"] in card.course.course_title.replace(' ', "").lower() if terms.get("ct") else True) and
                            (terms["ts"] <= card.course.total_seats if terms.get("ts") else True) and
                            (terms["sb"] <= card.course.seats_remaining if terms.get("sb") else True) and
                            (terms["sr"] <= card.course.seats_remaining if terms.get("sr") else True) and
                            ((terms["e"] in card.course.schedule.exam_date.lower() if card.course.schedule.exam_date else "") if terms.get("e") else True) and
                            ((terms["ed"] in card.course.schedule.exam_day.replace(' ', "").lower() if card.course.schedule.exam_day else "") if terms.get("ed") else True) and
                            ((datetime.strptime(card.course.schedule.exam_start_time, "%I:%M %p") >= datetime.strptime(terms.get("es"), "%I:%M %p") if card.course.schedule.exam_start_time else False) if terms.get("es") else True) and
                            ((datetime.strptime(card.course.schedule.exam_end_time, "%I:%M %p") <= datetime.strptime(terms.get("ee"), "%I:%M %p") if card.course.schedule.exam_end_time else False) if terms.get("ee") else True) and
                            ((terms["c1"] in card.course.schedule.class_day_1.lower() if card.course.schedule.class_day_1 else "") if terms.get("c1") else True) and
                            ((terms["c2"] in card.course.schedule.class_day_2.lower() if card.course.schedule.class_day_2 else "") if terms.get("c2") else True) and
                            ((terms["l1"] in card.course.schedule.lab_day_1.lower() if card.course.schedule.lab_day_1 else "") if terms.get("l1") else True) and
                            ((terms["l2"] in card.course.schedule.lab_day_2.lower() if card.course.schedule.lab_day_2 else "") if terms.get("l2") else True) and
                            ((datetime.strptime(card.course.schedule.class_day_1_start_time, "%I:%M %p") == datetime.strptime(terms["c1s"], "%I:%M %p") if card.course.schedule.class_day_1_start_time else False) if terms.get("c1s") else True) and
                            ((datetime.strptime(card.course.schedule.class_day_2_start_time, "%I:%M %p") == datetime.strptime(terms["c2s"], "%I:%M %p") if card.course.schedule.class_day_2_start_time else False) if terms.get("c2s") else True) and
                            ((datetime.strptime(card.course.schedule.class_day_1_end_time, "%I:%M %p") == datetime.strptime(terms["c1e"], "%I:%M %p") if card.course.schedule.class_day_1_end_time else False) if terms.get("c1e") else True) and
                            ((datetime.strptime(card.course.schedule.class_day_2_end_time, "%I:%M %p") == datetime.strptime(terms["c2e"], "%I:%M %p") if card.course.schedule.class_day_2_end_time else False) if terms.get("c2e") else True) and
                            ((datetime.strptime(card.course.schedule.lab_day_1_start_time, "%I:%M %p") == datetime.strptime(terms["l1s"], "%I:%M %p") if card.course.schedule.lab_day_1_start_time else False) if terms.get("l1s") else True) and
                            ((datetime.strptime(card.course.schedule.lab_day_2_start_time, "%I:%M %p") == datetime.strptime(terms["l2s"], "%I:%M %p") if card.course.schedule.lab_day_2_start_time else False) if terms.get("l2s") else True) and
                            ((datetime.strptime(card.course.schedule.lab_day_1_end_time, "%I:%M %p") == datetime.strptime(terms["l1e"], "%I:%M %p") if card.course.schedule.lab_day_1_end_time else False) if terms.get("l1e") else True) and
                            ((datetime.strptime(card.course.schedule.lab_day_2_end_time, "%I:%M %p") == datetime.strptime(terms["l2e"], "%I:%M %p") if card.course.schedule.lab_day_2_end_time else False) if terms.get("l2e") else True) and
                            ((datetime.strptime(card.course.schedule.class_day_1_start_time, "%I:%M %p") >= datetime.strptime(terms["c1sr"], "%I:%M %p") if card.course.schedule.class_day_1_start_time else False) if terms.get("c1sr") else True) and
                            ((datetime.strptime(card.course.schedule.class_day_1_end_time, "%I:%M %p") <= datetime.strptime(terms["c1er"], "%I:%M %p") if card.course.schedule.class_day_1_end_time else False) if terms.get("c1er") else True) and
                            ((datetime.strptime(card.course.schedule.class_day_2_start_time, "%I:%M %p") >= datetime.strptime(terms["c2sr"], "%I:%M %p") if card.course.schedule.class_day_2_start_time else False) if terms.get("c2sr") else True) and
                            ((datetime.strptime(card.course.schedule.class_day_2_end_time, "%I:%M %p") <= datetime.strptime(terms["c2er"], "%I:%M %p") if card.course.schedule.class_day_2_end_time else False) if terms.get("c2er") else True) and
                            ((datetime.strptime(card.course.schedule.lab_day_1_start_time, "%I:%M %p") >= datetime.strptime(terms["l1sr"], "%I:%M %p") if card.course.schedule.lab_day_1_start_time else False) if terms.get("l1sr") else True) and
                            ((datetime.strptime(card.course.schedule.lab_day_1_end_time, "%I:%M %p") <= datetime.strptime(terms["l1er"], "%I:%M %p") if card.course.schedule.lab_day_1_end_time else False) if terms.get("l1er") else True) and
                            ((datetime.strptime(card.course.schedule.lab_day_2_start_time, "%I:%M %p") >= datetime.strptime(terms["l2sr"], "%I:%M %p") if card.course.schedule.lab_day_2_start_time else False) if terms.get("l2sr") else True) and
                            ((datetime.strptime(card.course.schedule.lab_day_2_end_time, "%I:%M %p") <= datetime.strptime(
                                terms["l2er"], "%I:%M %p") if card.course.schedule.lab_day_2_end_time else False) if terms.get("l2er") else True)
                    ):
                        results.append((card, True))
                    else:
                        results.append((card, False))
                elif is_or:
                    section = card.course.section.lower()
                    sec = ""
                    for s in section:
                        if s.isdigit():
                            sec += s
                    section = int(sec)
                    if (
                            (terms["s"] == section if terms.get("s") else False) or
                            (terms["c"] in card.course.course_code.lower() if terms.get("c") else False) or
                            (terms["i"] in card.course.instructor_initial.lower() if terms.get("i") else False) or
                            (terms["p"] in card.course.program.lower() if terms.get("p") else False) or
                            ((terms["f"] in card.course.faculty.lower() if card.course.faculty else False) if terms.get("f") else False) or
                            (terms["in"] in card.course.instructor_name.replace(' ', "").lower() if terms.get("in") else False) or
                            (terms["ct"] in card.course.course_title.replace(' ', "").lower() if terms.get("ct") else False) or
                            (terms["ts"] <= card.course.total_seats if terms.get("ts") else False) or
                            (terms["sb"] <= card.course.seats_remaining if terms.get("sb") else False) or
                            (terms["sr"] <= card.course.seats_remaining if terms.get("sr") else False) or
                            ((terms["e"] in card.course.schedule.exam_date.lower() if card.course.schedule.exam_date else "") if terms.get("e") else False) or
                            ((terms["ed"] in card.course.schedule.exam_day.replace(' ', "").lower() if card.course.schedule.exam_day else "") if terms.get("ed") else False) or
                            ((datetime.strptime(card.course.schedule.exam_start_time, "%I:%M %p") >= datetime.strptime(terms.get("es"), "%I:%M %p") if card.course.schedule.exam_start_time else False) if terms.get("es") else False) or
                            ((datetime.strptime(card.course.schedule.exam_end_time, "%I:%M %p") <= datetime.strptime(terms.get("ee"), "%I:%M %p") if card.course.schedule.exam_end_time else False) if terms.get("ee") else False) or
                            ((terms["c1"] in card.course.schedule.class_day_1.lower() if card.course.schedule.class_day_1 else "") if terms.get("c1") else False) or
                            ((terms["c2"] in card.course.schedule.class_day_2.lower() if card.course.schedule.class_day_2 else "") if terms.get("c2") else False) or
                            ((terms["l1"] in card.course.schedule.lab_day_1.lower() if card.course.schedule.lab_day_1 else "") if terms.get("l1") else False) or
                            ((terms["l2"] in card.course.schedule.lab_day_2.lower() if card.course.schedule.lab_day_2 else "") if terms.get("l2") else False) or
                            ((datetime.strptime(card.course.schedule.class_day_1_start_time, "%I:%M %p") == datetime.strptime(terms["c1s"], "%I:%M %p") if card.course.schedule.class_day_1_start_time else False) if terms.get("c1s") else False) or
                            ((datetime.strptime(card.course.schedule.class_day_2_start_time, "%I:%M %p") == datetime.strptime(terms["c2s"], "%I:%M %p") if card.course.schedule.class_day_2_start_time else False) if terms.get("c2s") else False) or
                            ((datetime.strptime(card.course.schedule.class_day_1_end_time, "%I:%M %p") == datetime.strptime(terms["c1e"], "%I:%M %p") if card.course.schedule.class_day_1_end_time else False) if terms.get("c1e") else False) or
                            ((datetime.strptime(card.course.schedule.class_day_2_end_time, "%I:%M %p") == datetime.strptime(terms["c2e"], "%I:%M %p") if card.course.schedule.class_day_2_end_time else False) if terms.get("c2e") else False) or
                            ((datetime.strptime(card.course.schedule.lab_day_1_start_time, "%I:%M %p") == datetime.strptime(terms["l1s"], "%I:%M %p") if card.course.schedule.lab_day_1_start_time else False) if terms.get("l1s") else False) or
                            ((datetime.strptime(card.course.schedule.lab_day_2_start_time, "%I:%M %p") == datetime.strptime(terms["l2s"], "%I:%M %p") if card.course.schedule.lab_day_2_start_time else False) if terms.get("l2s") else False) or
                            ((datetime.strptime(card.course.schedule.lab_day_1_end_time, "%I:%M %p") == datetime.strptime(terms["l1e"], "%I:%M %p") if card.course.schedule.lab_day_1_end_time else False) if terms.get("l1e") else False) or
                            ((datetime.strptime(card.course.schedule.lab_day_2_end_time, "%I:%M %p") == datetime.strptime(terms["l2e"], "%I:%M %p") if card.course.schedule.lab_day_2_end_time else False) if terms.get("l2e") else False) or
                            ((datetime.strptime(card.course.schedule.class_day_1_start_time, "%I:%M %p") >= datetime.strptime(terms["c1sr"], "%I:%M %p") if card.course.schedule.class_day_1_start_time else False) if terms.get("c1sr") else False) or
                            ((datetime.strptime(card.course.schedule.class_day_1_end_time, "%I:%M %p") <= datetime.strptime(terms["c1er"], "%I:%M %p") if card.course.schedule.class_day_1_end_time else False) if terms.get("c1er") else False) or
                            ((datetime.strptime(card.course.schedule.class_day_2_start_time, "%I:%M %p") >= datetime.strptime(terms["c2sr"], "%I:%M %p") if card.course.schedule.class_day_2_start_time else False) if terms.get("c2sr") else False) or
                            ((datetime.strptime(card.course.schedule.class_day_2_end_time, "%I:%M %p") <= datetime.strptime(terms["c2er"], "%I:%M %p") if card.course.schedule.class_day_2_end_time else False) if terms.get("c2er") else False) or
                            ((datetime.strptime(card.course.schedule.lab_day_1_start_time, "%I:%M %p") >= datetime.strptime(terms["l1sr"], "%I:%M %p") if card.course.schedule.lab_day_1_start_time else False) if terms.get("l1sr") else False) or
                            ((datetime.strptime(card.course.schedule.lab_day_1_end_time, "%I:%M %p") <= datetime.strptime(terms["l1er"], "%I:%M %p") if card.course.schedule.lab_day_1_end_time else False) if terms.get("l1er") else False) or
                            ((datetime.strptime(card.course.schedule.lab_day_2_start_time, "%I:%M %p") >= datetime.strptime(terms["l2sr"], "%I:%M %p") if card.course.schedule.lab_day_2_start_time else False) if terms.get("l2sr") else False) or
                            ((datetime.strptime(card.course.schedule.lab_day_2_end_time, "%I:%M %p") <= datetime.strptime(
                                terms["l2er"], "%I:%M %p") if card.course.schedule.lab_day_2_end_time else False) if terms.get("l2er") else False)
                    ):
                        results.append((card, True))
                    else:
                        results.append((card, False))
        self.search_finished.emit(True, results)
