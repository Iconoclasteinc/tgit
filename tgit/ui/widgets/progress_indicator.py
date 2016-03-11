# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget


class QProgressIndicator(QWidget):
    _angle = 0
    _delay = 80
    _displayedWhenStopped = False
    _running = False
    _timerId = None

    def __init__(self, parent, color=None):
        super().__init__(parent)
        self.color = self.palette().color(QPalette.Text) if not color else QColor(color)

    def start(self):
        self._running = True
        self._startAnimation()
        self.show()

    def isRunning(self):
        return self._running

    def setDisplayedWhenStopped(self, state):
        self._displayedWhenStopped = state
        self.update()

    def isDisplayedWhenStopped(self):
        return self._displayedWhenStopped

    def stop(self):
        self._running = False

    def _startAnimation(self):
        self._stopTimer()
        self._reset()
        self._startTimer()

    def _reset(self):
        self._angle = 0

    def _startTimer(self):
        if self._timerId is None:
            self._timerId = self.startTimer(self._delay)

    def _stopTimer(self):
        if self._timerId is not None:
            self.killTimer(self._timerId)
            self._timerId = None

    def setAnimationDelay(self, delay):
        self._delay = delay
        if self.isRunning():
            self._stopTimer()
            self._startTimer()

    def setColor(self, color):
        self.color = color
        self.update()

    def sizeHint(self):
        return QSize(20,20)

    def heightForWidth(self, width):
        return width

    def timerEvent(self, event):
        if self.isRunning():
            self._advance()
        else:
            self._stopTimer()

        self.update()

    def _advance(self):
        self._angle = (self._angle + 30) % 360

    def paintEvent(self, event):
        if not self.isDisplayedWhenStopped() and not self.isRunning():
            return

        width = min(self.width(), self.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        outerRadius = (width-1) * 0.5
        innerRadius = (width-1) * 0.5 * 0.38

        capsuleHeight = outerRadius - innerRadius
        capsuleWidth  = capsuleHeight * 0.23 if width > 32 else capsuleHeight * 0.35
        capsuleRadius = capsuleWidth / 2

        for i in range(12):
            color = QColor(self.color)
            color.setAlphaF(float(1.0 - float(i / 12.0)))
            p.setPen(Qt.NoPen)
            p.setBrush(color)
            p.save()
            p.translate(self.rect().center())
            p.rotate(self._angle - float(i * 30.0))
            p.drawRoundedRect(-capsuleWidth * 0.5,
                              -(innerRadius + capsuleHeight),
                              capsuleWidth,
                              capsuleHeight,
                              capsuleRadius,
                              capsuleRadius)
            p.restore()
