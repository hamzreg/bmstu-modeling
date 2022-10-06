from PyQt6.QtWidgets import (
    QWidget,
    QListWidget,
    QStackedWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox
)
from dataclasses import dataclass

from app.page import UniformPage, NormalPage


@dataclass
class Settings:
    list_height = 40

    info_title = 'О программе'
    info_text = 'Лабораторная работа выполнена Хамзиной Региной, ИУ7-73Б'


class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.items = QListWidget(self)
        self.items.setFixedHeight(Settings.list_height)

        self.items.insertItem(0, 'Равномерное распределение')
        self.items.insertItem(1, 'Нормальное распределение')


        self.uniform_page = UniformPage()
        self.normal_page = NormalPage()

        self.uniform_page.get_page()
        self.normal_page.get_page()

        self.pages = QStackedWidget()

        self.pages.addWidget(self.uniform_page)
        self.pages.addWidget(self.normal_page)


        info_button = QPushButton(Settings.info_title)
        info_button.clicked.connect(self.__get_info)


        hbox = QHBoxLayout()
        hbox.addWidget(info_button)
        hbox.addWidget(self.items)

        layout = QVBoxLayout()
        layout.addLayout(hbox)
        layout.addWidget(self.pages)

        self.setLayout(layout)

        self.items.currentRowChanged.connect(self.__display_page)

    def __display_page(self, index):
        self.pages.setCurrentIndex(index)

    def __get_info(self):
        info = QMessageBox()

        info.setText(Settings.info_text)
        info.setWindowTitle(Settings.info_title)

        info.exec()
