COURSE_CARD_STYLE = """
    QWidget {
        background-color: #bed0ed;
        border: 2px solid black;
        border-radius: 5px;
        padding: 10px;
    }
    QWidget::hover {
        background-color: #81dbe6;
    }
"""

COURSE_CARD_CLICKED_STYLE = """
    QWidget {
        background-color: #aa64e8;
        border: 2px solid black;
        border-radius: 5px;
        padding: 10px;
    }
"""

NOT_BOLD_LABEL_STYLE = """
    QLabel {
        background-color: transparent;
        font-size: 14px;
        color: black;
        border: none;
        border-radius: 0px;
        padding: 0px;
        margin: 5px;
    }
"""

BOLD_LABEL_STYLE = """
    QLabel {
        background-color: transparent;
        font-size: 14px;
        font-weight: bold;
        color: black;
        border: none;
        border-radius: 0px;
        padding: 0px;
        margin: 5px;
    }
"""

SUCCESS_LABEL_STYLE = """
    QLabel {
        background-color: transparent;
        font-size: 14px;
        font-weight: bold;
        color: green;
        border: none;
        border-radius: 0px;
        padding: 0px;
        margin: 5px;
    }
"""

ERROR_LABEL_STYLE = """
    QLabel {
        background-color: transparent;
        font-size: 14px;
        font-weight: bold;
        color: red;
        border: none;
        border-radius: 0px;
        padding: 0px;
        margin: 5px;
    }
"""

STRICKEN_LABEL_STYLE = """
    QLabel {
        background-color: transparent;
        color:black;
        font-size: 14px;
        text-decoration: line-through;
        border: none;
        border-radius: 0px;
        padding: 0px;
        margin: 5px;
    }
"""
