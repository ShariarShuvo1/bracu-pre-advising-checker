class Schedule:
    def __init__(
            self,
            class_day_1=None,
            class_day_1_start_time=None,
            class_day_1_end_time=None,
            class_day_1_room=None,
            class_day_2=None,
            class_day_2_start_time=None,
            class_day_2_end_time=None,
            class_day_2_room=None,
            lab_day_1=None,
            lab_day_1_start_time=None,
            lab_day_1_end_time=None,
            lab_day_1_room=None,
            lab_day_2=None,
            lab_day_2_start_time=None,
            lab_day_2_end_time=None,
            lab_day_2_room=None,
            exam_date=None,
            exam_day=None,
            exam_start_time=None,
            exam_end_time=None,
    ):
        self.class_day_1: str = class_day_1
        self.class_day_1_start_time: str = class_day_1_start_time
        self.class_day_1_end_time: str = class_day_1_end_time
        self.class_day_1_room: str = class_day_1_room
        self.class_day_2: str = class_day_2
        self.class_day_2_start_time: str = class_day_2_start_time
        self.class_day_2_end_time: str = class_day_2_end_time
        self.class_day_2_room: str = class_day_2_room
        self.lab_day_1: str = lab_day_1
        self.lab_day_1_start_time: str = lab_day_1_start_time
        self.lab_day_1_end_time: str = lab_day_1_end_time
        self.lab_day_1_room: str = lab_day_1_room
        self.lab_day_2: str = lab_day_2
        self.lab_day_2_start_time: str = lab_day_2_start_time
        self.lab_day_2_end_time: str = lab_day_2_end_time
        self.lab_day_2_room: str = lab_day_2_room
        self.exam_date: str = exam_date
        self.exam_day: str = exam_day
        self.exam_start_time: str = exam_start_time
        self.exam_end_time: str = exam_end_time

    def __str__(self) -> str:
        return (f"Schedule(class_day_1={self.class_day_1}, "
                f"class_day_1_start_time={self.class_day_1_start_time}, "
                f"class_day_1_end_time={self.class_day_1_end_time}, "
                f"class_day_1_room={self.class_day_1_room}, "
                f"class_day_2={self.class_day_2}, "
                f"class_day_2_start_time={self.class_day_2_start_time}, "
                f"class_day_2_end_time={self.class_day_2_end_time}, "
                f"class_day_2_room={self.class_day_2_room}, "
                f"lab_day_1={self.lab_day_1}, "
                f"lab_day_1_start_time={self.lab_day_1_start_time}, "
                f"lab_day_1_end_time={self.lab_day_1_end_time}, "
                f"lab_day_1_room={self.lab_day_1_room}, "
                f"lab_day_2={self.lab_day_2}, "
                f"lab_day_2_start_time={self.lab_day_2_start_time}, "
                f"lab_day_2_end_time={self.lab_day_2_end_time}, "
                f"lab_day_2_room={self.lab_day_2_room}, "
                f"exam_date={self.exam_date}, "
                f"exam_day={self.exam_day}, "
                f"exam_start_time={self.exam_start_time}, "
                f"exam_end_time={self.exam_end_time})")
