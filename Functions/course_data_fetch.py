from datetime import datetime

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

    exam_day = ""
    exam_start_time = ""
    exam_end_time = ""
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
        elif len(exams) == 2:
            exam = exams[0].strip()
            exam_day = exam.split("(")[0].strip()
            exam_time = exams[1].strip()
            exam_time = exam_time.split("(")[1].strip()
            exam_start_time = exam_time.split("-")[0]
            exam_end_time = exam_time.split("-")[1]
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


def get_courses_user(main, signal) -> list[Course]:
    course_list = []
    session = main.session

    signal.emit("Getting available courses")
    try:
        response = session.get(
            f"https://usis.bracu.ac.bd/academia/studentCourse/"
            f"showCourseStatusList?query=&academiaSession={
                main.working_session_id}"
            f"&_search=false&nd=1711516270344&rows=-1&page=1&sidx=id&sord=desc")
    except Exception as e:
        signal.emit(f"USIS connection failed\nError: {e}")
        return course_list

    signal.emit("Converting Seat Status data to JSON")
    seats_json = response.json()
    seats_data = seats_json["rows"]

    signal.emit("Getting Classroom data")
    tr_data = get_response(session, signal)
    # This line is repeated on purpose to make sure the updated data is fetched
    tr_data = get_response(session, signal)
    if tr_data is None:
        return course_list

    signal.emit("Getting Course data")
    course_code_title_map = get_course_code_title_map(signal)

    url = (f"https://usis.bracu.ac.bd/academia/academicSection/listAcademicSectionWithSchedule?"
           f"academiaSession={
               main.working_session_id}&_search=false&nd=1711519391647&"
           f"rows=-1&page=1&sidx=course_code&sord=asc")
    exam_dict = get_exam_data(signal, session, url)
    if exam_dict is None:
        return course_list

    total_courses = len(seats_data)
    for idx, crs in enumerate(seats_data):
        try:
            course = crs["cell"]
            course_code = course[2]
            section = course[7]

            signal.emit(
                f"[{idx + 1}/{total_courses}] Getting Basic Data for {course_code} Section[{section}]")
            course_title = course_code_title_map.get(course_code, "")
            program = course[4]
            instructor_initial = course[5]
            try:
                course_credit = float(course[6])
            except ValueError:
                course_credit: float = 0.0
            try:
                total_seats = int(course[8])
            except ValueError:
                total_seats: int = 0
            try:
                seats_booked = int(course[9])
            except ValueError:
                seats_booked: int = 0
            try:
                seats_remaining: int = int(course[10])
            except ValueError:
                seats_remaining = 0
            tr: PageElement | None = None
            for tr_course in tr_data:
                td_elements = tr_course.find_all("td")
                if td_elements[1].get_text(strip=True) == course_code and td_elements[5].get_text(
                        strip=True) == section:
                    tr = tr_course
                    break
            if tr is not None:
                (day_1, day_2, lab_1, lab_2, exam_date, exam_day, exam_start_time, exam_end_time, faculty,
                 instructor_name) = get_schedule_data(idx, total_courses, course_code, section, tr, exam_dict, signal)
                course_object = create_course_object(signal, idx, total_courses, course_code, course_title,
                                                     course_credit, program, faculty, instructor_initial,
                                                     instructor_name, section, total_seats, seats_booked,
                                                     seats_remaining, day_1, day_2, lab_1, lab_2, exam_date, exam_day,
                                                     exam_start_time, exam_end_time)
                course_list.append(course_object)
            else:
                # Need some work done here
                pass
        except Exception as e:
            signal.emit(f"Error: {e}")
            continue
    signal.emit("Data parsing complete")
    return course_list
