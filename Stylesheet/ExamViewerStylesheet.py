TITLE_LABEL_STYLE = """
    QLabel {
        background-color: #2d2d2d;
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 5px;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
    }
"""

SCROLL_AREA_STYLE: str = """
    QScrollArea {
        background-color: white;
        border-top: 0px;
        border-bottom: 2px solid black;
        border-left: 2px solid black;
        border-right: 2px solid black;
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
    }
    
    QScrollBar:vertical {
        border: none;
        background-color: transparent;
        width: 10px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #9a00bd;
        min-height: 20px;
        border-radius: 5px;
        width: 5px;
    }
    
    QScrollBar::add-line:vertical {
        height: 0px;
    }
    
    QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    QScrollBar::add-page:vertical {
        background: none;
    }
    
    QScrollBar::sub-page:vertical {
        background: none;
    }
"""

COURSE_LABEL_STYLE: str = """
    QLabel {
        background-color: #d1fff9;
        color: black;
        font-size: 14px;
        font-weight: bold;
        padding: 5px;
        border: 2px solid black;
        border-radius: 5px;
    }
    QLabel:hover {
        background-color: #b8f9f2;
    }
"""

DUPLICATE_TIME_COURSE_LABEL_STYLE: str = """
    QLabel {
        background-color: #fc8d8d;
        font-size: 14px;
        font-weight: bold;
        padding: 5px;
        border: 2px solid black;
        border-radius: 5px;
    }
    QLabel:hover {
        background-color: #fa7a7a;
    }
"""
DUPLICATE_DATE_COURSE_LABEL_STYLE: str = """
    QLabel {
        background-color: #fcb8fc;
        font-size: 14px;
        font-weight: bold;
        padding: 5px;
        border: 2px solid black;
        border-radius: 5px;
    }
    QLabel:hover {
        background-color: #faaafa;
    }
"""
