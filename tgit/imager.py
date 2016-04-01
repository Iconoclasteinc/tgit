# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QIODevice, QBuffer
from PyQt5.QtGui import QImage

from tgit.metadata import Image


def scale(image, width, height):
    edited = QImage.fromData(image.data, format_for(image.mime))
    if edited.isNull():
        return image

    scaled = edited.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    scaled.save(buffer, format_for(image.mime))
    buffer.close()
    return Image(mime=image.mime, data=buffer.data(), desc=image.desc, type_=image.type)


def format_for(mime_type):
    return mime_type.split("/")[1].upper()
