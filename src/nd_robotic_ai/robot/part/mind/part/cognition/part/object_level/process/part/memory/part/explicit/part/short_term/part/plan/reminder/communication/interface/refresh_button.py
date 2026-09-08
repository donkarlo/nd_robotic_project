from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QPushButton


class RefreshButton(QPushButton):
    refresh_requested = Signal()

    def __init__(self, parent=None) -> None:
        QPushButton.__init__(self, parent)
        self._flash_active = False

        self.setFixedSize(56, 56)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip("Reload")

        self._flash_timer = QTimer(self)
        self._flash_timer.setSingleShot(True)
        self._flash_timer.timeout.connect(self._stop_flash)

        self.clicked.connect(self._on_clicked)

    def _on_clicked(self) -> None:
        self._start_flash()
        self.refresh_requested.emit()

    def _start_flash(self) -> None:
        self._flash_active = True
        self.update()
        self._flash_timer.start(180)

    def _stop_flash(self) -> None:
        self._flash_active = False
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        self._draw_background(painter)
        self._draw_refresh_symbol(painter)

    def _draw_background(self, painter: QPainter) -> None:
        if self.isDown():
            background_color = QColor("#B71C1C")
        else:
            background_color = QColor("#D32F2F")

        painter.setPen(Qt.NoPen)
        painter.setBrush(background_color)
        painter.drawEllipse(self.rect())

    def _draw_refresh_symbol(self, painter: QPainter) -> None:
        if self._flash_active:
            symbol_color = QColor("#FFFFFF")
        else:
            symbol_color = QColor("#F4F4F4")

        pen = QPen(symbol_color)
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        arc_rect = QRectF(14, 14, 28, 28)
        start_angle = 35 * 16
        span_angle = 265 * 16
        painter.drawArc(arc_rect, start_angle, span_angle)

        painter.setBrush(symbol_color)
        arrow = QPolygonF(
            [
                QPointF(38, 18),
                QPointF(30, 18),
                QPointF(35, 26),
            ]
        )
        painter.drawPolygon(arrow)
