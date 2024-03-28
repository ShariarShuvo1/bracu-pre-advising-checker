from datetime import datetime
from typing import Union, Tuple, Dict, Optional

from bs4 import BeautifulSoup, ResultSet, PageElement

from Constants.course_details import course_details
from Constants.day_data import day_checker, day_list
from Entity.Course import Course
from Entity.Schedule import Schedule


def get_course_code_title_map(signal) -> dict:
    signal.emit("Mapping course code to course title")
    course_code_title_map = {
        course_dict["cell"][2]: course_dict["cell"][3] for course_dict in course_details["rows"]}
    return course_code_title_map


def get_response(session, signal) -> ResultSet | None:
    try:
        response = session.get(
            "https://admissions.bracu.ac.bd/academia/admissionRequirement/getAvailableSeatStatus")
    except Exception as e:
        signal.emit(f"USIS connection failed\nError: {e}")
        return None

    signal.emit("Parsing data from HTML")
    soup = BeautifulSoup(response.text, "html.parser")
    tr_data = soup.find_all("tr")
    return tr_data


def get_exam_data(signal, session, url) -> dict | None:
    signal.emit("Getting exam dates")
    try:
        exam_response = session.get(
            f"{url}")
    except Exception as e:
        if "gitfront" in url:
            signal.emit(f"GitFront connection failed\nError: {e}")
        else:
            signal.emit(f"USIS connection failed\nError: {e}")
        return None

    signal.emit("Converting data to JSON")
    exam_data = exam_response.json()
    exam_data = exam_data["rows"]
    exam_dict = {}
    signal.emit("Mapping exam data")
    for exam in exam_data:
        key = (exam["cell"][1], exam["cell"][3])
        if key not in exam_dict:
            exam_dict[key] = (exam["cell"][6], exam["cell"][7],
                              exam["cell"][9], exam["cell"][10])
    return exam_dict


def get_schedule_data(idx, total_courses, course_code, section, tr, exam_dict, signal) -> list:
    signal.emit(
        f"[{idx + 1}/{total_courses}] Getting Class Schedule for {course_code} Section[{section}]")
    times = tr.find_all("td")[6].get_text(strip=True)
    times = times.split(")")
    for time in reversed(times):
        if len(time) < 2:
            times.remove(time)

    schedules = []
    for time in times:
        time = time.strip()
        time = time.split("(")
        day = day_checker.get(time[0])
        datas = time[1].split("-")
        if len(datas) == 3:
            start_time, end_time, room = datas
        else:
            start_time, end_time, room_1, room_2 = datas
            room = room_1 + " " + room_2
        schedules.append({
            "day": day,
            "start_time": start_time,
            "end_time": end_time,
            "room": room
        })

    day_1, day_2, lab_1, lab_2 = None, None, None, None
    for schedule in schedules:
        if schedule["room"].upper().endswith("L"):
            if lab_1:
                lab_2 = schedule
            else:
                lab_1 = schedule
        else:
            if day_1:
                day_2 = schedule
            else:
                day_1 = schedule

    if day_1 and day_2:
        if day_list.index(day_1["day"]) > day_list.index(day_2["day"]):
            day_1, day_2 = day_2, day_1
        if day_list.index(day_1["day"]) == day_list.index(day_2["day"]):
            if (datetime.strptime(day_1["start_time"], "%I:%M %p") >
                    datetime.strptime(day_2["start_time"], "%I:%M %p")):
                day_1, day_2 = day_2, day_1

    if lab_1 and lab_2:
        if day_list.index(lab_1["day"]) > day_list.index(lab_2["day"]):
            lab_1, lab_2 = lab_2, lab_1
        if day_list.index(lab_1["day"]) == day_list.index(lab_2["day"]):
            if (datetime.strptime(lab_1["start_time"], "%I:%M %p") >
                    datetime.strptime(lab_2["start_time"], "%I:%M %p")):
                lab_1, lab_2 = lab_2, lab_1
    signal.emit(
        f"[{idx + 1}/{total_courses}] Getting Exam Schedule for {course_code} Section[{section}]")
    faculty, instructor_name, exam_date, exam_string = exam_dict.get(
        (course_code, section), ("", "", "", ""))
    if exam_string is None:
        exam_string = ""
    if faculty is None:
        faculty = ""
    if instructor_name is None:
        instructor_name = ""
    if exam_date is None:
        exam_date = ""
    exam_day, exam_start_time, exam_end_time = get_exam_days(exam_string)
    return [day_1, day_2, lab_1, lab_2, exam_date, exam_day, exam_start_time, exam_end_time, faculty, instructor_name]


def create_course_object(signal, idx, total_courses, course_code, course_title, course_credit,
                         program, faculty, instructor_initial, instructor_name, section,
                         total_seats, seats_booked, seats_remaining, day_1, day_2, lab_1, lab_2,
                         exam_date, exam_day, exam_start_time, exam_end_time):
    signal.emit(
        f"[{idx + 1}/{total_courses}] Creating Schedule Object for {course_code} Section[{section}]")
    schedule_object = Schedule(
        class_day_1=day_1["day"] if day_1 else None,
        class_day_1_start_time=day_1["start_time"] if day_1 else None,
        class_day_1_end_time=day_1["end_time"] if day_1 else None,
        class_day_1_room=day_1["room"] if day_1 else None,
        class_day_2=day_2["day"] if day_2 else None,
        class_day_2_start_time=day_2["start_time"] if day_2 else None,
        class_day_2_end_time=day_2["end_time"] if day_2 else None,
        class_day_2_room=day_2["room"] if day_2 else None,
        lab_day_1=lab_1["day"] if lab_1 else None,
        lab_day_1_start_time=lab_1["start_time"] if lab_1 else None,
        lab_day_1_end_time=lab_1["end_time"] if lab_1 else None,
        lab_day_1_room=lab_1["room"] if lab_1 else None,
        lab_day_2=lab_2["day"] if lab_2 else None,
        lab_day_2_start_time=lab_2["start_time"] if lab_2 else None,
        lab_day_2_end_time=lab_2["end_time"] if lab_2 else None,
        lab_day_2_room=lab_2["room"] if lab_2 else None,
        exam_date=exam_date if exam_date else None,
        exam_day=exam_day if exam_day else None,
        exam_start_time=exam_start_time if exam_start_time else None,
        exam_end_time=exam_end_time if exam_end_time else None,
    )

    signal.emit(
        f"[{idx + 1}/{total_courses}] Creating Course Object for {course_code} Section[{section}]")
    course_object = Course(
        course_code=course_code,
        course_title=course_title,
        course_credit=course_credit,
        program=program,
        faculty=faculty,
        instructor_initial=instructor_initial,
        instructor_name=instructor_name,
        section=section,
        total_seats=total_seats,
        seats_booked=seats_booked,
        seats_remaining=seats_remaining,
        schedule=schedule_object
    )
    return course_object


def get_courses_guest(main, signal) -> list[Course]:
    course_list: list[Course] = []
    session = main.session

    signal.emit("Getting available courses")
    tr_data = get_response(session, signal)
    # This line is repeated on purpose to make sure the updated data is fetched
    tr_data = get_response(session, signal)
    if tr_data is None:
        return course_list

    signal.emit("Getting Course data")
    course_code_title_map = get_course_code_title_map(signal)

    url = "https://gitfront.io/r/user-6015890/N6zXuFDpUWFu/data-sharing/raw/usisCurrentData.json"
    exam_dict = get_exam_data(signal, session, url)
    if exam_dict is None:
        return course_list

    total_courses = len(tr_data)
    for idx, tr in enumerate(tr_data):
        try:
            course_code = tr.find_all("td")[1].get_text(strip=True)
            section = tr.find_all("td")[5].get_text(strip=True)

            signal.emit(
                f"[{idx + 1}/{total_courses}] Getting Basic Data for {course_code} Section[{section}]")
            course_title = course_code_title_map.get(course_code, "")
            program = tr.find_all("td")[2].get_text(strip=True)
            instructor_initial = tr.find_all("td")[3].get_text(strip=True)
            course_credit = float(tr.find_all("td")[4].get_text(strip=True))
            total_seats = int(tr.find_all("td")[7].get_text(strip=True))
            seats_booked = int(tr.find_all("td")[8].get_text(strip=True))
            seats_remaining = int(tr.find_all("td")[9].get_text(strip=True))

            (day_1, day_2, lab_1, lab_2, exam_date, exam_day, exam_start_time, exam_end_time, faculty,
             instructor_name) = get_schedule_data(idx, total_courses, course_code, section, tr, exam_dict, signal)

            course_object = create_course_object(signal, idx, total_courses, course_code, course_title, course_credit,
                                                 program, faculty, instructor_initial, instructor_name, section,
                                                 total_seats, seats_booked, seats_remaining, day_1, day_2, lab_1, lab_2,
                                                 exam_date, exam_day, exam_start_time, exam_end_time)
            course_list.append(course_object)
        except Exception as e:
            signal.emit(f"Error: {e}")
            continue
    signal.emit("Data parsing complete")
    return course_list


def get_usis_json_data(session, url, signal, message):
    signal.emit(f"Getting {message}")
    try:
        response = session.get(url)
    except Exception as e:
        signal.emit(f"USIS connection failed\nError: {e}")
        return None
    signal.emit(f"Converting {message} to JSON")
    json_data = response.json()
    return json_data["rows"]


def convert_seats_data_map(seats_data) -> Dict[Tuple[str, str], Dict[str, Union[str, float, int]]]:
    seats_map: Dict[Tuple[str, str], Dict[str, Union[str, float, int]]] = {}
    for seat in seats_data:
        data = seat["cell"]
        try:
            course_credit = float(data[6])
        except ValueError:
            course_credit = 0.0
        try:
            total_seats = int(data[8])
        except ValueError:
            total_seats: int = 0
        try:
            seats_booked = int(data[9])
        except ValueError:
            seats_booked: int = 0
        try:
            seats_remaining: int = int(data[10])
        except ValueError:
            seats_remaining = 0
        seats_map[(data[2], data[7])] = {
            "program": data[4],
            "instructor_initial": data[5],
            "course_credit": course_credit,
            "total_seats": total_seats,
            "seats_booked": seats_booked,
            "seats_remaining": seats_remaining
        }
    return seats_map


def convert_course_data_map(course_data) -> Dict[str, str]:
    course_name_map: Dict[str, str] = {}
    for course in course_data:
        data = course["cell"]
        course_name_map[data[2]] = data[3]
    return course_name_map


def get_exam_days(exam_string) -> Optional[Tuple[str, str, str]]:
    if len(exam_string) > 1:
        exams = exam_string.split(")")
        for exam in reversed(exams):
            if len(exam) < 2:
                exams.remove(exam)

        if len(exams) == 1:
            exam = exams[0].strip()
            exam_day = exam.split("(")[0].strip()
            exam_time = exam.split("(")[1].strip()
            exam_start_time = exam_time.split("-")[0].strip()
            exam_end_time = exam_time.split("-")[1].strip()
            return exam_day, exam_start_time, exam_end_time
        elif len(exams) == 2:
            exam = exams[0].strip()
            exam_day = exam.split("(")[0].strip()
            exam_time = exams[1].strip()
            exam_time = exam_time.split("(")[1].strip()
            exam_start_time = exam_time.split("-")[0]
            exam_end_time = exam_time.split("-")[1]
            return exam_day, exam_start_time, exam_end_time
    return "", "", ""


def convert_exam_data_map(exam_data) -> Dict[Tuple[str, str, int], Dict[str, Union[str, None]]]:
    exam_map: Dict[Tuple[str, str, int], Dict[str, Union[str, None]]] = {}
    for exam_element in exam_data:
        data = exam_element["cell"]
        course_code = data[1]
        course_title = data[2]
        section = data[3]
        faculty = data[6]
        instructor_name = data[7]
        exam_date = data[9]
        exam_string = data[10]
        if not exam_string:
            exam_string = ""
        exam_day, exam_start_time, exam_end_time = get_exam_days(exam_string)

        already_exists = (course_code, section, 1) in exam_map
        if already_exists:
            dict_key = (course_code, section, 2)
        else:
            dict_key = (course_code, section, 1)

        exam_map[dict_key] = {
            "course_title": course_title,
            "faculty": faculty,
            "instructor_name": instructor_name,
            "exam_date": exam_date,
            "exam_day": exam_day,
            "exam_start_time": exam_start_time,
            "exam_end_time": exam_end_time,
            "Sunday": data[11],
            "Monday": data[12],
            "Tuesday": data[13],
            "Wednesday": data[14],
            "Thursday": data[15],
            "Friday": data[16],
            "Saturday": data[17]
        }
    return exam_map

    # for key, value in class_schedule_dict.items():
    #     is_lab = value["room"].upper().endswith("L")
    #     schedule_type = "lab" if is_lab else "day"
    #     schedule_key = "lab_" if is_lab else "day_"
    #
    #     schedule = {
    #         "day": value["day"],
    #         "start_time": value["start_time"],
    #         "end_time": value["end_time"],
    #         "room": value["room"]
    #     }
    #
    #     existing_schedule = class_schedule_map.get((key[0], key[1]), {})
    #     existing_key = f"{schedule_key}2" if existing_schedule.get(f"{schedule_key}1") else f"{schedule_key}1"
    #
    #     class_schedule_map[(key[0], key[1])] = {existing_key: schedule}


def convert_class_schedule_data_map(class_schedule_data) -> Dict[Tuple[str, str], Dict[str, Dict[str, str]]]:
    class_schedule_dict: Dict[Tuple[str, str, int], Dict[str, str]] = {}
    for class_schedule in class_schedule_data:
        data = class_schedule["cell"]
        course_code = data[2]
        section = data[4]

        already_exists = (course_code, section, 1) in class_schedule_dict
        if already_exists:
            dict_key = (course_code, section, 2)
        else:
            dict_key = (course_code, section, 1)

        class_schedule_dict[dict_key] = {
            "day": data[5],
            "start_time": data[6],
            "end_time": data[7],
            "room": data[8]
        }

    class_schedule_map: Dict[Tuple[str, str], Dict[str, Dict[str, str]]] = {}
    for key, value in class_schedule_dict.items():
        is_lab = value["room"].upper().endswith("L")
        if (key[0], key[1]) not in class_schedule_map:
            class_schedule_map[(key[0], key[1])] = {}
        if is_lab:
            room = value["room"]
            if room and '-' in room:
                room1, room2 = room.split("-")
                room = room1 + " " + room2
            lab = {
                "day": value["day"],
                "start_time": value["start_time"],
                "end_time": value["end_time"],
                "room": room
            }
            if class_schedule_map.get((key[0], key[1])):
                if class_schedule_map[(key[0], key[1])].get("lab_1"):
                    class_schedule_map[(key[0], key[1])]["lab_2"] = lab
                else:
                    class_schedule_map[(key[0], key[1])]["lab_1"] = lab
            else:
                class_schedule_map[(key[0], key[1])]["lab_1"] = lab
        else:
            room = value["room"]
            if room and '-' in room:
                room1, room2 = room.split("-")
                room = room1 + " " + room2
            day = {
                "day": value["day"],
                "start_time": value["start_time"],
                "end_time": value["end_time"],
                "room": room
            }
            if class_schedule_map.get((key[0], key[1])):
                if class_schedule_map[(key[0], key[1])].get("day_1"):
                    class_schedule_map[(key[0], key[1])]["day_2"] = day
                else:
                    class_schedule_map[(key[0], key[1])]["day_1"] = day
            else:
                class_schedule_map[(key[0], key[1])]["day_1"] = day
    return class_schedule_map


def combine_exam_map_with_class_schedule_map(
        exam_map: Dict[Tuple[str, str, int], Dict[str, Union[str, None]]],
        class_schedule_map: Dict[Tuple[str, str], Dict[str, Dict[str, str]]]
):
    schedule_map = dict()
    for key, value in class_schedule_map.items():
        course_code = key[0]
        section = key[1]
        is_lab_1 = value.get("lab_1") is not None
        is_lab_2 = value.get("lab_2") is not None
        exam_1 = exam_map.get((course_code, section, 1))
        exam_2 = exam_map.get((course_code, section, 2))
        if not exam_1 and not exam_2:
            continue
        course_title = exam_1["course_title"]
        faculty = exam_1["faculty"]
        instructor_name = exam_1["instructor_name"]
        class_day_1: str | None = None
        class_day_1_start_time: str | None = None
        class_day_1_end_time: str | None = None
        class_day_1_room: str | None = None
        class_day_2: str | None = None
        class_day_2_start_time: str | None = None
        class_day_2_end_time: str | None = None
        class_day_2_room: str | None = None
        lab_day_1: str | None = None
        lab_day_1_start_time: str | None = None
        lab_day_1_end_time: str | None = None
        lab_day_1_room: str | None = None
        lab_day_2: str | None = None
        lab_day_2_start_time: str | None = None
        lab_day_2_end_time: str | None = None
        lab_day_2_room: str | None = None
        exam_date: str | None = None
        exam_day: str | None = None
        exam_start_time: str | None = None
        exam_end_time: str | None = None
        if (exam := exam_1 or exam_2) and exam.get("exam_day"):
            exam_day = exam["exam_day"]
            exam_date = exam["exam_date"]
            exam_start_time = exam["exam_start_time"]
            exam_end_time = exam["exam_end_time"]
        if is_lab_1:
            if lab := value.get("lab_1"):
                lab_day_1 = lab["day"]
                lab_day_1_start_time = lab["start_time"]
                lab_day_1_end_time = lab["end_time"]
                lab_day_1_room = lab["room"]
        if is_lab_2:
            if lab := value.get("lab_2"):
                lab_day_2 = lab["day"]
                lab_day_2_start_time = lab["start_time"]
                lab_day_2_end_time = lab["end_time"]
                lab_day_2_room = lab["room"]
        is_class_1 = value.get("day_1") is not None
        is_class_2 = value.get("day_2") is not None

        if is_class_1:
            if day := value.get("day_1"):
                class_day_1 = day["day"]
                class_day_1_start_time = day["start_time"]
                class_day_1_end_time = day["end_time"]
                class_day_1_room = day["room"]
        if is_class_2:
            if day := value.get("day_2"):
                class_day_2 = day["day"]
                class_day_2_start_time = day["start_time"]
                class_day_2_end_time = day["end_time"]
                class_day_2_room = day["room"]
        lab_data = exam_2 if exam_1.get("exam_day") else exam_1
        if lab_data:
            count_of_lab_day = {}
            for k, v in lab_data.items():
                if k in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday") and v:
                    count_of_lab_day[k] = v
            if len(count_of_lab_day) == 1:
                lab_day_1 = list(count_of_lab_day.keys())[0]
                lab_day_string = count_of_lab_day[lab_day_1]
                lab_day_string = lab_day_string.split("-")
                if len(lab_day_string) == 3:
                    lab_day_2 = list(count_of_lab_day.keys())[0]
                    lab_day_1_start_time = lab_day_string[0].strip()
                    lab_day_2_end_time = lab_day_string[2].strip()
                    middle_part = lab_day_string[1].strip()
                    middle_part = middle_part.split("M")
                    lab_day_1_end_time = middle_part[0].strip() + "M"
                    lab_day_2_start_time = middle_part[1].strip() + "M"
                else:
                    lab_day_1_start_time = lab_day_string[0].strip()
                    lab_day_1_end_time = lab_day_string[1].strip()
            else:
                lab_day_1 = list(count_of_lab_day.keys())[0]
                lab_day_2 = list(count_of_lab_day.keys())[1]
                lab_day_1_string = count_of_lab_day[lab_day_1]
                lab_day_2_string = count_of_lab_day[lab_day_2]
                lab_day_1_string = lab_day_1_string.split("-")
                lab_day_2_string = lab_day_2_string.split("-")
                lab_day_1_start_time, lab_day_1_end_time = lab_day_1_string[0].strip(), lab_day_1_string[1].strip()
                lab_day_2_start_time, lab_day_2_end_time = lab_day_2_string[0].strip(), lab_day_2_string[1].strip()
        if lab_day_1 and lab_day_2:
            if day_list.index(lab_day_1) > day_list.index(lab_day_2):
                lab_day_1, lab_day_2 = lab_day_2, lab_day_1
                lab_day_1_start_time, lab_day_2_start_time = lab_day_2_start_time, lab_day_1_start_time
                lab_day_1_end_time, lab_day_2_end_time = lab_day_2_end_time, lab_day_1_end_time
                lab_day_1_room, lab_day_2_room = lab_day_2_room, lab_day_1_room
            if day_list.index(lab_day_1) == day_list.index(lab_day_2):
                if (datetime.strptime(lab_day_1_start_time, "%I:%M %p") >
                        datetime.strptime(lab_day_2_start_time, "%I:%M %p")):
                    lab_day_1, lab_day_2 = lab_day_2, lab_day_1
                lab_day_1_start_time, lab_day_2_start_time = lab_day_2_start_time, lab_day_1_start_time
                lab_day_1_end_time, lab_day_2_end_time = lab_day_2_end_time, lab_day_1_end_time
                lab_day_1_room, lab_day_2_room = lab_day_2_room, lab_day_1_room
        if class_day_1 and class_day_2:
            if day_list.index(class_day_1) > day_list.index(class_day_2):
                class_day_1, class_day_2 = class_day_2, class_day_1
                class_day_1_start_time, class_day_2_start_time = class_day_2_start_time, class_day_1_start_time
                class_day_1_end_time, class_day_2_end_time = class_day_2_end_time, class_day_1_end_time
                class_day_1_room, class_day_2_room = class_day_2_room, class_day_1_room
            if day_list.index(class_day_1) == day_list.index(class_day_2):
                if (datetime.strptime(class_day_1_start_time, "%I:%M %p") >
                        datetime.strptime(class_day_2_start_time, "%I:%M %p")):
                    class_day_1, class_day_2 = class_day_2, class_day_1
                class_day_1_start_time, class_day_2_start_time = class_day_2_start_time, class_day_1_start_time
                class_day_1_end_time, class_day_2_end_time = class_day_2_end_time, class_day_1_end_time
                class_day_1_room, class_day_2_room = class_day_2_room, class_day_1_room
        schedule_map[(course_code, section)] = {
            "course_title": course_title,
            "faculty": faculty,
            "instructor_name": instructor_name,
            "class_day_1": class_day_1,
            "class_day_1_start_time": class_day_1_start_time,
            "class_day_1_end_time": class_day_1_end_time,
            "class_day_1_room": class_day_1_room,
            "class_day_2": class_day_2,
            "class_day_2_start_time": class_day_2_start_time,
            "class_day_2_end_time": class_day_2_end_time,
            "class_day_2_room": class_day_2_room,
            "lab_day_1": lab_day_1,
            "lab_day_1_start_time": lab_day_1_start_time,
            "lab_day_1_end_time": lab_day_1_end_time,
            "lab_day_1_room": lab_day_1_room,
            "lab_day_2": lab_day_2,
            "lab_day_2_start_time": lab_day_2_start_time,
            "lab_day_2_end_time": lab_day_2_end_time,
            "lab_day_2_room": lab_day_2_room,
            "exam_date": exam_date,
            "exam_day": exam_day,
            "exam_start_time": exam_start_time,
            "exam_end_time": exam_end_time,
        }
    return schedule_map


def get_courses_user(main, signal) -> list[Course]:
    course_list: list[Course] = []
    session = main.session

    seats_data = get_usis_json_data(session, f"https://usis.bracu.ac.bd/academia/"
                                             f"studentCourse/showCourseStatusList?query"
                                             f"=&academiaSession={main.working_session_id}"
                                             f"&_search=false&nd=1711516270344&rows=-1&page="
                                             f"1&sidx=id&sord=desc", signal, "available courses")
    if seats_data is None:
        return course_list
    signal.emit("Converting available courses to HashMap")
    seats_map: Dict[Tuple[str, str], Dict[str, Union[str, float, int]]] = convert_seats_data_map(seats_data)
    exam_data = get_usis_json_data(session, f"https://usis.bracu.ac.bd/academia/ac"
                                            f"ademicSection/listAcademicSectionWithSche"
                                            f"dule?academiaSession={main.working_session_id}"
                                            f"&_search=false&nd=1711519391647&rows=-1&page=1&"
                                            f"sidx=course_code&sord=asc", signal, "exam dates")
    if exam_data is None:
        return course_list
    signal.emit("Mapping exam data to HashMap")
    exam_map: Dict[Tuple[str, str, int], Dict[str, Union[str, None]]] = convert_exam_data_map(exam_data)

    class_schedule_data = get_usis_json_data(session, f"https://usis.bracu.ac.bd/academia/student"
                                                      f"Course/showClassScheduleInTabularFormatInGrid?"
                                                      f"query=&academiaSession={main.working_session_id}"
                                                      f"&_search=false&nd=1711567882232&rows=-1&page=1&si"
                                                      f"dx=course_code&sord=asc", signal, "class schedules")
    if class_schedule_data is None:
        return course_list
    signal.emit("Mapping class schedule data to HashMap")
    class_schedule_map: Dict[Tuple[str, str], Dict[str, Dict[str, str]]] = (
        convert_class_schedule_data_map(class_schedule_data))

    signal.emit("Combining exam data with class schedule data")
    schedule_map = combine_exam_map_with_class_schedule_map(exam_map, class_schedule_map)

    total_courses = len(seats_map)
    for idx, (course_code, section) in enumerate(seats_map.keys()):
        try:
            signal.emit(
                f"[{idx + 1}/{total_courses}] Getting Basic Data for {course_code} Section[{section}]")
            course_data = seats_map[(course_code, section)]
            course_title = course_data["program"]
            program = course_data["program"]
            instructor_initial = course_data["instructor_initial"]
            course_credit = course_data["course_credit"]
            total_seats = course_data["total_seats"]
            seats_booked = course_data["seats_booked"]
            seats_remaining = course_data["seats_remaining"]

            signal.emit(
                f"[{idx + 1}/{total_courses}] Getting Schedule Data for {course_code} Section[{section}]")
            schedule_data = schedule_map.get((course_code, section), {})
            class_day_1 = schedule_data.get("class_day_1")
            class_day_1_start_time = schedule_data.get("class_day_1_start_time")
            class_day_1_end_time = schedule_data.get("class_day_1_end_time")
            class_day_1_room = schedule_data.get("class_day_1_room")
            class_day_2 = schedule_data.get("class_day_2")
            class_day_2_start_time = schedule_data.get("class_day_2_start_time")
            class_day_2_end_time = schedule_data.get("class_day_2_end_time")
            class_day_2_room = schedule_data.get("class_day_2_room")
            lab_day_1 = schedule_data.get("lab_day_1")
            lab_day_1_start_time = schedule_data.get("lab_day_1_start_time")
            lab_day_1_end_time = schedule_data.get("lab_day_1_end_time")
            lab_day_1_room = schedule_data.get("lab_day_1_room")
            lab_day_2 = schedule_data.get("lab_day_2")
            lab_day_2_start_time = schedule_data.get("lab_day_2_start_time")
            lab_day_2_end_time = schedule_data.get("lab_day_2_end_time")
            lab_day_2_room = schedule_data.get("lab_day_2_room")

            exam_date = schedule_data.get("exam_date")
            exam_day = schedule_data.get("exam_day")
            exam_start_time = schedule_data.get("exam_start_time")
            exam_end_time = schedule_data.get("exam_end_time")
            faculty = schedule_data.get("faculty")
            instructor_name = schedule_data.get("instructor_name")

            signal.emit(
                f"[{idx + 1}/{total_courses}] Creating Schedule Object for {course_code} Section[{section}]")
            schedule = Schedule(
                class_day_1=class_day_1,
                class_day_1_start_time=class_day_1_start_time,
                class_day_1_end_time=class_day_1_end_time,
                class_day_1_room=class_day_1_room,
                class_day_2=class_day_2,
                class_day_2_start_time=class_day_2_start_time,
                class_day_2_end_time=class_day_2_end_time,
                class_day_2_room=class_day_2_room,
                lab_day_1=lab_day_1,
                lab_day_1_start_time=lab_day_1_start_time,
                lab_day_1_end_time=lab_day_1_end_time,
                lab_day_1_room=lab_day_1_room,
                lab_day_2=lab_day_2,
                lab_day_2_start_time=lab_day_2_start_time,
                lab_day_2_end_time=lab_day_2_end_time,
                lab_day_2_room=lab_day_2_room,
                exam_date=exam_date,
                exam_day=exam_day,
                exam_start_time=exam_start_time,
                exam_end_time=exam_end_time
            )

            signal.emit(
                f"[{idx + 1}/{total_courses}] Creating Course Object for {course_code} Section[{section}]")

            course = Course(
                course_code=course_code,
                course_title=course_title,
                course_credit=course_credit,
                program=program,
                faculty=faculty,
                instructor_initial=instructor_initial,
                instructor_name=instructor_name,
                section=section,
                total_seats=total_seats,
                seats_booked=seats_booked,
                seats_remaining=seats_remaining,
                schedule=schedule
            )
            course_list.append(course)
        except Exception as e:
            signal.emit(f"Error: {e}")
            continue
    signal.emit("Data parsing complete")
    return course_list
