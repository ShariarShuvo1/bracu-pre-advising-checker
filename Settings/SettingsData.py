from PyQt6.QtCore import QSettings

from Entity.Course import Course

settings = QSettings("BPAC", "BPAC_Settings")


def set_setting(setting_name, value):
    if type(value) is bool and value:
        value = "true"
    elif type(value) is bool and not value:
        value = "false"
    settings.setValue(setting_name, value)


def get_setting(setting_name, default=None):
    value = settings.value(setting_name, default)
    if value == "true":
        return True
    elif value == "false":
        return False
    return value


if not settings.contains("IS_LOGGED_IN"):
    set_setting("IS_LOGGED_IN", False)
if not settings.contains("IS_LOGGED_IN_INFO_SAVED"):
    set_setting("IS_LOGGED_IN_INFO_SAVED", False)
if not settings.contains("EMAIL"):
    set_setting("EMAIL", "")
if not settings.contains("PASSWORD"):
    set_setting("PASSWORD", "")
if get_setting("IS_LOGGED_IN") and not get_setting("IS_LOGGED_IN_INFO_SAVED"):
    set_setting("IS_LOGGED_IN", False)
    set_setting("IS_LOGGED_IN_INFO_SAVED", False)


def reset_settings():
    set_setting("IS_LOGGED_IN", False)
    set_setting("IS_LOGGED_IN_INFO_SAVED", False)
    set_setting("EMAIL", "")
    set_setting("PASSWORD", "")


def course_data_contains() -> bool:
    return settings.contains("COURSE_DATA")


def get_backup_course_data() -> list[Course]:
    return settings.value("COURSE_DATA")


def set_backup_course_data(data: list[Course]):
    settings.setValue("COURSE_DATA", data)


def pre_requisite_data_contains() -> bool:
    return settings.contains("PRE_REQ_DATA")


def get_pre_requisite_data() -> dict[str, list[str]]:
    return settings.value("PRE_REQ_DATA")


def set_pre_requisite_data(data: dict[str, list[str]]):
    settings.setValue("PRE_REQ_DATA", data)


def set_working_session_id(session_id: str):
    set_setting("WORKING_SESSION_ID", session_id)


def get_working_session_id() -> str:
    return get_setting("WORKING_SESSION_ID")


def working_session_id_contains() -> bool:
    return settings.contains("WORKING_SESSION_ID")


def set_current_session_id(session_id: str):
    set_setting("CURRENT_SESSION_ID", session_id)


def get_current_session_id() -> str:
    return get_setting("CURRENT_SESSION_ID")


def current_session_id_contains() -> bool:
    return settings.contains("CURRENT_SESSION_ID")


def set_prediction_data(data):
    settings.setValue("PREDICTION_DATA", data)


def get_prediction_data():
    return settings.value("PREDICTION_DATA")


def prediction_data_contains():
    return settings.contains("PREDICTION_DATA")


def set_current_semester_name(name):
    set_setting("CURRENT_SEMESTER_NAME", name)


def get_current_semester_name() -> str:
    return get_setting("CURRENT_SEMESTER_NAME")


def current_semester_name_contains() -> bool:
    return settings.contains("CURRENT_SEMESTER_NAME")


def set_next_semester_name(name):
    set_setting("NEXT_SEMESTER_NAME", name)


def get_next_semester_name() -> str:
    return get_setting("NEXT_SEMESTER_NAME")


def next_semester_name_contains() -> bool:
    return settings.contains("NEXT_SEMESTER_NAME")


# reset_settings()
