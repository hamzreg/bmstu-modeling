from logging import handlers
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QFormLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton
)
from dataclasses import dataclass

from app.time_spinbox import TimeSpinBox
from commission.enrollee_generator import EnrolleeGenerator
from commission.handler import Handler
from commission.receiver import Receiver
from commission.commission import Commission


@dataclass
class Settings:
    button_text = 'Промоделировать'


@dataclass
class Constants:
    min_enrollees_number = 100
    max_enrollees_number = 1000

    min_minutes = 1
    max_minutes = 59


class Page(QWidget):
    def __init__(self):
        super().__init__()

        enrollees_title = QLabel('Абитуриенты')
        enrollees_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.enrollees_number = QSpinBox()
        self.enrollees_number.setRange(Constants.min_enrollees_number,
                                       Constants.max_enrollees_number)

        self.enrollees_time = TimeSpinBox()

        enrollees_parameters = QFormLayout()
        enrollees_parameters.addRow(QLabel('Число абитуриентов:'), 
                                    self.enrollees_number)
        enrollees_parameters.addRow(QLabel('Интервал прибытия (мин.):'),
                                    self.enrollees_time.hbox)

        departments_title = QLabel('Вероятность выбора кафедр')
        departments_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_probability = QDoubleSpinBox()
        self.first_probability.setSingleStep(0.01)
        self.second_probability = QDoubleSpinBox()
        self.second_probability.setSingleStep(0.01)
        self.third_probability = QDoubleSpinBox()
        self.third_probability.setSingleStep(0.01)

        departments = QFormLayout()
        departments.addRow(QLabel('ИУ1-ИУ4'),
                           self.first_probability)
        departments.addRow(QLabel('ИУ5-ИУ8'),
                           self.second_probability)
        departments.addRow(QLabel('ИУ9-ИУ12'),
                           self.third_probability)

        enrollees = QVBoxLayout()
        enrollees.addWidget(enrollees_title)
        enrollees.addLayout(enrollees_parameters)
        enrollees.addWidget(departments_title)
        enrollees.addLayout(departments)
    

        commission_title = QLabel('Приемная комиссия')
        commission_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        handlers_title = QLabel('Время обработки анкеты')
        handlers_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_handler = TimeSpinBox()
        self.second_handler = TimeSpinBox()

        handlers = QFormLayout()
        handlers.addRow(QLabel('первым сотрудником (мин.)'), 
                        self.first_handler.hbox)
        handlers.addRow(QLabel('вторым сотрудником (мин.)'), 
                        self.second_handler.hbox)

        receivers_title = QLabel('Время приема документов')
        receivers_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_receiver = TimeSpinBox()
        self.second_receiver = TimeSpinBox()
        self.third_receiver = TimeSpinBox()

        receivers = QFormLayout()
        receivers.addRow(QLabel('первым сотрудником (мин.)'), 
                         self.first_receiver.hbox)
        receivers.addRow(QLabel('вторым сотрудником (мин.)'), 
                         self.second_receiver.hbox)
        receivers.addRow(QLabel('третьим сотрудником (мин.)'), 
                         self.third_receiver.hbox)

        result_title = QLabel('Число абитуриентов, подавших документы на')
        result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_departments = QLineEdit()
        self.second_departments = QLineEdit()
        self.third_departments = QLineEdit()

        result_parameters = QFormLayout()
        result_parameters.addRow(QLabel('ИУ1-ИУ4:'), 
                                 self.first_departments)
        result_parameters.addRow(QLabel('ИУ5-ИУ8:'), 
                                 self.second_departments)
        result_parameters.addRow(QLabel('ИУ9-ИУ12:'), 
                                 self.third_departments)

        result = QVBoxLayout()
        result.addWidget(result_title)
        result.addLayout(result_parameters)


        button = QPushButton(Settings.button_text)
        button.clicked.connect(self.__simulate_commission)


        commission = QVBoxLayout()
        commission.addLayout(enrollees)
        commission.addWidget(commission_title)
        commission.addWidget(handlers_title)
        commission.addLayout(handlers)
        commission.addWidget(receivers_title)
        commission.addLayout(receivers)
        commission.addWidget(button)
        commission.addLayout(result)

        self.setLayout(commission)

    def __simulate_commission(self):
        self.__create_commission()

        probabilities = [self.first_probability.value(),
                         self.second_probability.value(),
                         self.third_probability.value()]
        received_documents = self.commission.service_enrollees(probabilities)
        self.__set_result(received_documents)

    def __create_commission(self):
        first_receiver = Receiver(self.first_receiver.value.value(),
                                  self.first_receiver.limit.value())
        second_receiver = Receiver(self.second_receiver.value.value(),
                                   self.second_receiver.limit.value())
        third_receiver = Receiver(self.third_receiver.value.value(),
                                  self.third_receiver.limit.value())
        receivers = [first_receiver, second_receiver, third_receiver]

        first_handler = Handler(self.first_handler.value.value(),
                                self.first_handler.limit.value())
        second_handler = Handler(self.second_handler.value.value(),
                                self.second_handler.limit.value())
        handlers = [first_handler, second_handler]

        enrollee_generator = EnrolleeGenerator(
                                 self.enrollees_time.value.value(),
                                 self.enrollees_time.limit.value(),
                                 handlers,
                                 self.enrollees_number.value())

        self.commission = Commission(enrollee_generator, receivers)

    def __set_result(self, received_documents):
        self.first_departments.setText(str(received_documents[0]))
        self.second_departments.setText(str(received_documents[1]))
        self.third_departments.setText(str(received_documents[2]))
