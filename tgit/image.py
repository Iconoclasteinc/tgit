# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QIODevice, QBuffer
from PyQt5.QtGui import QImage


def scale(image_data, width, height):
    image = QImage.fromData(image_data)

    if image.isNull():
        scaled_image = image
    else:
        scaled_image = image.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    scaled_image.save(buffer, "PNG")
    buffer.close()
    return buffer.data()
