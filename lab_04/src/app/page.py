from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QFormLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)
from dataclasses import dataclass

from qsystem.qsystem import QSystem

@dataclass
class Settings:
    button_text = 'Промоделировать'
    error_title = 'Ошибка ввода'


@dataclass
class Constants:
    min_msg_number = 1
    max_msg_number = 10000

    min_probability = 0.00
    max_probability = 1.00

    step = 0.01


class Page(QWidget):
    def __init__(self):
        super().__init__()

        generation_title = QLabel('Появление сообщений')
        generation_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.msg_number = QSpinBox()
        self.msg_number.setRange(Constants.min_msg_number,
                                 Constants.max_msg_number)
        self.step = QDoubleSpinBox()
        self.step.setSingleStep(0.01)
        msg_parameters = QFormLayout()
        msg_parameters.addRow(QLabel('Число сообщений:'), self.msg_number)
        msg_parameters.addRow(QLabel('Временной шаг:'), self.step)

        generation_law = QLabel('Параметры равномерного распределения:')
        self.a = QDoubleSpinBox()
        self.a.setSingleStep(Constants.step)
        self.a.setRange(-20, 20)
        self.b = QDoubleSpinBox()
        self.b.setSingleStep(Constants.step)
        self.b.setRange(-20, 20)
        generation_parameters = QFormLayout()
        generation_parameters.addRow(QLabel('a:'), self.a)
        generation_parameters.addRow(QLabel('b:'), self.b)

        generation = QVBoxLayout()
        generation.addWidget(generation_title)
        generation.addLayout(msg_parameters)
        generation.addWidget(generation_law)
        generation.addLayout(generation_parameters)


        handling_title = QLabel('Обработка сообщений')
        handling_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.return_probability = QDoubleSpinBox()
        self.return_probability.setSingleStep(Constants.step)
        self.return_probability.setRange(Constants.min_probability,
                                         Constants.max_probability)
        msg_return = QFormLayout()
        msg_return.addRow(QLabel('Вероятность возврата сообщения:'), 
                          self.return_probability)

        handling_law = QLabel('Параметры нормального распределения:')
        self.mu = QDoubleSpinBox()
        self.mu.setSingleStep(Constants.step)
        self.mu.setRange(-20, 20)
        self.sigma = QDoubleSpinBox()
        self.sigma.setSingleStep(Constants.step)
        handling_parameters = QFormLayout()
        handling_parameters.addRow(QLabel('μ:'), self.mu)
        handling_parameters.addRow(QLabel('σ:'), self.sigma)

        handling = QVBoxLayout()
        handling.addWidget(handling_title)
        handling.addLayout(msg_return)
        handling.addWidget(handling_law)
        handling.addLayout(handling_parameters)


        queue_title = QLabel('Максимальная длина очереди')
        queue_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.step_length = QLineEdit()
        self.eventful_length = QLineEdit()
        lengths = QFormLayout()
        lengths.addRow(QLabel('Принцип Δt:'), self.step_length)
        lengths.addRow(QLabel('Событийный принцип:'), self.eventful_length)

        queue = QVBoxLayout()
        queue.addWidget(queue_title)
        queue.addLayout(lengths)


        qsystem = QVBoxLayout()
        qsystem.addLayout(generation)
        qsystem.addLayout(handling)
        button = QPushButton(Settings.button_text)
        button.clicked.connect(self.__get_max_queue_length)
        qsystem.addWidget(button)
        qsystem.addLayout(queue)

        self.setLayout(qsystem)

    def __get_max_queue_length(self):
        msg_number = int(self.msg_number.value())
        step = float(self.step.value())
        return_probability = float(self.return_probability.value())

        a = float(self.a.value())
        b = float(self.b.value())

        mu = float(self.mu.value())
        sigma = float(self.sigma.value())

        self.qsystem = QSystem(a, b, mu, sigma,
                               msg_number, return_probability, step)

        step_max_length = self.qsystem.step_principle()
        eventful_max_length = self.qsystem.eventful_principle()

        self.step_length.setText(str(step_max_length))
        self.eventful_length.setText(str(eventful_max_length))
