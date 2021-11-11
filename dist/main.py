import sys
from db_help import DbHelper
import sqlite3
from pyowm import OWM
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui
from page3 import Ui_MainWindow
from page4 import Window
from page1 import Page1
from page2 import Page2
from page22 import Page22
from pyowm.utils.config import get_default_config


class Weather:
    def __init__(self, place):
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = OWM('fa2341043bc0ddc3934a1068470c66d4', config_dict)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(place)
        self.w = observation.weather
        self.temp = self.w.temperature('celsius')
        self.we = self.w.weather_icon_name
        self.t1 = 0
        self.t2 = 0
        self.humi = 0
        self.pr = 0
        self.st = ''

#  Температура
    def temperatura(self):
        self.t1 = self.temp['temp']
        self.t2 = self.temp['feels_like']
        return self.t1

#  Температура, как она ощущается
    def temperatura_fil(self):
        self.t2 = self.temp['feels_like']
        return self.t2

    # Влажность
    def vlag(self):
        self.humi = self.w.humidity
        return self.humi

    # Давление
    def dav(self):
        self.pr = self.w.pressure['press']
        return self.pr

    # Статус
    def status(self):
        st = self.w.detailed_status
        self.st = st.title()
        return self.st

#  Номер статуса
    def icon_name(self):
        if self.we == '01d' or self.we == '01n':
            return '1614545998_4-p-solntse-na-belom-fone-4.png'  # Ясное небо
        elif self.we == '02d' or self.we == '02n':
            return '194-1945831_clipart-of-sun-blue-moon-full-and-ash.png'  # Несколько облаков
        elif self.we == '03d' or self.we == '03n' or self.we == '04d' or self.we == '04n':
            return '170-1709571_cartoon-clip-art-cartoon-white-clouds-png-transparent.png'  # Облачно
        elif self.we == '09d' or self.we == '09n' or self.we == '10d' or self.we == '10n':
            return '7d3eb81b136a8e4cb61b3c54a1692518.png'  # Ливень, Дождь!
        elif self.we == '11d' or self.we == '11n':
            return '138-1389556_thunderstorm-clipart-storm-cloud-clipart-3995448-shop-cartoon.png'
        elif self.we == '13d' or self.we == '13n':
            return '1779887.png'  # Снег
        elif self.we == '50d' or self.we == '50n':
            return '7f68007e2fad78db079bf7c604f5dd63.png'  # Туман


# Нажатие кнопок и переход на страницы 2, 2.2 Входа и Регистрации
class Enter1(QMainWindow, Page1):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run1)
        self.pushButton_2.clicked.connect(self.run2)

    def run1(self):
        self.main_window = Main2(self)
        self.main_window.show()
        self.hide()

    def run2(self):
        self.main_window = Main22(self)
        self.main_window.show()
        self.hide()


# Вход
class Main22(QMainWindow, Page2):
    def __init__(self, enter_window):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.enter_window = enter_window
        self.is_check_done = False
        self.pushButton.clicked.connect(self.closeEvent)
        self.pushButton_2.clicked.connect(self.prov)

    def prov(self):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        con = sqlite3.connect('BASDT.db')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM BAS WHERE Пароль=? and ИМЯ=?""", (password, name)).fetchall()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Ошибка")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        if not result:
            msgBox.setText("Такой пользователь нет")
            msgBox.exec_()

        elif len(name) == 0 or len(password) == 0:
            msgBox.setText("Обнаружены пустые строки")
            msgBox.exec_()

        else:
            self.is_check_done = True

    def closeEvent(self, event):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if self.is_check_done:
            self.enter_window = Enter2(name, password)
            self.enter_window.show()
            self.hide()


# Регистрация
class Main2(QMainWindow, Page22):
    def __init__(self, enter_window):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.enter_window = enter_window
        self.is_check_done = False
        self.pushButton.clicked.connect(self.closeEvent)
        self.pushButton_2.clicked.connect(self.add)

    def add(self):
        db_helper = DbHelper()
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        city = self.lineEdit_3.text()
        city = city.lower()
        con = sqlite3.connect('BASDT.db')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM BAS WHERE Пароль=?""", (password,)).fetchall()
#  Создание окна ошибки
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Ошибка")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        if result:
            msgBox.setText("Такой пользователь уже есть")
            msgBox.exec_()

        elif len(name) == 0 or len(password) == 0 or len(city) == 0:
            msgBox.setText("Обнаружены пустые строки")
            msgBox.exec_()

        elif len(password) < 8 or password.upper() == password or password.lower() == password:
            msgBox.setText("Пароль не соответствует требованию."
                           "8 букв, наличие больших и маленьких букв и цифр")
            msgBox.exec_()

        elif city not in open('все города.txt', 'r', encoding='utf-8').read() or ' ' in city:
            msgBox.setText("Такого горада нет в списке")
            msgBox.exec_()

        else:
            city = city.title()
            try:
                result = db_helper.request("""INSERT INTO BAS('ИМЯ', 'Пароль', 'Город') VALUES (?, ?, ?)""",
                                           (name, password, city))
                if result:
                    self.is_check_done = True

                else:
                    raise Exception("Произошла ошибка при создании пользователя!")
            except Exception as ex:
                print(ex)
                msgBox.setText("Проверьте логи")
                msgBox.exec_()
                return

    def closeEvent(self, event):
        if self.is_check_done:
            self.enter_window = Main22(self)
            self.enter_window.show()
            self.hide()


# Ввод города
class Enter2(QMainWindow, Ui_MainWindow):
    def __init__(self, name, password):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.is_check_done = False
        self.pushButton.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.prov)
        self.pushButton_2.clicked.connect(self.run2)
        self.name = name
        self.password = password
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("MainWindow", self.name))

    def prov(self):
        self.city = self.name_input.text()
        city = self.city.lower()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Ошибка")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if city not in open('все города.txt', 'r', encoding='utf-8').read():
            msgBox.setText("Такого горада нет в списке")
            msgBox.exec_()

        elif len(self.city) == 0:
            msgBox.setText("Нет Ввода")
            msgBox.exec_()
        else:
            self.is_check_done = True

    def run(self):
        if self.is_check_done:
            city = self.city.title()
            self.main_window = Main3(self, city)
            self.main_window.show()
            self.hide()

    def run2(self):
        con = sqlite3.connect('BASDT.db')
        cur = con.cursor()
        res = cur.execute("""SELECT Город FROM BAS WHERE Пароль=? AND ИМЯ=?""", (self.password, self.name)).fetchall()
        for i in res:
            for city in i:
                self.main_window = Main3(self, city)
        self.main_window.show()
        self.hide()


# Узнаем погоду
class Main3(QMainWindow, Window):
    def __init__(self, enter_window, city):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.enter_window = enter_window
        self.weather = Weather(city)
        _translate = QtCore.QCoreApplication.translate
        self.label_12.setPixmap(QtGui.QPixmap(self.weather.icon_name()))
        self.label_7.setText(str(city))
        self.label_13.setText(_translate("MainWindow", self.weather.status()))
        self.lineEdit.setText(str(self.weather.temperatura()))
        self.lineEdit_2.setText(str(self.weather.temperatura_fil()))
        self.lineEdit_3.setText(str(self.weather.dav()))
        self.lineEdit_4.setText(str(self.weather.vlag()))

    def closeEvent(self, event):
        self.enter_window.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Enter1()
    ex.show()
    sys.exit(app.exec())
