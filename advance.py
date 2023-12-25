import webbrowser
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QListWidgetItem
from ObjectBuilder import object_builder
from internetChecker import internet_checker
from Course import Course
from seatStatusThread import jsonThread, loggedInThread


def myNameClicked():
    webbrowser.open_new('https://www.facebook.com/ShariarShuvo01/')


def githubClicked():
    webbrowser.open_new('https://github.com/ShariarShuvo1/bracu-pre-advising-checker')


def listUpdate(listName, searchBar):
    text = searchBar.text()
    for element in range(len(listName)):
        item = listName.item(element)
        if text.lower() not in item.text().lower():
            item.setHidden(True)
        else:
            item.setHidden(False)


def isChecked(check_mark):
    return check_mark.checkState() == Qt.CheckState.Checked


def showWarning(text: str):
    msg = QMessageBox()
    msg.resize(400, 170)
    msg.setMinimumSize(QtCore.QSize(400, 170))
    msg.setBaseSize(QtCore.QSize(400, 170))
    msg.setIcon(msg.Icon.Warning)
    msg.setText(text)
    msg.setWindowTitle("Invalid Course")
    msg.setStandardButtons(msg.StandardButton.Close)
    msg.exec()


class Ui_AdvanceWindow(object):
    def __init__(self):
        self.github = None
        self.my_name = None
        self.seats_data = None
        self.table: QtWidgets.QTableWidget = None
        self.advanceSearch: QtWidgets.QCheckBox = None
        self.item_exist = None
        self.founded_item: Course = None
        self.bound = None
        self.course_list = []
        self.json = None
        self.jsonThreadParser = None
        self.font_size = None
        self.unitWidth = None
        self.unitHeight = None
        self.width = None
        self.height = None
        self.labClash: QtWidgets.QCheckBox = None
        self.theoryClash: QtWidgets.QCheckBox = None
        self.examClash: QtWidgets.QCheckBox = None
        self.pointingHandMouse = QCursor(Qt.CursorShape.PointingHandCursor)
        self.disableAllRestriction: QtWidgets.QCheckBox = None
        self.sameCourse: QtWidgets.QCheckBox = None
        self.seatLimit: QtWidgets.QCheckBox = None
        self.reloadButton: QtWidgets.QPushButton = None
        self.right_search: QtWidgets.QLineEdit = None
        self.left_search: QtWidgets.QLineEdit = None
        self.details_listViewer: QtWidgets.QListWidget = None
        self.clearButton: QtWidgets.QPushButton = None
        self.removeButton: QtWidgets.QPushButton = None
        self.addButton: QtWidgets.QPushButton = None
        self.right_listViewer: QtWidgets.QListWidget = None
        self.left_listViewer: QtWidgets.QListWidget = None
        self.backButton: QtWidgets.QPushButton = None
        self.advance_ui = None
        self.htmlThreadParser = None
        self.centralwidget = None
        self.MainWindow = None
        self.AdvanceWindow = None
        self.html = None

    def labUpdate(self, item):
        day_name = {11: "Sunday", 12: "Monday", 13: "Tuesday", 14: "Wednesday", 15: "Thursday", 16: "Friday",
                    17: "Saturday"}
        day1 = None
        time1 = None
        day2 = None
        time2 = None
        for i in range(11, len(item)):
            if item[i] is not None and day1 is None:
                day1 = day_name[i]
                time1 = item[i]
            elif item[i] is not None:
                day2 = day_name[i]
                time2 = item[i]
        for course in self.course_list:
            if course.course_initial == item[1] and course.section_number == item[3]:
                course.setLab(day1, time1, day2, time2)
                break

    def createCourse(self):
        self.json = self.json['rows']
        for element in self.json:
            item = element['cell']
            if item[10] is not None:
                day_name = {11: "Sunday", 12: "Monday", 13: "Tuesday", 14: "Wednesday", 15: "Thursday", 16: "Friday",
                            17: "Saturday"}
                day1 = None
                time1 = None
                day2 = None
                time2 = None
                for i in range(11, len(item)):
                    if item[i] is not None and day1 is None:
                        day1 = day_name[i]
                        time1 = item[i]
                    elif item[i] is not None:
                        day2 = day_name[i]
                        time2 = item[i]
                self.course_list.append(
                    Course(item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10],
                           day1, time1, day2, time2))
            else:
                self.labUpdate(item)

    def updateSeatStatus(self):
        inserted_count = 0
        self.seats_data = self.seats_data['rows']
        for element in self.seats_data:
            item = element['cell']
            name = item[2]
            section = item[7]
            seat_booked = item[9]
            if len(seat_booked) == 0:
                seat_booked = 0
            for course in self.course_list:
                if name == course.course_initial and section == course.section_number:
                    course.setSeatStatus(seat_booked)
                    inserted_count += 1
                    break
        print(len(self.course_list) - inserted_count)

    def download(self):
        self.AdvanceWindow.setCursor(QCursor(Qt.CursorShape.BusyCursor))
        self.jsonThreadParser = jsonThread()
        self.jsonThreadParser.setter(
            "https://usis.bracu.ac.bd/academia/academicSection/listAcademicSectionWithSchedule?academiaSession=627122&_search=false&nd=1692364983604&rows=-1&page=1&sidx=course_code&sord=asc",
            self.advance_ui, self.session)
        self.jsonThreadParser.start()

    def FoundSeatData(self):
        self.AdvanceWindow.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.updateSeatStatus()
        self.add_to_list()

    def FoundJson(self):
        self.createCourse()
        self.htmlThreadParser = loggedInThread()
        self.htmlThreadParser.setter(
            "https://usis.bracu.ac.bd/academia/studentCourse/showCourseStatusList?query=&academiaSession=627122&_search=false&nd=1692363291093&rows=-1&page=1&sidx=id&sord=desc",
            self.advance_ui, self.session)
        self.htmlThreadParser.start()

    def find_row_number(self, time_string):
        for i in range(self.table.rowCount()):
            if self.table.verticalHeaderItem(i).text() == time_string:
                return i

    def find_column_number(self, day):
        for i in range(self.table.columnCount()):
            if self.table.horizontalHeaderItem(i).text() == f' {day} ':
                return i

    def get_row_col(self, time1, time2, day):
        time_string = f'{time1} - \n{time2}'
        row = self.find_row_number(time_string)
        column = self.find_column_number(day)
        return [row, column]

    def setting_table(self, row, column, txt: str):
        temp_txt = self.table.item(row, column)
        if temp_txt is None:
            temp = QTableWidgetItem(txt)
            temp.setForeground(QtGui.QColor('yellow'))
            self.table.setItem(row, column, temp)
            self.table.showRow(row)
        else:
            temp = QTableWidgetItem(f'{temp_txt.text()}\n{txt}')
            temp.setForeground(QtGui.QColor('red'))
            self.table.setItem(row, column, temp)
            self.table.showRow(row)

    def resize_table(self):
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def add_to_table(self, list_text):
        current_course: Course = self.find_course_by_string(list_text)
        if current_course.theory_1_day is not None:
            row, column = self.get_row_col(current_course.theory_1_time_start, current_course.theory_1_time_end,
                                           current_course.theory_1_day)
            self.setting_table(row, column, current_course.table_string())
        if current_course.theory_2_day is not False:
            row, column = self.get_row_col(current_course.theory_2_time_start, current_course.theory_2_time_end,
                                           current_course.theory_2_day)
            self.setting_table(row, column, current_course.table_string())
        if current_course.lab_1_day is not None:
            row, column = self.get_row_col(current_course.lab_1_time_start, current_course.lab_1_time_end,
                                           current_course.lab_1_day)
            self.setting_table(row, column, current_course.table_string().split(' - ')[0] + ' - LAB')
        if current_course.lab_2_day is not None:
            row, column = self.get_row_col(current_course.lab_2_time_start, current_course.lab_2_time_end,
                                           current_course.lab_2_day)
            self.setting_table(row, column, current_course.table_string().split(' - ')[0] + ' - LAB')
        self.resize_table()

    def add_to_list(self):
        for course in self.course_list:
            self.left_listViewer.addItem(str(course))

    def setupBody(self):
        if internet_checker():
            self.download()

        self.font_size = int(0.8 * self.unitWidth)

        # Back Button
        self.backButton = object_builder(QtWidgets.QPushButton(parent=self.centralwidget),
                                         (int(self.unitWidth * 0.5), 1, self.unitWidth * 6, self.unitHeight * 4),
                                         "<- BACK", self.font_size, False,
                                         "QPushButton::!hover { border: 1px solid white; background-color: rgba(0, 0, 0, 0);} QPushButton::hover {border : 1px solid red; background-color: rgba(0, 0, 0, 0);};",
                                         self.backButtonClicked, self.pointingHandMouse, "Return to home page")

        # Restart Button
        self.reloadButton = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (
            int((self.unitWidth * 6.5) + (self.unitWidth * 0.5)), 1, self.unitWidth * 6, self.unitHeight * 4), "Reload",
                                           self.font_size, False,
                                           "QPushButton::!hover { border: 1px solid white; background-color: rgba(0, 0, 0, 0);} QPushButton::hover {border : 1px solid green; background-color: rgba(0, 0, 0, 0);};",
                                           self.reloadButtonClicked, self.pointingHandMouse,
                                           "Reload the data from USIS. This will clear all of your list")

        # Disable Seat Limit
        self.seatLimit = object_builder(QtWidgets.QCheckBox(parent=self.centralwidget), (
            int((self.unitWidth * 13) + (self.unitWidth * 0.5)), 1, self.unitWidth * 10, self.unitHeight * 4),
                                        "Disable Seat Limit", self.font_size, False,
                                        "border: 1px solid white; background-color: rgba(0, 0, 0, 0);",
                                        self.seatLimitClicked, self.pointingHandMouse,
                                        "You will be able to select sections which does not have any seat left")

        # Allow Same Course
        self.sameCourse = object_builder(QtWidgets.QCheckBox(parent=self.centralwidget), (
            int((self.unitWidth * 23.5) + (self.unitWidth * 0.5)), 1, self.unitWidth * 11, self.unitHeight * 4),
                                         "Allow Same Course", self.font_size, False,
                                         "border: 1px solid white; background-color: rgba(0, 0, 0, 0);",
                                         self.sameCourseClicked, self.pointingHandMouse,
                                         "You will be able to select same course multiple times")

        # Allow Exam Clash
        self.examClash = object_builder(QtWidgets.QCheckBox(parent=self.centralwidget), (
            int((self.unitWidth * 35) + (self.unitWidth * 0.5)), 1, self.unitWidth * 10, self.unitHeight * 4),
                                        "Allow Exam Clash", self.font_size, False,
                                        "border: 1px solid white; background-color: rgba(0, 0, 0, 0);",
                                        self.examClashClicked, self.pointingHandMouse,
                                        "You will be able to select courses with same exam date")

        # Allow Theory Clash
        self.theoryClash = object_builder(QtWidgets.QCheckBox(parent=self.centralwidget), (
            int((self.unitWidth * 45.5) + (self.unitWidth * 0.5)), 1, self.unitWidth * 11, self.unitHeight * 4),
                                          "Allow Theory Clash", self.font_size, False,
                                          "border: 1px solid white; background-color: rgba(0, 0, 0, 0);",
                                          self.theoryClashClicked, self.pointingHandMouse,
                                          "You will be able to select courses with same theory schedule")

        # Allow Lab Clash
        self.labClash = object_builder(QtWidgets.QCheckBox(parent=self.centralwidget), (
            int((self.unitWidth * 57) + (self.unitWidth * 0.5)), 1, self.unitWidth * 11, self.unitHeight * 4),
                                       "Allow Lab Clash", self.font_size, False,
                                       "border: 1px solid white; background-color: rgba(0, 0, 0, 0);",
                                       self.labClashClicked, self.pointingHandMouse,
                                       "You will be able to select courses with same lab schedule")
        self.labClash.setChecked(True)

        # Disable all restriction
        self.disableAllRestriction = object_builder(QtWidgets.QCheckBox(parent=self.centralwidget), (
            int((self.unitWidth * 68.5) + (self.unitWidth * 0.5)), 1, self.unitWidth * 12, self.unitHeight * 4),
                                                    "Disable All Restriction", self.font_size, False,
                                                    "border: 1px solid white; background-color: rgba(0, 0, 0, 0);",
                                                    self.disableAllRestrictionClicked, self.pointingHandMouse,
                                                    "There will be no restriction to add courses")

        # Advance Search
        self.advanceSearch = object_builder(QtWidgets.QCheckBox(parent=self.centralwidget), (
            int((self.unitWidth * 81) + (self.unitWidth * 0.5)), 1, self.unitWidth * 9, self.unitHeight * 4),
                                            "Advance Search", self.font_size, False,
                                            "border: 1px solid white; background-color: rgba(0, 0, 0, 0);",
                                            self.advanceSearchClicked, self.pointingHandMouse,
                                            "You will be able to filter data using keyword")

        # Left Search Bar
        self.left_search: QtWidgets.QLineEdit = object_builder(QtWidgets.QLineEdit(parent=self.centralwidget), (
            int(self.unitWidth * 0.5), int(self.unitHeight * 5), int(self.unitWidth * 15), int(self.unitHeight * 4)),
                                                               "Search", self.font_size + 5, False,
                                                               "QLineEdit{border:1px solid white; color: white}")
        self.left_search.textEdited.connect(self.leftSearchChanged)

        # Left List Viewer
        self.left_listViewer: QtWidgets.QListWidget = object_builder(QtWidgets.QListWidget(parent=self.centralwidget), (
            int(self.unitWidth * 0.5), int(self.unitHeight * 10), int(self.unitWidth * 15),
            int((self.unitHeight * 100) - (self.unitHeight * 11))), None, self.font_size, False,
                                                                     "QListWidget{border:1px solid white; alternate-background-color: #232323;background-color: black;};")
        self.left_listViewer.setAlternatingRowColors(True)
        self.left_listViewer.itemSelectionChanged.connect(self.left_listViewer_selection_changed)

        # # Add Button
        self.addButton = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (
            int(self.unitWidth * 16), int(self.unitHeight * 10), int(self.unitWidth * 6), int(self.unitHeight * 4)),
                                        "Add ->", self.font_size, True,
                                        "QPushButton{border:1px solid yellow} QPushButton::hover{border:1px solid green; color:green}",
                                        self.addButtonClicked, self.pointingHandMouse,
                                        "Add the selected course to your list")

        # Remove Button
        self.removeButton = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (
            int(self.unitWidth * 16), int(self.unitHeight * 14.5), int(self.unitWidth * 6), int(self.unitHeight * 4)),
                                           "<- Remove", self.font_size, True,
                                           "QPushButton{border:1px solid yellow} QPushButton::hover{border:1px solid magenta; color: magenta}",
                                           self.removeButtonClicked, self.pointingHandMouse,
                                           "Remove the course from your list")
        #
        # Clear All Button
        self.clearButton = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (
            int(self.unitWidth * 16), int(self.unitHeight * 19), int(self.unitWidth * 6), int(self.unitHeight * 4)),
                                          "Clear -X", self.font_size, True,
                                          "QPushButton{border:1px solid yellow} QPushButton::hover{border:1px solid red; color:red}",
                                          self.clearButtonClicked, self.pointingHandMouse,
                                          "Remove all the course from your list")

        # Right Search Bar
        self.right_search: QtWidgets.QLineEdit = object_builder(QtWidgets.QLineEdit(parent=self.centralwidget), (
            int(self.unitWidth * 22.5), int(self.unitHeight * 5), int(self.unitWidth * 15), int(self.unitHeight * 4)),
                                                                "Search", self.font_size + 5, False,
                                                                "QLineEdit{border:1px solid white; color: white}")
        self.right_search.textEdited.connect(self.rightSearchChanged)

        # Right List Viewer
        self.right_listViewer = object_builder(QtWidgets.QListWidget(parent=self.centralwidget), (
            int(self.unitWidth * 22.5), int(self.unitHeight * 10), int(self.unitWidth * 15), int(self.unitHeight * 25)),
                                               None, self.font_size, False,
                                               "QListWidget{border:1px solid white; alternate-background-color: #232323;background-color: black;};")
        self.right_listViewer.setAlternatingRowColors(True)
        self.right_listViewer.itemSelectionChanged.connect(self.right_listViewer_selection_changed)

        # Details Viewer
        self.details_listViewer: QtWidgets.QListWidget = object_builder(
            QtWidgets.QListWidget(parent=self.centralwidget), (
                int(self.unitWidth * 22.5), int(self.unitHeight * 36), int(self.unitWidth * 15),
                int((self.unitHeight * 100) - (self.unitHeight * 37))), None, self.font_size, False,
            "QListWidget{border:1px solid white; color:white; alternate-background-color: #232323;background-color: black;};")
        self.details_listViewer.setAlternatingRowColors(True)
        self.setupSchedule()

        self.my_name = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (
            int(self.unitWidth * 38), int((self.unitHeight * 100) - (self.unitHeight * 10)) + int(self.unitHeight * 5),
            int(self.unitWidth * 15), int(self.unitHeight * 2)), "Created By: Shariar Islam Shuvo", self.font_size,
                                      False,
                                      "QPushButton::hover{color:red}", myNameClicked, self.pointingHandMouse,
                                      "Click to visit my Facebook Profile")
        self.github = object_builder(QtWidgets.QPushButton(parent=self.centralwidget), (
            int(self.unitWidth * 55), int((self.unitHeight * 100) - (self.unitHeight * 10)) + int(self.unitHeight * 5),
            int(self.unitWidth * 6), int(self.unitHeight * 2)), "GitHub", self.font_size, False,
                                     "QPushButton::hover{color:red}", githubClicked, self.pointingHandMouse,
                                     "Click to visit GitHub repo for this project")

    def setupSchedule(self):
        self.table = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.table.setGeometry(QtCore.QRect(int(self.unitWidth * 38), int(self.unitHeight * 5),
                                            int((self.unitWidth * 100) - (self.unitWidth * 39)),
                                            int((self.unitHeight * 100) - (self.unitHeight * 10))))
        self.table.setRowCount(26)
        self.table.setColumnCount(7)

        days = [" Saturday ", " Sunday ", " Monday ", " Tuesday ", " Wednesday ", " Thursday ", " Friday "]
        times = ['08:00 AM - \n09:20 AM', '08:00 AM - \n11:05 AM', '09:00 AM - \n09:55 AM', '09:00 AM - \n12:00 PM',
                 '09:00 AM - \n12:05 PM', '09:00 AM - \n01:10 PM', '09:30 AM - \n10:50 AM', '10:05 AM - \n11:00 AM',
                 '11:00 AM - \n12:20 PM', '11:00 AM - \n01:30 AM', '11:10 AM - \n12:05 PM', '12:15 PM - \n01:10 PM',
                 '12:30 PM - \n01:30 PM', '12:30 PM - \n01:50 PM', '01:20 PM - \n02:15 PM', '02:00 PM - \n02:55 PM',
                 '02:00 PM - \n03:20 PM', '02:00 PM - \n04:00 PM', '02:00 PM - \n05:05 PM', '03:05 PM - \n04:00 PM',
                 '03:30 PM - \n04:50 PM', '04:10 PM - \n05:05 PM', '05:00 PM - \n06:20 PM', '05:00 PM - \n06:30 PM',
                 '05:05 PM - \n06:00 PM', '06:00 PM - \n09:00 PM']
        self.table.setHorizontalHeaderLabels(days)
        self.table.setVerticalHeaderLabels(times)
        self.table.setAlternatingRowColors(True)
        for i in range(0, 26):
            self.table.hideRow(i)
        self.resize_table()
        self.table.setDisabled(True)

    def setupUi(self, AdvanceWindow, MainWindow, advance_ui, session):
        self.session = session
        self.advance_ui = advance_ui
        self.AdvanceWindow = AdvanceWindow
        self.MainWindow = MainWindow
        self.unitHeight = int(self.height / 100)
        self.unitWidth = int(self.width / 100)
        AdvanceWindow.resize(self.width, self.height)
        AdvanceWindow.setMinimumSize(QtCore.QSize(self.width, self.height))
        AdvanceWindow.setBaseSize(QtCore.QSize(self.width, self.height))
        AdvanceWindow.setStyleSheet("background-color: black; color: yellow")
        AdvanceWindow.setWindowTitle("Pre Advising Advance")
        self.centralwidget = QtWidgets.QWidget(parent=AdvanceWindow)

        self.setupBody()

        # Initiate texts
        AdvanceWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(AdvanceWindow)

    def show_description(self, course_name, section):
        current_course: Course = None
        for course in self.course_list:
            if course.course_initial == course_name and course.section_number == section:
                current_course = course
                break
        self.details_listViewer.clear()
        self.details_listViewer.addItem(f'Course Name: {current_course.course_name}')
        self.details_listViewer.addItem(f'Course Code: {current_course.course_initial}')
        self.details_listViewer.addItem(f'Section Number: {current_course.section_number}')
        self.details_listViewer.addItem(f'Total Seat: {current_course.total_seat}')
        self.details_listViewer.addItem(f'Booked Seat: {current_course.booked_seat}')
        self.details_listViewer.addItem(f'Available Seat: {current_course.available_seat}')
        self.details_listViewer.addItem(f'Faculty Name: {current_course.faculty_name}')
        self.details_listViewer.addItem(f'Faculty Initial: {current_course.faculty_initial}')
        self.details_listViewer.addItem(f'Department Name: {current_course.department_name}')
        self.details_listViewer.addItem(f'Department Initial: {current_course.department_initial}')
        self.details_listViewer.addItem("")
        self.details_listViewer.addItem(f'Mid-Term Date: {current_course.exam_date}')
        self.details_listViewer.addItem(
            f'Mid-Term Time: ({current_course.exam_time_start} - {current_course.exam_time_end})')
        self.details_listViewer.addItem(f'Mid-Term Day: {current_course.exam_day}')
        self.details_listViewer.addItem("")
        self.details_listViewer.addItem(f'Theory Class Day 1: {current_course.theory_1_day}')
        self.details_listViewer.addItem(
            f'Theory Class Day 1 Time: ({current_course.theory_1_time_start} - {current_course.theory_1_time_end})')
        if current_course.theory_2_day is not None:
            self.details_listViewer.addItem(f'Theory Class Day 2: {current_course.theory_2_day}')
            self.details_listViewer.addItem(
                f'Theory Class Day 2 Time: ({current_course.theory_2_time_start} - {current_course.theory_2_time_end})')
        self.details_listViewer.addItem("")
        if current_course.labAvailable:
            if current_course.lab_2_day is not None:
                self.details_listViewer.addItem(f'Lab Day: {current_course.lab_1_day}')
                self.details_listViewer.addItem(
                    f'Lab Time First Half: ({current_course.lab_1_time_start} - {current_course.lab_1_time_end})')
                self.details_listViewer.addItem(
                    f'Lab Time Second Half: ({current_course.lab_2_time_start} - {current_course.lab_2_time_end})')
            else:
                self.details_listViewer.addItem(f'Lab Day 1: {current_course.lab_1_day}')
                self.details_listViewer.addItem(
                    f'Lab Day 1 Time: ({current_course.lab_1_time_start} - {current_course.lab_1_time_end})')
                self.details_listViewer.addItem(f'Lab Day 2: {current_course.lab_2_day}')
                self.details_listViewer.addItem(
                    f'Lab Time Second Half: ({current_course.lab_2_time_start} - {current_course.lab_2_time_end})')

    def find_course_by_string(self, item):
        for course in self.course_list:
            if str(course) == item:
                return course

    def already_exist(self, element):
        for i in range(len(self.left_listViewer)):
            if self.left_listViewer.item(i).text() == element:
                return True
        return False

    def add_to_right_list(self, element):
        self.right_listViewer.addItem(element)
        self.add_to_table(element)

    def bound_checker(self, item):
        self.founded_item: Course = self.find_course_by_string(item)
        self.item_exist = self.already_exist(item)
        self.bound = [True] * 5
        for i in range(len(self.right_listViewer)):
            if self.right_listViewer.item(i).text() == item:
                showWarning("You can not take same course section twice")
                self.bound[0] = False
        if False in self.bound:
            return False
        if not isChecked(self.seatLimit):
            if self.founded_item.available_seat == 0 and self.founded_item.total_seat != 0:
                showWarning("There are no seat left!")
                self.bound[0] = False
        if False in self.bound:
            return False
        if not isChecked(self.sameCourse):
            temp_course = item.split()[0]
            for i in range(len(self.right_listViewer)):
                comp_course = self.right_listViewer.item(i).text().split()[0]
                if temp_course == comp_course:
                    showWarning("Your already took this Course!")
                    self.bound[1] = False
                    break
        if False in self.bound:
            return False
        if not isChecked(self.examClash):
            for i in range(len(self.right_listViewer)):
                temp_course = self.find_course_by_string(self.right_listViewer.item(i).text())
                if self.founded_item.exam_date == temp_course.exam_date and self.founded_item.exam_time_start == temp_course.exam_time_start:
                    showWarning(f"Your Exam Date Clashes with\n{temp_course}")
                    self.bound[2] = False
                    break
        if False in self.bound:
            return False
        if not isChecked(self.theoryClash):
            for i in range(len(self.right_listViewer)):
                temp_course: Course = self.find_course_by_string(self.right_listViewer.item(i).text())
                temp_list = [temp_course.theory_1_day, temp_course.theory_1_time_start, temp_course.theory_1_time_end]
                if self.founded_item.theory_1_day in temp_list and (
                        self.founded_item.theory_1_time_start in temp_list or self.founded_item.theory_1_time_end in temp_list):
                    showWarning(f"Your Theory Class Clashes with\n{temp_course}")
                    self.bound[3] = False
                    break
                if self.founded_item.theory_2_day is not None:
                    if self.founded_item.theory_2_day in temp_list and (
                            self.founded_item.theory_2_time_start in temp_list or self.founded_item.theory_2_time_end in temp_list):
                        showWarning(f"Your Theory Class Clashes with\n{temp_course}")
                        self.bound[3] = False
                        break
                if temp_course.theory_2_day is not None:
                    temp_list = [temp_course.theory_2_day, temp_course.theory_2_time_start,
                                 temp_course.theory_2_time_end]
                    if self.founded_item.theory_1_day in temp_list and (
                            self.founded_item.theory_1_time_start in temp_list or self.founded_item.theory_1_time_end in temp_list):
                        showWarning(f"Your Theory Class Clashes with\n{temp_course}")
                        self.bound[3] = False
                        break
                    if self.founded_item.theory_2_day is not None:
                        if self.founded_item.theory_2_day in temp_list and (
                                self.founded_item.theory_2_time_start in temp_list or self.founded_item.theory_2_time_end in temp_list):
                            showWarning(f"Your Theory Class Clashes with\n{temp_course}")
                            self.bound[3] = False
                            break
                if not self.bound[3]:
                    break
        if False in self.bound:
            return False
        if not isChecked(self.labClash):
            for i in range(len(self.right_listViewer)):
                temp_course: Course = self.find_course_by_string(self.right_listViewer.item(i).text())
                temp_list = [temp_course.theory_1_day, temp_course.theory_1_time_start, temp_course.theory_1_time_end]
                if self.founded_item.lab_1_day in temp_list and (
                        self.founded_item.lab_1_time_start in temp_list or self.founded_item.lab_1_time_end in temp_list):
                    showWarning(f"Your LAB Class Clashes with\n{temp_course}")
                    self.bound[3] = False
                    break
                if self.founded_item.lab_2_day is not None:
                    if self.founded_item.lab_2_day in temp_list and (
                            self.founded_item.lab_2_time_start in temp_list or self.founded_item.lab_2_time_end in temp_list):
                        showWarning(f"Your LAB Class Clashes with\n{temp_course}")
                        self.bound[3] = False
                        break
                if temp_course.theory_2_day is not None:
                    temp_list = [temp_course.theory_2_day, temp_course.theory_2_time_start,
                                 temp_course.theory_2_time_end]
                    if self.founded_item.lab_1_day in temp_list and (
                            self.founded_item.lab_1_time_start in temp_list or self.founded_item.lab_1_time_end in temp_list):
                        showWarning(f"Your LAB Class Clashes with\n{temp_course}")
                        self.bound[3] = False
                        break
                    if self.founded_item.lab_2_day is not None:
                        if self.founded_item.lab_2_day in temp_list and (
                                self.founded_item.lab_2_time_start in temp_list or self.founded_item.lab_2_time_end in temp_list):
                            showWarning(f"Your LAB Class Clashes with\n{temp_course}")
                            self.bound[3] = False
                            break
                temp_list = [temp_course.lab_1_day, temp_course.lab_1_time_start, temp_course.lab_1_time_end]
                if self.founded_item.lab_1_day in temp_list and (
                        self.founded_item.lab_1_time_start in temp_list or self.founded_item.lab_1_time_end in temp_list):
                    showWarning(f"Your LAB Class Clashes with\n{temp_course}")
                    self.bound[3] = False
                    break
                if self.founded_item.lab_2_day is not None:
                    if self.founded_item.lab_2_day in temp_list and (
                            self.founded_item.lab_2_time_start in temp_list or self.founded_item.lab_2_time_end in temp_list):
                        showWarning(f"Your LAB Class Clashes with\n{temp_course}")
                        self.bound[3] = False
                        break
                if temp_course.theory_2_day is not None:
                    temp_list = [temp_course.lab_2_day, temp_course.lab_2_time_start, temp_course.lab_2_time_end]
                    if self.founded_item.lab_1_day in temp_list and (
                            self.founded_item.lab_1_time_start in temp_list or self.founded_item.lab_1_time_end in temp_list):
                        showWarning(f"Your LAB Class Clashes with\n{temp_course}")
                        self.bound[3] = False
                        break
                    if self.founded_item.lab_2_day is not None:
                        if self.founded_item.lab_2_day in temp_list and (
                                self.founded_item.lab_2_time_start in temp_list or self.founded_item.lab_2_time_end in temp_list):
                            showWarning(f"Your LAB Class Clashes with\n{temp_course}")
                            self.bound[3] = False
                            break
                if not self.bound[3]:
                    break
        if False in self.bound:
            return False
        else:
            return True

    def addButtonClicked(self):
        item = self.left_listViewer.currentItem()
        if item is not None:
            item = item.text()
            if isChecked(self.disableAllRestriction):
                self.add_to_right_list(item)
            elif self.bound_checker(item):
                self.add_to_right_list(item)

    def removing_table(self, row, column, txt: str):
        table_item = self.table.item(row, column)
        if len(table_item.text()) == len(txt):
            self.table.takeItem(row, column)
        else:
            temp: str = table_item.text()
            idx = temp.find(f'\n{temp}')
            if idx > 0:
                temp1 = temp[:idx]
                if len(temp) == idx + len(txt) + 1:
                    temp2 = ''
                else:
                    temp2 = temp[idx + len(txt) + 1:]
                temp = temp1 + temp2
            else:
                temp = temp[len(txt) + 1:]
            if temp.count('\n') > 0:
                self.table.takeItem(row, column)
                element = QTableWidgetItem(temp)
                element.setForeground(QtGui.QColor('red'))
                self.table.setItem(row, column, element)
            else:
                self.table.takeItem(row, column)
                element = QTableWidgetItem(temp)
                element.setForeground(QtGui.QColor('yellow'))
                self.table.setItem(row, column, QTableWidgetItem(element))
        found_item = False
        for i in range(7):
            if self.table.item(row, i) is not None:
                if self.table.item(row, i).text() != '':
                    found_item = True
        if not found_item:
            self.table.hideRow(row)

    def remove_from_table(self, temp_item):
        txt = temp_item.text()
        current_course: Course = self.find_course_by_string(txt)
        if current_course.theory_1_day is not None:
            row, column = self.get_row_col(current_course.theory_1_time_start, current_course.theory_1_time_end,
                                           current_course.theory_1_day)
            self.removing_table(row, column, current_course.table_string())
        if current_course.theory_2_day is not None:
            row, column = self.get_row_col(current_course.theory_2_time_start, current_course.theory_2_time_end,
                                           current_course.theory_2_day)
            self.removing_table(row, column, current_course.table_string())
        if current_course.lab_1_day is not None:
            row, column = self.get_row_col(current_course.lab_1_time_start, current_course.lab_1_time_end,
                                           current_course.lab_1_day)
            self.removing_table(row, column, current_course.table_string().split(' - ')[0] + ' - LAB')
        if current_course.lab_2_day is not None:
            row, column = self.get_row_col(current_course.lab_2_time_start, current_course.lab_2_time_end,
                                           current_course.lab_2_day)
            self.removing_table(row, column, current_course.table_string().split(' - ')[0] + ' - LAB')
        self.resize_table()

    def removeButtonClicked(self):
        item = self.right_listViewer.currentRow()
        if item != -1:
            temp_item = self.right_listViewer.takeItem(item)
            self.remove_from_table(temp_item)

    def clearButtonClicked(self):
        mn = self.table.rowCount()
        for i in range(mn):
            for j in range(self.table.columnCount()):
                self.table.takeItem(i, j)
            self.table.hideRow(i)
        self.resize_table()
        self.right_listViewer.clear()
        self.advanceSearch.setChecked(False)
        self.seatLimit.setChecked(False)
        self.sameCourse.setChecked(False)
        self.examClash.setChecked(False)
        self.theoryClash.setChecked(False)
        self.labClash.setChecked(True)
        self.disableAllRestriction.setChecked(False)

    def left_listViewer_selection_changed(self):
        if self.left_listViewer.currentItem() is not None:
            item = self.left_listViewer.currentItem().text()
            course_name = item.split('[')[0]
            course_name = course_name[0:len(course_name) - 1]
            section = item.split('[')[1]
            section = section[0:2]
            self.show_description(course_name, section)

    def right_listViewer_selection_changed(self):
        item = self.right_listViewer.currentItem()
        if item is not None:
            item = item.text()
            course_name = item.split('[')[0]
            course_name = course_name[0:len(course_name) - 1]
            section = item.split('[')[1]
            section = section[0:2]
            self.show_description(course_name, section)

    def backButtonClicked(self):
        self.MainWindow.show()
        self.AdvanceWindow.hide()

    def seatLimitClicked(self):
        if not isChecked(self.seatLimit):
            self.disableAllRestriction.setChecked(False)
        if isChecked(self.labClash) and isChecked(self.theoryClash) and isChecked(self.examClash) and isChecked(
                self.seatLimit) and isChecked(self.sameCourse):
            self.disableAllRestriction.setChecked(True)

    def sameCourseClicked(self):
        if not isChecked(self.sameCourse):
            self.disableAllRestriction.setChecked(False)
        if isChecked(self.labClash) and isChecked(self.theoryClash) and isChecked(self.examClash) and isChecked(
                self.seatLimit) and isChecked(self.sameCourse):
            self.disableAllRestriction.setChecked(True)

    def examClashClicked(self):
        if not isChecked(self.examClash):
            self.disableAllRestriction.setChecked(False)
        if isChecked(self.labClash) and isChecked(self.theoryClash) and isChecked(self.examClash) and isChecked(
                self.seatLimit) and isChecked(self.sameCourse):
            self.disableAllRestriction.setChecked(True)

    def theoryClashClicked(self):
        if not isChecked(self.theoryClash):
            self.disableAllRestriction.setChecked(False)
        if isChecked(self.labClash) and isChecked(self.theoryClash) and isChecked(self.examClash) and isChecked(
                self.seatLimit) and isChecked(self.sameCourse):
            self.disableAllRestriction.setChecked(True)

    def labClashClicked(self):
        if not isChecked(self.labClash):
            self.disableAllRestriction.setChecked(False)
        if isChecked(self.labClash) and isChecked(self.theoryClash) and isChecked(self.examClash) and isChecked(
                self.seatLimit) and isChecked(self.sameCourse):
            self.disableAllRestriction.setChecked(True)

    def advanceSearchClicked(self):
        if isChecked(self.advanceSearch):
            msg = QMessageBox()
            msg.resize(600, 250)
            msg.setMinimumSize(QtCore.QSize(600, 250))
            msg.setBaseSize(QtCore.QSize(600, 250))
            msg.setIcon(msg.Icon.Warning)
            msg.setText(
                f"You will be able to search with custom parameter\nlike: faculty name, specific time in any order etc\n\nbut your searching will be too much slower\nEx: zaber mohammad cse220 sunday tuesday\nEx: cse320 gazzali\nEx: cse260 monday\n\nAre you sure you want to activate advance search?")
            msg.setWindowTitle("Performance Warning!")
            msg.setStandardButtons(msg.StandardButton.Yes | msg.StandardButton.No)
            msg.exec()
            if msg.standardButton(msg.clickedButton()) == msg.StandardButton.No:
                self.advanceSearch.setChecked(False)

    def disableAllRestrictionClicked(self):
        if isChecked(self.disableAllRestriction):
            self.seatLimit.setChecked(True)
            self.sameCourse.setChecked(True)
            self.examClash.setChecked(True)
            self.theoryClash.setChecked(True)
            self.labClash.setChecked(True)
        else:
            self.seatLimit.setChecked(False)
            self.sameCourse.setChecked(False)
            self.examClash.setChecked(False)
            self.theoryClash.setChecked(False)
            self.labClash.setChecked(False)

    def reloadButtonClicked(self):
        msg = QMessageBox()
        msg.resize(300, 170)
        msg.setMinimumSize(QtCore.QSize(300, 170))
        msg.setBaseSize(QtCore.QSize(300, 170))
        msg.setIcon(msg.Icon.Warning)
        msg.setText(f"All of your list will be LOST\nDo you want to Reload?")
        msg.setWindowTitle("Reload Warning!")
        msg.setStandardButtons(msg.StandardButton.Yes | msg.StandardButton.No)
        msg.exec()

        if msg.standardButton(msg.clickedButton()) == msg.StandardButton.Yes:
            if internet_checker():
                self.clearButtonClicked()
                self.left_listViewer.clear()
                self.right_listViewer.clear()
                self.details_listViewer.clear()
                self.download()

    def advanceListUpdate(self, listName, searchBar):
        if len(searchBar.text()) > 0:
            text_array = searchBar.text().split(' ')
            for part in text_array:
                for element in range(len(listName)):
                    item = listName.item(element)
                    current_course: Course = self.find_course_by_string(item.text())
                    if part.lower() not in current_course.advance_string().lower():
                        item.setHidden(True)
                    else:
                        item.setHidden(False)

    def leftSearchChanged(self):
        self.left_listViewer.setCurrentItem(QListWidgetItem(None))
        self.right_listViewer.setCurrentItem(QListWidgetItem(None))
        if isChecked(self.advanceSearch):
            self.advanceListUpdate(self.left_listViewer, self.left_search)
        else:
            listUpdate(self.left_listViewer, self.left_search)

    def rightSearchChanged(self):
        self.left_listViewer.setCurrentItem(QListWidgetItem(None))
        self.right_listViewer.setCurrentItem(QListWidgetItem(None))
        if isChecked(self.advanceSearch):
            self.advanceListUpdate(self.right_listViewer, self.right_search)
        else:
            listUpdate(self.right_listViewer, self.right_search)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    AdvanceWindow = QtWidgets.QMainWindow()
    ui = Ui_AdvanceWindow()
    screenSize = app.screens()[0].availableGeometry()
    ui.height = screenSize.height()
    ui.width = screenSize.width()
    ui.setupUi(AdvanceWindow, None, ui, None)
    AdvanceWindow.show()
    sys.exit(app.exec())
