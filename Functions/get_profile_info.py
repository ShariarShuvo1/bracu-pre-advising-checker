from bs4 import BeautifulSoup

from Entity.Profile import Profile
from Entity.ProfileCourse import ProfileCourse


def get_profile_info(main) -> Profile:
    session = main.session
    response = session.get("https://usis.bracu.ac.bd/academia/student/showProfile")

    soup = BeautifulSoup(response.text, "html.parser")
    program = soup.find('font', class_='choice-color').next_sibling.get_text(strip=True)
    student_info = soup.find('div', class_='admission-form-inner-div').find_all('div', class_='element-input-value')
    image_id = soup.find('input', {'type': 'hidden', 'name': 'id'})['value']

    image_url = f"https://usis.bracu.ac.bd/academia/student/fetchImage/{image_id}"
    image = session.get(image_url)

    student_id = student_info[0].get_text(strip=True)
    full_name = student_info[1].get_text(strip=True)

    response = session.get("https://usis.bracu.ac.bd/academia/studentCourse/loadPreviousResultByStudent")
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all('tr')
    courses: list[ProfileCourse] = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if cols[0].text.strip() not in ("CUMULATIVE", "SEMESTER", "SEMESTER :"):
            course_code = cols[0].text.strip()
            course_name = cols[1].text.strip()
            try:
                course_credit = float(cols[2].text.strip())
            except ValueError:
                course_credit = 0.0
            try:
                credit_earned = float(cols[3].text.strip())
            except ValueError:
                credit_earned = 0.0
            grade = cols[4].text.strip()
            try:
                grade_point = float(cols[5].text.strip())
            except ValueError:
                grade_point = 0.0

            for course in courses:
                if course.course_code == course_code:
                    courses.remove(course)
                    break
            course = ProfileCourse(course_code, course_name, course_credit, credit_earned, grade, grade_point)
            courses.append(course)
    response = session.get(
        f"https://usis.bracu.ac.bd/academia/student/loadRegistrationFormReport?studentId={image_id}&academiaSessionId={main.current_session_id}"
    )
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', class_='registrationFormStyle')
    tr = table.find_all('tr')[1:]
    for row in tr:
        if not len(row.find_all_next("td")[4].text.strip()) > 0:
            course_code = row.find_all_next("td")[0].text.strip()
            course_name = row.find_all_next("td")[1].text.strip()
            try:
                course_credit = float(row.find_all_next("td")[3].text.strip())
            except ValueError:
                course_credit = 0.0
            credit_earned = 0.0
            grade = "Pending"
            grade_point = 0.0
            for course in courses:
                if course.course_code == course_code:
                    courses.remove(course)
                    break
            course = ProfileCourse(course_code, course_name, course_credit, credit_earned, grade, grade_point)
            courses.append(course)

    profile = Profile(student_id, full_name, image, program, courses)
    return profile
