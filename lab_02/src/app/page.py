from PyQt6.QtWidgets import (
    QWidget,
    QSpinBox,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from dataclasses import dataclass

from qsystem.qsystem import QSystem, Constants


@dataclass
class Settings:
    spinbox_width = 40

    form_text = 'Выберите количество состояний системы:'

    plot_button_width = 150
    plot_button_text = 'Построить график'
    solve_button_width = 110
    solve_button_text = 'Определить'

    table_width = 1022
    matrix_table_height = 322
    result_table_height = 82

    error_title = 'Ошибка ввода'


class Page(QWidget):
    def __init__(self):
        super().__init__()

        self.size_spinbox = QSpinBox()
        self.size_spinbox.setFixedWidth(Settings.spinbox_width)
        self.size_spinbox.setRange(Constants.min_number_states,
                                   Constants.max_number_states)
        self.size_spinbox.valueChanged.connect(self.__change_tables)

        self.qsystem = QSystem(int(self.size_spinbox.value()))

        self.__create_tables()

        form = QFormLayout()
        form.addRow(Settings.form_text, self.size_spinbox)

        plot_button = QPushButton(Settings.plot_button_text)
        plot_button.setFixedWidth(Settings.plot_button_width)
        plot_button.clicked.connect(self.qsystem.plot_charts)

        solve_button = QPushButton(Settings.solve_button_text)
        solve_button.setFixedWidth(Settings.solve_button_width)
        solve_button.clicked.connect(self.__get_time_and_probabilities)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(form)
        self.hbox.addWidget(plot_button)
        self.hbox.addWidget(solve_button)

        vbox = QVBoxLayout()
        vbox.addLayout(self.hbox)
        vbox.addWidget(QLabel('Матрица интенсивностей переходов:'))
        vbox.addWidget(self.matrix_table)
        vbox.addWidget(QLabel('Вероятности и время пребывания:'))
        vbox.addWidget(self.result_table)
        self.setLayout(vbox)

    def __create_tables(self):
        self.matrix_table = QTableWidget()
        self.matrix_table.setFixedSize(Settings.table_width, 
                                       Settings.matrix_table_height)
        self.matrix_table.setRowCount(self.qsystem.number_states)
        self.matrix_table.setColumnCount(self.qsystem.number_states)

        self.result_table = QTableWidget()
        self.result_table.setFixedSize(Settings.table_width, 
                                       Settings.result_table_height)
        self.result_table.setRowCount(2)
        self.result_table.setColumnCount(self.qsystem.number_states)
        self.result_table.setVerticalHeaderItem(0, 
                                         QTableWidgetItem('P  '))
        self.result_table.setVerticalHeaderItem(1, 
                                         QTableWidgetItem('t  '))

    def __change_tables(self):
        prev_size = self.qsystem.number_states
        self.qsystem.number_states = int(self.size_spinbox.value())

        if self.qsystem.number_states > prev_size:
            for i in range(self.qsystem.number_states - prev_size):
                self.matrix_table.insertRow(prev_size + i)
                self.matrix_table.insertColumn(prev_size + i)
    
                self.result_table.insertColumn(prev_size + i)
        elif self.qsystem.number_states < prev_size:
            for i in range(prev_size - self.qsystem.number_states):
                self.matrix_table.removeRow(prev_size - i - 1)
                self.matrix_table.removeColumn(prev_size - i - 1)

                self.result_table.removeColumn(prev_size - i - 1)

    def __get_time_and_probabilities(self):
        try:
            self.__set_qsystem() 
        except:
            return

        probabilities = self.qsystem.get_limit_probabilities()
        self.__fill_probabilities(probabilities)

        time = self.qsystem.get_stabilization_time(probabilities)
        self.__fill_time(time)

    def __set_qsystem(self):
        matrix = []

        for i in range(self.qsystem.number_states):
            matrix.append([])
            for j in range(self.qsystem.number_states):
                try:
                    item = self.matrix_table.model().index(i, j).data()
                    self.__check_item(item)
                except:
                    raise ValueError
                else:
                    matrix[i].append(float(item))

        self.qsystem.intensity_matrix = matrix

    def __fill_probabilities(self, probabilities):
        for state, probability in enumerate(probabilities):
            self.result_table.setItem(0, state,
                               QTableWidgetItem(str(round(probability, 2))))

    def __fill_time(self, time):
        for state, value in enumerate(time):
            self.result_table.setItem(1, state,
                               QTableWidgetItem(str(round(value, 2))))

    def __check_item(self, item):
        try:
            item = float(item)
        except:
            self.__error_msg('Интенсивность перехода должна быть вещественным числом.')
            raise ValueError
        else:
            if item < 0:
                self.__error_msg('Интенсивность перехода должна быть неотрицательной.')
                raise ValueError

    def __error_msg(self, text):
        msg = QMessageBox()

        msg.setText(text)
        msg.setWindowTitle(Settings.error_title)

        msg.exec()
