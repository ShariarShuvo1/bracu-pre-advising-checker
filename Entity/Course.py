from Entity.Schedule import Schedule


class Course:
    def __init__(
            self,
            course_code: str,
            course_title: str,
            course_credit: float,
            program: str,
            faculty: str,
            instructor_initial: str,
            instructor_name: str,
            section: str,
            total_seats: int,
            seats_booked: int,
            seats_remaining: int,
            schedule: Schedule,
    ):
        self.course_code: str = course_code
        self.course_title: str = course_title
        self.course_credit: float = course_credit
        self.program: str = program
        self.faculty: str = faculty
        self.instructor_initial: str = instructor_initial
        self.instructor_name: str = instructor_name
        self.section: str = section
        self.total_seats: int = total_seats
        self.seats_booked: int = seats_booked
        self.seats_remaining: int = seats_remaining
        self.schedule: Schedule = schedule

    def __str__(self) -> str:
        return f"Course Code: {self.course_code}\n" \
            f"Course Title: {self.course_title}\n" \
            f"Course Credit: {self.course_credit}\n" \
            f"Program: {self.program}\n" \
            f"Faculty: {self.faculty}\n" \
            f"Instructor Initial: {self.instructor_initial}\n" \
            f"Instructor Name: {self.instructor_name}\n" \
            f"Section: {self.section}\n" \
            f"Total Seats: {self.total_seats}\n" \
            f"Seats Booked: {self.seats_booked}\n" \
            f"Seats Remaining: {self.seats_remaining}\n" \
            f"Schedule: {self.schedule}"
