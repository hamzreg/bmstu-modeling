from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)
from dataclasses import dataclass

from generators.tabular_generator import TabularGenerator
from generators.mixed_generator import MixedGenerator
from generators.chance import get_chance

@dataclass
class Settings:
    line_width = 125

    generate_button_width = 200
    generate_button_text = 'Сгенерировать числа'
    solve_button_width = 120
    solve_button_text = 'Вычислить'

    manual_table_width = 125
    generate_table_width = 357
    table_height = 324
    chance_table_heidht = 54

    chance_title = 'Коэффициент'
    error_title = 'Ошибка ввода'


@dataclass
class Constants:
    file_path = 'data/number_table.txt'
    count = 7000

    a = 84589
    mu = 45989
    m = 217728
    start = 1


class Page(QWidget):
    def __init__(self):
        super().__init__()

        self.__create_tables()

        self.tabular_generator = TabularGenerator(Constants.file_path)
        self.mixed_generator = MixedGenerator(Constants.a, Constants.mu, Constants.m, Constants.start)


        manual_part = QVBoxLayout()

        manual_title = QLabel('Ручной ввод')
        manual_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manual_part.addWidget(manual_title)

        manual_part.addWidget(self.manual_table)

        manual_chance_title = QLabel(Settings.chance_title + ':')
        manual_chance_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manual_part.addWidget(manual_chance_title)
        manual_part.addWidget(self.manual_chance)

        manual_button = QPushButton(Settings.solve_button_text)
        manual_button.setFixedWidth(Settings.solve_button_width)
        manual_button.clicked.connect(self.__get_manual_chance)
        manual_part.addWidget(manual_button)


        tabular_part = QVBoxLayout()

        tabular_title = QLabel('Табличный способ')
        tabular_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tabular_part.addWidget(tabular_title)
        
        tabular_part.addWidget(self.tabular_table)

        tabular_chance_title = QLabel(Settings.chance_title + 'ы:')
        tabular_chance_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tabular_part.addWidget(tabular_chance_title)
        tabular_part.addWidget(self.tabular_chance)


        algorithmic_part = QVBoxLayout()

        algorithmic_title = QLabel('Алгоритмический способ')
        algorithmic_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        algorithmic_part.addWidget(algorithmic_title)

        algorithmic_part.addWidget(self.algorithmic_table)

        algorithmic_chance_title = QLabel(Settings.chance_title + 'ы:')
        algorithmic_chance_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        algorithmic_part.addWidget(algorithmic_chance_title)
        algorithmic_part.addWidget(self.algorithmic_chance)


        generate_button = QPushButton(Settings.generate_button_text)
        generate_button.setFixedWidth(Settings.generate_button_width)
        generate_button.clicked.connect(self.__generate_numbers)

        solve_button = QPushButton(Settings.solve_button_text)
        solve_button.setFixedWidth(Settings.solve_button_width)
        solve_button.clicked.connect(self.__get_chances)

        buttons = QHBoxLayout()
        buttons.addWidget(generate_button)
        buttons.addWidget(solve_button)


        tables = QHBoxLayout()
        tables.addLayout(tabular_part)
        tables.addLayout(algorithmic_part)

        generation_part = QVBoxLayout()
        generation_part.addLayout(tables)
        generation_part.addLayout(buttons)

        hbox = QHBoxLayout()
        hbox.addLayout(manual_part)
        hbox.addLayout(generation_part)

        self.setLayout(hbox)

    def __create_tables(self):
        self.manual_table = QTableWidget()
        self.manual_table.setFixedSize(Settings.manual_table_width, 
                                       Settings.table_height)
        self.manual_table.setRowCount(10)
        self.manual_table.setColumnCount(1)

        self.manual_chance = QTableWidget()
        self.manual_chance.setFixedSize(Settings.manual_table_width,
                                          Settings.chance_table_heidht)
        self.manual_chance.setRowCount(1)
        self.manual_chance.setColumnCount(1)


        self.tabular_table = QTableWidget()
        self.tabular_table.setFixedSize(Settings.generate_table_width, 
                                        Settings.table_height)
        self.tabular_table.setColumnCount(3)

        self.tabular_chance = QTableWidget()
        self.tabular_chance.setFixedSize(Settings.generate_table_width,
                                           Settings.chance_table_heidht)
        self.tabular_chance.setRowCount(1)
        self.tabular_chance.setColumnCount(3)


        self.algorithmic_table = QTableWidget()
        self.algorithmic_table.setFixedSize(Settings.generate_table_width, 
                                       Settings.table_height)
        self.algorithmic_table.setColumnCount(3)

        self.algorithmic_chance = QTableWidget()
        self.algorithmic_chance.setFixedSize(Settings.generate_table_width,
                                               Settings.chance_table_heidht)
        self.algorithmic_chance.setRowCount(1)
        self.algorithmic_chance.setColumnCount(3)

    def __get_manual_chance(self):
        try:
            numbers = self.__get_numbers(self.manual_table, 0, check=True)
        except:
            return

        chance = round(get_chance(numbers), 5)

        self.manual_chance.setItem(0, 0,
                                  QTableWidgetItem(str(chance)))

    def __generate_numbers(self):
        self.tabular_table.setRowCount(Constants.count)
        self.algorithmic_table.setRowCount(Constants.count)

        for digit in range(1, 4):
            self.__fill_numbers(self.tabular_table, digit - 1,
                                self.tabular_generator.get_sequence(digit, Constants.count))
            self.__fill_numbers(self.algorithmic_table, digit - 1,
                                self.mixed_generator.get_sequence(digit, Constants.count))

    def __get_chances(self):

        tabular_chances = []
        algorithmic_chances = []

        for column in range(3):
            tabular_numbers = self.__get_numbers(self.tabular_table, column)
            tabular_chances.append(round(get_chance(tabular_numbers), 5))
            
            algorithmic_numbers = self.__get_numbers(self.algorithmic_table, column)
            algorithmic_chances.append(round(get_chance(algorithmic_numbers), 5))
        

        self.__fill_chances(self.tabular_chance, tabular_chances)
        self.__fill_chances(self.algorithmic_chance, algorithmic_chances)

    def __get_numbers(self, table, column, check=False):
        numbers = []

        for i in range(table.rowCount()):
            try:
                item = table.model().index(i, column).data()
                
                if check:
                    self.__check_item(item)
            except:
                raise ValueError
            else:
                numbers.append(int(item))
        
        return numbers

    def __fill_numbers(self, table, column, numbers):
        for i in range(table.rowCount()):
            table.setItem(i, column, QTableWidgetItem(str(numbers[i])))

    def __fill_chances(self, table, chances):
        for i, chance in enumerate(chances):
            table.setItem(0, i, QTableWidgetItem(str(chance)))

    def __check_item(self, item):
        try:
            item = int(item)
        except:
            self.__error_msg('Необходимо ввести целое число.')
            raise ValueError
        else:
            if item < 0 or item // 10 != 0:
                self.__error_msg('Число должно быть одноразрядным и положительным.')
                raise ValueError
            
    def __error_msg(self, text):
        msg = QMessageBox()

        msg.setText(text)
        msg.setWindowTitle(Settings.error_title)

        msg.exec()
