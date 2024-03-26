class ProfileCourse:
    def __init__(self,
                 course_code: str,
                 course_name: str,
                 course_credit: float,
                 credit_earned: float,
                 grade: str,
                 grade_point: float):
        self.course_code: str = course_code
        self.course_name: str = course_name
        self.course_credit: float = course_credit
        self.credit_earned: float = credit_earned
        self.grade: str = grade
        self.grade_point: float = grade_point

    def __str__(self):
        return f"{self.course_code} - {self.course_name} - {self.course_credit} - {self.credit_earned} - {self.grade} - {self.grade_point}"
