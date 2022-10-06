from PyQt6.QtWidgets import QMainWindow
from dataclasses import dataclass

from app.menu import Menu
from app.style import StyleSheet

@dataclass
class Settings:
    title = 'Равномерное и нормальное распределения'
    width = 1400
    height = 760


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(Settings.title)
        self.setFixedSize(Settings.width, Settings.height)
        self.setStyleSheet(StyleSheet)

        menu = Menu()
        self.setCentralWidget(menu)
