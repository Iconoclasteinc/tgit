from PyQt5.QtCore import QPoint


def center_right(rect):
    return QPoint(rect.right(), rect.center().y())


def center_left(rect, with_offset=0):
    return QPoint(rect.left() + with_offset, rect.center().y())


def top_center(rect):
    return QPoint(rect.center().x(), rect.top())


def bottom_center(rect):
    return QPoint(rect.center().x(), rect.bottom())