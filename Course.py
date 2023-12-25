class Course:
    def __init__(self, course_initial, course_name, section_number, total_seat, department_name, department_initial,
                 faculty_name, faculty_initial, exam_date, exam_day, theory_1_day, theory_1_time, theory_2_day=None,
                 theory_2_time=None):
        self.course_initial = course_initial
        self.course_name = course_name
        self.section_number = section_number
        self.total_seat = total_seat
        if self.total_seat is None:
            self.total_seat = 0
        self.department_name = department_name
        self.department_initial = department_initial
        self.faculty_name = faculty_name
        self.faculty_initial = faculty_initial

        # exam
        self.exam_date = exam_date
        e_day = exam_day.split('(')[0]
        if e_day[-1] == ' ':
            self.exam_day = e_day[0:len(e_day) - 1]
        else:
            self.exam_day = e_day
        e_time = exam_day.split('(')[-1]
        e_time = e_time[0:len(e_time) - 1]
        self.exam_time_start = e_time.split('-')[0]
        self.exam_time_end = e_time.split('-')[1]

        # Theory
        self.theory_1_day = theory_1_day

        if len(theory_1_time) == 51:
            temp_time = theory_1_time[17:34]
            self.theory_1_time_start = temp_time.split('-')[0]
            self.theory_1_time_end = temp_time.split('-')[1]
            self.setLab(self.theory_1_day, theory_1_time[:17]+theory_1_time[34:], None, None)
        elif len(theory_1_time) == 34:
            self.theory_1_time_start = theory_1_time[0:17].split('-')[0]
            self.theory_1_time_end = theory_1_time[0:17].split('-')[1]
            theory_2_day = self.theory_1_day
            theory_2_time = theory_1_time[0:17]
        else:
            self.theory_1_time_start = theory_1_time.split('-')[0]
            self.theory_1_time_end = theory_1_time.split('-')[1]

        if theory_2_day is None:
            self.theory_2_day = False
            self.theory_2_time_start = False
            self.theory_2_time_end = False
        else:
            self.theory_2_day = theory_2_day

            if len(theory_2_time) == 51:
                temp_time = theory_2_time[17:34]
                self.theory_2_time_start = temp_time.split('-')[0]
                self.theory_2_time_end = temp_time.split('-')[1]
                self.setLab(self.theory_2_day, theory_2_time[:17]+theory_1_time[34:], None, None)
            elif len(theory_2_time) == 34:
                self.setLab(self.theory_2_day, theory_2_time, None, None)
                self.theory_2_day = False
                self.theory_2_time_start = False
                self.theory_2_time_end = False
            else:
                self.theory_2_time_start = theory_2_time.split('-')[0]
                self.theory_2_time_end = theory_2_time.split('-')[1]

        self.labAvailable = False
        self.lab_1_day = None
        self.lab_2_day = None
        self.lab_1_time_start = None
        self.lab_1_time_end = None
        self.lab_2_time_start = None
        self.lab_2_time_end = None
        self.booked_seat = 0
        self.available_seat = self.total_seat

    def setLab(self, day1, time1, day2, time2):
        self.labAvailable = True
        self.lab_1_day = day1
        if len(time1) > 20:
            self.lab_2_day = day1
            new_time_1 = time1[0:17]
            new_time_2 = time1[17:]
            self.lab_1_time_start = new_time_1.split('-')[0]
            self.lab_1_time_end = new_time_1.split('-')[1]
            self.lab_2_time_start = new_time_2.split('-')[0]
            self.lab_2_time_end = new_time_2.split('-')[1]
            if ((int(self.lab_1_time_start[:2]) * 60) + int(self.lab_1_time_start[3:5])) > (
                    (int(self.lab_2_time_start[:2]) * 60) + int(self.lab_2_time_start[3:5])):
                self.lab_1_day, self.lab_2_day = (self.lab_2_day, self.lab_1_day)
                self.lab_1_time_start, self.lab_2_time_start = (self.lab_2_time_start, self.lab_1_time_start)
                self.lab_1_time_end, self.lab_2_time_end = (self.lab_2_time_end, self.lab_1_time_end)
        else:
            self.lab_1_time_start = time1.split('-')[0]
            self.lab_1_time_end = time1.split('-')[1]
            if day2 is not None:
                self.lab_2_day = day2
                self.lab_2_time_start = time2.split('-')[0]
                self.lab_2_time_end = time2.split('-')[1]
                if ((int(self.lab_1_time_start[:2]) * 60) + int(self.lab_1_time_start[3:5])) > (
                        (int(self.lab_2_time_start[:2]) * 60) + int(self.lab_2_time_start[3:5])):
                    self.lab_1_day, self.lab_2_day = (self.lab_2_day, self.lab_1_day)
                    self.lab_1_time_start, self.lab_2_time_start = (self.lab_2_time_start, self.lab_1_time_start)
                    self.lab_1_time_end, self.lab_2_time_end = (self.lab_2_time_end, self.lab_1_time_end)

    def setSeatStatus(self, booked_seat):
        self.booked_seat = booked_seat
        self.available_seat = int(self.total_seat) - int(self.booked_seat)

    def __str__(self):
        if self.total_seat == 0:
            if self.theory_2_day:
                return f"{self.course_initial} [{self.section_number}] - {self.faculty_initial} - SL: N/A - T: {self.theory_1_day[0:2]},{self.theory_2_day[0:2]} ({self.theory_1_time_start}-{self.theory_1_time_end})"
            else:
                return f"{self.course_initial} [{self.section_number}] - {self.faculty_initial} - SL: N/A - T: {self.theory_1_day[0:2]} ({self.theory_1_time_start}-{self.theory_1_time_end})"
        else:
            if self.theory_2_day:
                return f"{self.course_initial} [{self.section_number}] - {self.faculty_initial} - SL: {self.available_seat} - T: {self.theory_1_day[0:2]},{self.theory_2_day[0:2]} ({self.theory_1_time_start}-{self.theory_1_time_end})"
            else:
                return f"{self.course_initial} [{self.section_number}] - {self.faculty_initial} - SL: {self.available_seat} - T: {self.theory_1_day[0:2]} ({self.theory_1_time_start}-{self.theory_1_time_end})"

    def table_string(self):
        return f'{self.course_initial} [{self.section_number}] - {self.faculty_initial}'

    def advance_string(self):
        return f'{self.course_initial} {self.course_name} {self.section_number} {self.total_seat} {self.department_name} {self.department_initial} {self.faculty_name} {self.faculty_initial} {self.exam_date} {self.exam_day} {self.exam_time_start} {self.exam_time_end} {self.theory_1_day} {self.theory_1_time_start} {self.theory_1_time_end} {self.theory_2_day} {self.theory_2_time_start} {self.theory_2_time_end} {self.lab_1_day} {self.lab_1_time_start} {self.lab_1_time_end} {self.lab_2_day} {self.lab_2_time_start} {self.lab_2_time_end} {self.booked_seat} {self.available_seat}'