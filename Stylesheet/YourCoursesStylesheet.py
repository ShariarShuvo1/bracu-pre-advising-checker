TITLE_LABEL_STYLE = """
    QLabel {
        font-size: 25px;
        font-weight: bold;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        background-color: #170040;
        color: white;
    }
"""
COURSE_SEARCH_INPUT_STYLE = """
    QLineEdit {
        border: 2px solid black;
        border-radius: 5px;
        padding: 5px;
        color:black;
        background-color: white;
    }
    QLineEdit::hover {
        border: 2px solid #ff00ee;
    }
    QLineEdit::focus {
        border: 2px solid #d600c8;
    }
"""
SCROLL_AREA_STYLE: str = """
    QScrollArea {
        background-color: white;
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
