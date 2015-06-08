from PyQt5.QtCore import QPoint


def center_right(rect):
    return QPoint(rect.right(), rect.center().y())


def top_center(rect):
    return QPoint(rect.center().x(), rect.top())


def bottom_center(rect):
    return QPoint(rect.center().x(), rect.bottom())