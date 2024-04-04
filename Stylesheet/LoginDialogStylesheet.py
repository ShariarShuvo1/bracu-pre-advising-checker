EMAIL_INPUT_STYLE = """
    QLineEdit {
        font-size: 18px;
        border: 2px solid #000000;
        border-radius: 5px;
        padding: 5px;
        color:black;
    }
    QLineEdit:focus {
        border: 2px solid #cf82ff;
    }
"""

EMAIL_INPUT_ERROR_STYLE = """
    QLineEdit {
        font-size: 18px;
        border: 2px solid red;
        border-radius: 5px;
        padding: 5px;
        color:black;
    }
    QLineEdit:focus {
        border: 2px solid red;
    }
"""

EMAIL_LABEL_STYLE = """
    QLabel {
        font-size: 20px;
        padding-right: 10px;
        color:black;
    }
"""

REMEMBER_ME_CHECKBOX_STYLE = """
    QCheckBox {
        font-size: 16px;
        padding-left: 5px;
        color:black;
    }
"""

LOGIN_BUTTON_STYLE = """
    QPushButton {
        font-size: 16px;
        font-weight: bold;
        border: 2px solid black;
        border-radius: 5px;
        padding: 5px;
        background-color: white;
        color:black;
    }
    QPushButton:hover {
        background-color: #b672e0;
    }
    QPushButton:pressed {
        background-color: #a165c7;
    }
"""

LOADING_LABEL_STYLE = """
    QLabel {
        font-size: 16px;
        border: 2px solid black;
        border-radius: 5px;
        background-color: white;
        color:black;
    }
"""

STATUS_LABEL_STYLE = """
    QLabel {
        font-size: 12px;
        color:black;
    }
"""

STATUS_LABEL_SUCCESS_STYLE = """
    QLabel {
        font-size: 12px;
        color: green;
    }
"""

STATUS_LABEL_ERROR_STYLE = """
    QLabel {
        font-size: 12px;
        color: red;
    }
"""

INFO_BUTTON_STYLE = """
    QPushButton {
        background-color: transparent;
        color:black;
    }
    QPushButton:hover {
        border-radius: 15px;
        background-color: violet;
    }
    QPushButton:pressed {
        border-radius: 15px;
        background-color: #cf82ff;
    }
"""

TOGGLE_BUTTON_STYLE = """
    QPushButton {
        background-color: transparent;
        color:black;
    }
"""
