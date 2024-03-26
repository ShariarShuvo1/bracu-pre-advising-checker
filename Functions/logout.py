from Settings.SettingsData import set_setting


def logout(main):
    set_setting("IS_LOGGED_IN", False)
    set_setting("IS_LOGGED_IN_INFO_SAVED", False)
    set_setting("EMAIL", "")
    set_setting("PASSWORD", "")
    main.session.cookies.clear()
    main.logged_in(False)
