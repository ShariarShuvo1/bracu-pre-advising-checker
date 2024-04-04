LIST_VIEWER_WIDGET_STYLE = """
    QWidget {
        background-color: white;
    }
"""

SEARCH_BAR_STYLE = """
    QLineEdit {
        background-color: white;
        border: 2px solid black;
        border-radius: 5px;
        padding: 5px;
        font-size: 15px;
        color:black;
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
        border: 2px solid black;
        border-radius: 5px;
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
