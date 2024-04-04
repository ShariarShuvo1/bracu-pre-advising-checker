from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

from Stylesheet.ProfileDialogStylesheet import DIALOG_STYLE


class UserManualDialog(QDialog):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.setWindowTitle(f"User Manual")
        self.setMinimumHeight(600)
        self.setMinimumWidth(900)
        self.setWindowIcon(QIcon("./Assets/logo.png"))
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)
        self.setStyleSheet(DIALOG_STYLE)

        self.keyword_label = QLabel()
        self.main_layout.addWidget(self.keyword_label)

        html_content = """
            Explanation of Keywords
            s: Represents a section. To define a section, use s=section_name
            c: Stands for course code. You can specify the course code using c=course_code
            i: Indicates the instructor of the course. To include the instructor's name, use i=instructor_name
            p: Denotes the program related to the course. Specify the program using p=program_name
            f: Represents the faculty associated with the course. Include the faculty name using f=faculty_name
            in:  Stands for instructor name. Include the instructor's name using in=instructor_name
            ct:  Represents the course title. Specify the course title using ct=course_title
            ts:  Indicates the total number of seats greater than a specified value. Specify the value using ts=number
            sb:  Represents the number of seats booked greater than a specified value. Specify the value using sb=number
            sr:  Indicates the number of seats remaining greater than a specified value. Specify the value using sr=number
            e: Denotes the exam date. Include the exam date using e=exam_date
            ed:  Represents the exam day. Specify the exam day using ed=exam_day
            es:  Indicates the exam start time. Specify the start time using es=start_time
            ee:  Denotes the exam end time. Specify the end time using ee=end_time
            c1:  Represents class 1 day
            c2:  Represents class 2 day
            l1:  Represents lab 1 day
            l2:  Represents lab 2 day
            c1s: Class 1 start time. Use c1s=start_time
            c1e: Class 1 end time. Use c1e=end_time
            c1sr: Class 1 start from. Use c1sr=start_time
            c1er: Class 1 end till. Use c1er=end_time
            c2s: Class 2 start time. Use c2s=start_time
            c2e: Class 2 end time. Use c2e=end_time
            c2sr: Class 2 start from. Use c2sr=start_time
            c2er: Class 2 end till. Use c2er=end_time
            l1s: Lab 1 start time. Use l1s=start_time
            l1e: Lab 1 end time. Use l1e=end_time
            l1sr: Lab 1 start from. Use l1sr=start_time
            l1er: Lab 1 end till. Use l1er=end_time
            l2s: Lab 2 start time. Use l2s=start_time
            l2e: Lab 2 end time. Use l2e=end_time
            l2sr: Lab 2 start from. Use l2sr=start_time
            l2er: Lab 2 end till. Use l2er=end_time
            
            Here is some example of how you can use the keywords to search for courses:
            c=cse110&i=taw
            This search will return all courses in the CSE110 course which is taken by Tawhid Anwar Sir
            c=cse220&c1er=10:00am&c1=sunday
            This search will return all courses in the CSE220 course which take place in sunday and start from 10 am
        """
        self.keyword_label.setText(html_content)
