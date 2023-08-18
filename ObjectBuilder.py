from PyQt6 import QtCore, QtGui


def object_builder(obj, coordinate, text=None, font_size=None, isBold=False, css="", connected=None, mousePointer=None, tooltip=None):
    item = obj
    item.setGeometry(QtCore.QRect(coordinate[0], coordinate[1], coordinate[2], coordinate[3]))
    if text is not None:
        if str(type(obj)) != "<class 'PyQt6.QtWidgets.QLineEdit'>":
            item.setText(text)
        else:
            item.setPlaceholderText(text)
    if font_size is not None:
        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setBold(isBold)
        item.setFont(font)
    item.setStyleSheet(css)
    if connected is not None:
        item.clicked.connect(connected)
    if mousePointer is not None:
        item.setCursor(mousePointer)
    if tooltip is not None:
        item.setToolTip(tooltip)

    return item
