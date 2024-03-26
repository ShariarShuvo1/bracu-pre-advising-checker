import requests

from Entity.ProfileCourse import ProfileCourse


class Profile:
    def __init__(self,
                 student_id: str,
                 name: str,
                 picture: requests.Response,
                 program: str,
                 courses: list[ProfileCourse],
                 ):
        self.student_id: str = student_id
        self.name: str = name
        self.picture: requests.Response = picture
        self.program: str = program
        self.courses: list[ProfileCourse] = courses

    def __str__(self):
        return f"Profile({self.student_id}, {self.name})"

    def total_credit(self):
        total: float = 0.0
        for course in self.courses:
            total += course.credit_earned
        return total

    def total_grade_point(self):
        total_grade: float = 0.0
        total_valid_course: int = 0
        for course in self.courses:
            if course.credit_earned > 0.0:
                total_valid_course += 1
                total_grade += course.grade_point
        return str(total_grade / total_valid_course)[:4]
