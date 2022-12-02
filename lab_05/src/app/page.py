from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QSpinBox,
    QFormLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton
)
from dataclasses import dataclass

from app.time_spinbox import TimeSpinBox
from center.client_generator import ClientGenerator
from center.operator import Operator
from center.computer import Computer
from center.center import Center

@dataclass
class Settings:
    button_text = 'Промоделировать'


@dataclass
class Constants:
    min_clients_number = 100
    max_clients_number = 1000

    min_minutes = 1
    max_minutes = 59


class Page(QWidget):
    def __init__(self):
        super().__init__()

        clients_title = QLabel('Клиенты')
        clients_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clients_number = QSpinBox()
        self.clients_number.setRange(Constants.min_clients_number,
                                     Constants.max_clients_number)

        self.clients_time = TimeSpinBox()

        clinets_parameters = QFormLayout()
        clinets_parameters.addRow(QLabel('Число клиентов:'), 
                                  self.clients_number)
        clinets_parameters.addRow(QLabel('Интервал прибытия (мин.):'), 
                                  self.clients_time.hbox)

        clients = QVBoxLayout()
        clients.addWidget(clients_title)
        clients.addLayout(clinets_parameters)


        center_title = QLabel('Информационный центр')
        center_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        operators_title = QLabel('Время обслуживания')
        operators_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_operator = TimeSpinBox()
        self.second_operator = TimeSpinBox()
        self.third_operator = TimeSpinBox()

        operators = QFormLayout()
        operators.addRow(QLabel('первым оператором (мин.)'), 
                         self.first_operator.hbox)
        operators.addRow(QLabel('вторым оператором (мин.)'), 
                         self.second_operator.hbox)
        operators.addRow(QLabel('третьим оператором (мин.)'), 
                         self.third_operator.hbox)

        computers_title = QLabel('Время обработки')
        computers_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_computer = QSpinBox()
        self.first_computer.setRange(Constants.min_minutes,
                                     Constants.max_minutes)
        self.second_computer = QSpinBox()
        self.second_computer.setRange(Constants.min_minutes,
                                     Constants.max_minutes)

        computers = QFormLayout()
        computers.addRow(QLabel('первым компьютером (мин.)'), 
                         self.first_computer)
        computers.addRow(QLabel('вторым компьютером (мин.)'), 
                         self.second_computer)


        result_title = QLabel('Результат')
        result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.successes_number = QLineEdit()
        self.failures_number = QLineEdit()
        self.failure_probability = QLineEdit()

        result_parameters = QFormLayout()
        result_parameters.addRow(QLabel('Число обслуженных клиентов:'), 
                                 self.successes_number)
        result_parameters.addRow(QLabel('Число отказов:'), 
                                 self.failures_number)
        result_parameters.addRow(QLabel('Вероятность отказа:'), 
                                 self.failure_probability)

        result = QVBoxLayout()
        result.addWidget(result_title)
        result.addLayout(result_parameters)


        button = QPushButton(Settings.button_text)
        button.clicked.connect(self.__simulate_center)


        center = QVBoxLayout()
        center.addLayout(clients)
        center.addWidget(center_title)
        center.addWidget(operators_title)
        center.addLayout(operators)
        center.addWidget(computers_title)
        center.addLayout(computers)
        center.addWidget(button)
        center.addLayout(result)

        self.setLayout(center)

    def __simulate_center(self):
        self.__create_center()
        failures_number = self.center.service_clients()
        self.__set_result(failures_number)

    def __create_center(self):
        first_computer = Computer(self.first_computer.value(),
                                  self.first_computer.value())
        second_computer = Computer(self.second_computer.value(),
                                  self.second_computer.value())

        first_operator = Operator(self.first_operator.value.value(),
                                  self.first_operator.limit.value(),
                                  first_computer)
        second_operator = Operator(self.second_operator.value.value(),
                                  self.second_operator.limit.value(),
                                  first_computer)
        third_operator = Operator(self.third_operator.value.value(),
                                  self.third_operator.limit.value(),
                                  second_computer)
        operators = [first_operator, second_operator, third_operator]

        client_generator = ClientGenerator(self.clients_time.value.value(),
                                           self.clients_time.limit.value(),
                                           operators,
                                           self.clients_number.value())

        self.center = Center(client_generator)

    def __set_result(self, failures_number):
        clients_number = self.clients_number.value()
        successes_number = clients_number - failures_number
        failure_probability = round(failures_number / clients_number, 5)

        self.successes_number.setText(str(successes_number))
        self.failures_number.setText(str(failures_number))
        self.failure_probability.setText(str(failure_probability))
