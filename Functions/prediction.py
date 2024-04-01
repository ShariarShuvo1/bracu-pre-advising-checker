from datetime import datetime

from bs4 import BeautifulSoup

from Settings.SettingsData import set_working_session_id, set_current_session_id, set_prediction_data, \
    get_prediction_data, set_current_semester_name, set_next_semester_name


def academic_session_data(main, session_id, signal):
    signal.emit(f"Checking session: {session_id}")
    url = (f"https://usis.bracu.ac.bd/academia/studentCourse/showCourseStatusList?query=&academiaSession="
           f"{session_id}&_search=false&nd=1711935207096&rows=-1&page=1&sidx=id&sord=desc")
    session = main.session
    try:
        signal.emit(f"Data fetching for session: {session_id}")
        response = session.get(url)
        data = response.json()
        if data["records"] >= 2:
            return data["rows"]
        else:
            return None
    except Exception as e:
        signal.emit(f"Error: {e}")
        return None


def get_data(main, signal):
    base_year_2022_spring = 627117
    year = 2022
    semester_list = ["Spring", "Summer", "Fall"]
    current_semester = 0
    semester_data = {}
    continuous_fail_count = 0
    while True:
        data = academic_session_data(
            main, base_year_2022_spring, signal)
        if data:
            semester_data[(f"{semester_list[current_semester]}_"
                           f"{year}_{base_year_2022_spring}")] = data
            current_semester = (current_semester + 1) % 3
            if current_semester == 0:
                year += 1
            continuous_fail_count = 0
        else:
            continuous_fail_count += 1
        base_year_2022_spring += 1
        if continuous_fail_count > 10:
            break
    return semester_data


def synthesis_data(semester_data, signal):
    for key, value in semester_data.items():
        data = {}
        signal.emit(f"Synthesizing data for {key}")
        for course in value:
            course_code = course["cell"][2]
            faculty = course["cell"][5]
            section = course["cell"][7]
            data[(course_code, section)] = faculty
        semester_data[key] = data
    return semester_data


def get_current_semester_name(main, signal):
    signal.emit("Getting current semester name")
    response = main.session.get(
        "https://usis.bracu.ac.bd/academia/studentCourse/loadPreviousResultByStudent")
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all('tr')
    semester_name = ""
    for row in rows[1:]:
        cols = row.find_all('td')
        if cols[0].text.strip() == "SEMESTER :":
            semester_name = cols[1].text.strip()
    return semester_name.lower()


def predict_faculty(course_code, section):
    semester_data = get_prediction_data()
    faculty_list = []
    for key, value in semester_data.items():
        faculty_list.append(value.get((course_code, section), None))
    result_dict = {}
    for idx, faculty in enumerate(faculty_list):
        if faculty:
            if faculty in result_dict and faculty != "TBA":
                result_dict[faculty] += ((idx + 1) * 2)
            else:
                result_dict[faculty] = ((idx + 1) * 1)
    total = sum(result_dict.values())
    for key, value in result_dict.items():
        result_dict[key] = (value / total) * 100
    return result_dict


def get_course_data(main, signal):
    prediction_data = get_data(main, signal)
    prediction_data = synthesis_data(prediction_data, signal)
    set_prediction_data(prediction_data)

    last_semester_text = list(prediction_data.keys())[-1]
    last_semester_name, last_semester_year, last_semester = last_semester_text.split(
        "_")
    set_current_semester_name((last_semester_name, last_semester_year))
    main.footer_bar.next_semester_label.setText(
        f"Showing data for: {last_semester_name} {last_semester_year}")
    main.working_session_id = last_semester
    set_working_session_id(last_semester)

    current_semester_name = get_current_semester_name(main, signal)
    semester_name, semester_year = current_semester_name.split(" ")
    found = False
    count = 0
    for key in prediction_data.keys():
        semester, year, _ = key.split("_")
        if found:
            count += 1
        if semester.lower() == semester_name.lower() and year == semester_year:
            found = True
    current_semester_code = ""
    current_semester_name = ""
    current_semester_year = ""
    if count == 1:
        found = False
        for key in prediction_data.keys():
            semester, year, code = key.split("_")
            if found:
                current_semester_code = code
                current_semester_name = semester
                current_semester_year = year
            if semester.lower() == semester_name.lower() and year == semester_year:
                found = True
    else:
        found = False
        for key in prediction_data.keys():
            semester, year, code = key.split("_")
            if found:
                current_semester_code = code
                current_semester_name = semester
                current_semester_year = year
                break
            if semester.lower() == semester_name.lower() and year == semester_year:
                found = True
    set_next_semester_name((current_semester_name, current_semester_year))
    main.footer_bar.current_semester_label.setText(
        f"Current semester: {current_semester_name} {current_semester_year}")
    main.footer_bar.current_semester_label.show()
    main.footer_bar.next_semester_label.show()
    main.current_session_id = current_semester_code
    set_current_session_id(current_semester_code)
