from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QSpinBox,
    QLabel,
    QHBoxLayout
)
from dataclasses import dataclass


@dataclass
class Constants:
    min_minutes = 1
    max_minutes = 59


class TimeSpinBox(QWidget):
    def __init__(self):
        super().__init__()

        self.value = QSpinBox()
        self.value.setRange(Constants.min_minutes,
                            Constants.max_minutes)

        self.limit = QSpinBox()
        self.limit.setRange(Constants.min_minutes,
                            Constants.max_minutes)

        sign = QLabel('±')
        sign.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.value)
        self.hbox.addWidget(sign)
        self.hbox.addWidget(self.limit)
