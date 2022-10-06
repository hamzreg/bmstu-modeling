from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QMessageBox
)
import pyqtgraph as pg
from dataclasses import dataclass

from distribution.distribution import Disribution

@dataclass
class Settings:
    entry_width = 200

    button_width = 100

    function_title = 'График функции распределения'
    density_title = 'График плотности распределения '

    error_title = 'Ошибка ввода'
    error_text = 'Неверный ввод параметров.'


class UniformPage(QWidget):
    def get_page(self):
        params_layout = QHBoxLayout()

        ab_layout = QFormLayout()
        self.a_entry = QLineEdit()
        self.a_entry.setFixedWidth(Settings.entry_width)
        self.b_entry = QLineEdit()
        self.b_entry.setFixedWidth(Settings.entry_width)
        ab_layout.addRow('a:', self.a_entry)
        ab_layout.addRow('b:', self.b_entry)

        graphic_layout = QFormLayout()
        self.start_entry = QLineEdit()
        self.start_entry.setFixedWidth(Settings.entry_width)
        self.end_entry = QLineEdit()
        self.end_entry.setFixedWidth(Settings.entry_width)
        self.step_entry = QLineEdit()
        self.step_entry.setFixedWidth(Settings.entry_width)
        graphic_layout.addRow('Начало интервала:', self.start_entry)
        graphic_layout.addRow('Конец интервала:', self.end_entry)
        graphic_layout.addRow('Шаг:', self.step_entry)

        params_layout.addLayout(ab_layout)
        params_layout.addLayout(graphic_layout)


        view_layout = QHBoxLayout()
        styles = {'color':'#113665', 'font-size':'20px'}

        self.uniform_view = view = pg.PlotWidget()
        self.uniform_view.setBackground('w')
        self.uniform_view.setTitle(Settings.function_title, **styles, size='14pt')
        self.uniform_view.setLabel('left', 'F(x)', **styles)
        self.uniform_view.setLabel('bottom', 'x', **styles)
        self.uniform_view.showGrid(x=True, y=True)
        self.uniform_curve = view.plot(name='Line', pen=pg.mkPen('#113665', width=4))

        self.uniform_density_view = view = pg.PlotWidget()
        self.uniform_density_view.setBackground('w')
        self.uniform_density_view.setTitle(Settings.density_title, **styles, size='14pt')
        self.uniform_density_view.setLabel('left', 'p(x)', **styles)
        self.uniform_density_view.setLabel('bottom', 'x', **styles)
        self.uniform_density_view.showGrid(x=True, y=True)
        self.uniform_density_curve = view.plot(name='Line', pen=pg.mkPen('#113665', width=4))

        view_layout.addWidget(self.uniform_view)
        view_layout.addWidget(self.uniform_density_view)


        plot_button = QPushButton('Построить')
        plot_button.setFixedWidth(Settings.button_width)
        plot_button.clicked.connect(self.plot_uniform)


        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Введите параметры:'))
        main_layout.addLayout(params_layout)
        main_layout.addLayout(view_layout)
        main_layout.addWidget(plot_button)

        self.setLayout(main_layout)

    def plot_uniform(self):
        a, b, start, end, step = self.__parse_args()

        if b < a:
            self.__error_msg('Параметр b должен быть больше параметра a.')
            return
        elif end < start:
            self.__error_msg('Конец интервала должен быть больше начала интервала.')
            return
        
        distribution = Disribution()

        args, values = distribution.get_uniform_function(a, b, 
                                                         start, end, step)
        self.uniform_curve.setData(args, values)

        args, values = distribution.get_uniform_density(a, b, 
                                                        start, end, step)
        self.uniform_density_curve.setData(args, values)

    def __parse_args(self):
        try:
            a = float(self.a_entry.text())
            b = float(self.b_entry.text())

            start = float(self.start_entry.text())
            end = float(self.end_entry.text())
            step = float(self.step_entry.text())

            return a, b, start, end, step
        except:
            self.__error_msg(Settings.error_text)
    
    def __error_msg(self, text):
        msg = QMessageBox()

        msg.setText(text)
        msg.setWindowTitle(Settings.error_title)

        msg.exec()


class NormalPage(QWidget):
    def get_page(self):
        params_layout = QHBoxLayout()

        ms_layout = QFormLayout()
        self.mu_entry = QLineEdit()
        self.mu_entry.setFixedWidth(Settings.entry_width)
        self.sigma_entry = QLineEdit()
        self.sigma_entry.setFixedWidth(Settings.entry_width)
        ms_layout.addRow('μ:', self.mu_entry)
        ms_layout.addRow('σ:', self.sigma_entry)

        graphic_layout = QFormLayout()
        self.start_entry = QLineEdit()
        self.start_entry.setFixedWidth(Settings.entry_width)
        self.end_entry = QLineEdit()
        self.end_entry.setFixedWidth(Settings.entry_width)
        self.step_entry = QLineEdit()
        self.step_entry.setFixedWidth(Settings.entry_width)
        graphic_layout.addRow('Начало интервала:', self.start_entry)
        graphic_layout.addRow('Конец интервала:', self.end_entry)
        graphic_layout.addRow('Шаг:', self.step_entry)

        params_layout.addLayout(ms_layout)
        params_layout.addLayout(graphic_layout)


        view_layout = QHBoxLayout()
        styles = {'color':'#113665', 'font-size':'20px'}

        self.normal_view = view = pg.PlotWidget()
        self.normal_view.setBackground('w')
        self.normal_view.setTitle(Settings.function_title, **styles, size='14pt')
        self.normal_view.setLabel('left', 'F(x)', **styles)
        self.normal_view.setLabel('bottom', 'x', **styles)
        self.normal_view.showGrid(x=True, y=True)
        self.normal_curve = view.plot(name='Line', pen=pg.mkPen('#113665', width=4))

        self.normal_density_view = view = pg.PlotWidget()
        self.normal_density_view.setBackground('w')
        self.normal_density_view.setTitle(Settings.density_title, **styles, size='14pt')
        self.normal_density_view.setLabel('left', 'p(x)', **styles)
        self.normal_density_view.setLabel('bottom', 'x', **styles)
        self.normal_density_view.showGrid(x=True, y=True)
        self.normal_density_curve = view.plot(name='Line', pen=pg.mkPen('#113665', width=4))

        view_layout.addWidget(self.normal_view)
        view_layout.addWidget(self.normal_density_view)


        plot_button = QPushButton('Построить')
        plot_button.setFixedWidth(Settings.button_width)
        plot_button.clicked.connect(self.plot_normal)


        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Введите параметры:'))
        main_layout.addLayout(params_layout)
        main_layout.addLayout(view_layout)
        main_layout.addWidget(plot_button)

        self.setLayout(main_layout)

    def plot_normal(self):
        mu, sigma, start, end, step = self.__parse_args()

        if end < start:
            self.__error_msg('Конец интервала должен быть больше начала интервала.')
            return

        distribution = Disribution()

        args, values = distribution.get_normal_function(mu, sigma, 
                                                         start, end, step)
        self.normal_curve.setData(args, values)

        args, values = distribution.get_normal_density(mu, sigma, 
                                                        start, end, step)
        self.normal_density_curve.setData(args, values)

    def __parse_args(self):
        try:
            mu = float(self.mu_entry.text())
            sigma = float(self.sigma_entry.text())

            start = float(self.start_entry.text())
            end = float(self.end_entry.text())
            step = float(self.step_entry.text())

            return mu, sigma, start, end, step
        except:
            self.__error_msg(Settings.error_text)

    def __error_msg(self, message):
        msg = QMessageBox()

        msg.setText(message)
        msg.setWindowTitle(Settings.error_title)

        msg.exec()
