from PyQt6.QtCore import QSettings

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


# reset_settings()
