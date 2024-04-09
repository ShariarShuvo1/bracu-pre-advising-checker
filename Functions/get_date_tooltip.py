from Entity.Course import Course


def get_date_tooltip(course: Course) -> str:
    tooltip: str = ""
    if course.schedule.class_day_1:
        tooltip += (f"Class Day 1: {course.schedule.class_day_1} "
                    f"({course.schedule.class_day_1_start_time} - "
                    f"{course.schedule.class_day_1_end_time}) "
                    f"[{course.schedule.class_day_1_room}]")

    if course.schedule.class_day_2:
        tooltip += (f"\nClass Day 2: {course.schedule.class_day_2} "
                    f"({course.schedule.class_day_2_start_time} - "
                    f"{course.schedule.class_day_2_end_time}) "
                    f"[{course.schedule.class_day_2_room}]")

    if course.schedule.lab_day_1:
        if course.schedule.class_day_1:
            room = f"[{course.schedule.lab_day_1_room}]" if course.schedule.lab_day_1_room else ""
            tooltip += (f"\n\nLab Day 1: {course.schedule.lab_day_1} "
                        f"({course.schedule.lab_day_1_start_time} - "
                        f"{course.schedule.lab_day_1_end_time}) "
                        f"{room}")
        else:
            room = f"[{course.schedule.lab_day_1_room}]" if course.schedule.lab_day_1_room else ""
            tooltip += (f"Lab Day 1: {course.schedule.lab_day_1} "
                        f"({course.schedule.lab_day_1_start_time} - "
                        f"{course.schedule.lab_day_1_end_time}) "
                        f"{room}")

    if course.schedule.lab_day_2:
        room = f"[{course.schedule.lab_day_2_room}]" if course.schedule.lab_day_2_room else ""
        tooltip += (f"\nLab Day 2: {course.schedule.lab_day_2} "
                    f"({course.schedule.lab_day_2_start_time} - "
                    f"{course.schedule.lab_day_2_end_time}) "
                    f"{room}")

    if course.schedule.exam_day:
        tooltip += f"\n\nExam Day: {course.schedule.exam_day}"
        tooltip += (f"\nExam Date: {course.schedule.exam_date} "
                    f"({course.schedule.exam_start_time} - "
                    f"{course.schedule.exam_end_time})")

    return tooltip
