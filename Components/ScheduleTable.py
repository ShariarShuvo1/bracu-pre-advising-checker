from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem

from Entity.Course import Course
from Stylesheet.ScheduleTableStylesheet import *
from Constants.day_data import day_list
from datetime import datetime


class ScheduleTable:
    def __init__(self, main):
        self.main = main
        self.courses: list[Course] = []
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Time", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStyleSheet(TABLE_HEADER_STYLE)
        self.table.setCursor(Qt.CursorShape.ArrowCursor)
        self.table.horizontalHeader().setCursor(Qt.CursorShape.ArrowCursor)
        self.table.verticalHeader().setCursor(Qt.CursorShape.ArrowCursor)

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setShowGrid(True)

        self.table.setStyleSheet(TABLE_STYLE)
        self.table.setCursor(Qt.CursorShape.PointingHandCursor)
        self.table.clicked.connect(self.table_clicked)

    def add_course(self, course: Course):
        self.courses.append(course)
        self.update_table()

    def remove_course(self, course: Course):
        self.courses.remove(course)
        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        for course in self.courses:
            course_code = course.course_code
            section = course.section

            data = f"{course_code}-[{section}]"
            lab_data = f"L-{course_code}-[{section}]"

            class_day_1 = course.schedule.class_day_1
            class_day_2 = course.schedule.class_day_2
            lab_day_1 = course.schedule.lab_day_1
            lab_day_2 = course.schedule.lab_day_2

            class_1_time = None
            if class_day_1:
                class_day_1_start_time = course.schedule.class_day_1_start_time
                class_day_1_end_time = course.schedule.class_day_1_end_time
                class_1_time = f"{class_day_1_start_time}\n{
                    class_day_1_end_time}"

            class_2_time = None
            if class_day_2:
                class_day_2_start_time = course.schedule.class_day_2_start_time
                class_day_2_end_time = course.schedule.class_day_2_end_time
                class_2_time = f"{class_day_2_start_time}\n{
                    class_day_2_end_time}"

            lab_1_time = None
            if lab_day_1:
                lab_day_1_start_time = course.schedule.lab_day_1_start_time
                lab_day_1_end_time = course.schedule.lab_day_1_end_time
                lab_1_time = f"{lab_day_1_start_time}\n{lab_day_1_end_time}"

            lab_2_time = None
            if lab_day_2:
                lab_day_2_start_time = course.schedule.lab_day_2_start_time
                lab_day_2_end_time = course.schedule.lab_day_2_end_time
                lab_2_time = f"{lab_day_2_start_time}\n{lab_day_2_end_time}"

            times_to_be_added = [class_1_time,
                                 class_2_time, lab_1_time, lab_2_time]
            times_to_be_added = list(
                filter(lambda x: x is not None, times_to_be_added))
            times_to_be_added = list(set(times_to_be_added))

            for i in range(self.table.rowCount()):
                first_item = self.table.item(i, 0)
                if first_item.text() in times_to_be_added:
                    times_to_be_added.remove(first_item.text())

            for time in times_to_be_added:
                for i in range(self.table.rowCount() + 1):
                    if i == self.table.rowCount():
                        self.table.insertRow(i)
                        self.table.setItem(i, 0, QTableWidgetItem(time))
                        break
                    current_time = self.table.item(i, 0)
                    current_time_start, current_time_end = current_time.text().split("\n")
                    selected_time_start, selected_time_end = time.split("\n")
                    if datetime.strptime(current_time_start, "%I:%M %p") > datetime.strptime(selected_time_start, "%I:%M %p"):
                        self.table.insertRow(i)
                        self.table.setItem(i, 0, QTableWidgetItem(time))
                        break
                    elif datetime.strptime(current_time_start, "%I:%M %p") == datetime.strptime(selected_time_start, "%I:%M %p"):
                        if datetime.strptime(current_time_end, "%I:%M %p") > datetime.strptime(selected_time_end, "%I:%M %p"):
                            self.table.insertRow(i)
                            self.table.setItem(i, 0, QTableWidgetItem(time))
                            break

            for i in range(self.table.rowCount()):
                first_item = self.table.item(i, 0)
                self.table.item(i, 0).setBackground(QColor("#e3c4ff"))
                self.table.item(i, 0).setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter)

                if class_day_1:
                    if first_item.text() == class_1_time:
                        col = day_list.index(class_day_1) + 1
                        item = self.table.item(i, col)
                        if item is None:
                            self.table.setItem(i, col, QTableWidgetItem(data))
                            self.table.item(i, col).setBackground(
                                Qt.GlobalColor.white)
                        else:
                            self.table.setItem(i, col, QTableWidgetItem(
                                f"{item.text()}\n{data}"))
                            self.table.item(i, col).setBackground(
                                QColor("#fc8d8d"))
                if class_day_2:
                    if first_item.text() == class_2_time:
                        col = day_list.index(class_day_2) + 1
                        item = self.table.item(i, col)
                        if item is None:
                            self.table.setItem(i, col, QTableWidgetItem(data))
                            self.table.item(i, col).setBackground(
                                Qt.GlobalColor.white)
                        else:
                            self.table.setItem(i, col, QTableWidgetItem(
                                f"{item.text()}\n{data}"))
                            self.table.item(i, col).setBackground(
                                QColor("#fc8d8d"))
                if lab_day_1:
                    if first_item.text() == lab_1_time:
                        col = day_list.index(lab_day_1) + 1
                        item = self.table.item(i, col)
                        if item is None:
                            self.table.setItem(
                                i, col, QTableWidgetItem(lab_data))
                            self.table.item(i, col).setBackground(
                                Qt.GlobalColor.white)
                        else:
                            self.table.setItem(i, col, QTableWidgetItem(
                                f"{item.text()}\n{lab_data}"))
                            self.table.item(i, col).setBackground(
                                QColor("#fc8d8d"))
                if lab_day_2:
                    if first_item.text() == lab_2_time:
                        col = day_list.index(lab_day_2) + 1
                        item = self.table.item(i, col)
                        if item is None:
                            self.table.setItem(
                                i, col, QTableWidgetItem(lab_data))
                            self.table.item(i, col).setBackground(
                                Qt.GlobalColor.white)
                        else:
                            self.table.setItem(i, col, QTableWidgetItem(
                                f"{item.text()}\n{lab_data}"))
                            self.table.item(i, col).setBackground(
                                QColor("#fc8d8d"))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def table_clicked(self, index):
        x, y = index.row(), index.column()
        item = self.table.item(x, y)
        if item is not None and item.text() != "" and y != 0 and not item.text().startswith("L"):
            text = item.text()
            text = text.split("\n")[0]
            course_code, section = text.split("-")
            section = section[1:-1]
            selected_course = None
            for course in self.courses:
                if course.course_code == course_code and course.section == section:
                    selected_course = course
                    break
            self.main.card_clicked.emit([selected_course])
