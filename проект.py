import random
import sqlite3
import sys
sys.excepthook = lambda *a: sys.__excepthook__(*a)
from PyQt5 import uic, QtCore, QtMultimedia
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


# классы ошибок
class NoButtonsError(Exception):
    pass


class LengthButtonsError(SyntaxError):
    pass


class NumberButtonsError(ValueError):
    pass


class FirstForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 200, 900, 600)
        self.setWindowTitle('Запуск')
        # делаем фон окна запуска
        self.pixmap = QPixmap('neww.jpg')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(900, 600)
        self.image.setPixmap(self.pixmap)

        self.label_start = QLabel(self)
        self.label_start.setText('Если готовы проверить свою память, то скорее начинайте игру:)')
        self.label_start.resize(700, 50)
        self.label_start.setFont(QFont("Yu Gothic UI Semibold", 15))
        self.label_start.move(150, 100)

        self.label_rules = QLabel(self)
        self.label_rules.setText('Правила:')
        self.label_rules.resize(200, 70)
        self.label_rules.setFont(QFont("Yu Gothic UI Semibold", 20))
        self.label_rules.move(400, 320)

        self.label_disription1 = QLabel(self)
        self.label_disription1.setWordWrap(True)
        self.label_disription1.setText('1. Нажимая кнопку "Начать", вы сразу ниченайте игру, вам будет '
                                       'дано определенное время на запоминание картинки,'
                                       ' после чего начнется таймер заново, но уже надо будет '
                                       'воспроизвести полученную картинку по памяти.')
        self.label_disription1.resize(900, 100)
        self.label_disription1.setFont(QFont("Yu Gothic UI Semibold", 12))
        self.label_disription1.move(20, 360)

        self.label_disription2 = QLabel(self)
        self.label_disription2.setWordWrap(True)
        self.label_disription2.setText('2. Когда закончится время, если вы успешно прошли уровень, появится кнопка '
                                       'для прохождения следующего уровня, по мере возвышения уровня картинка '
                                       'будет сложнее, поэтому если вы неправильно соберете ее, '
                                       'то вы проигрываете и заканчиваете игру.')
        self.label_disription2.resize(900, 100)
        self.label_disription2.setFont(QFont("Yu Gothic UI Semibold", 12))
        self.label_disription2.move(20, 430)

        self.btn = QPushButton('Начать', self)
        self.btn.resize(200, 100)
        self.btn.move(350, 200)
        self.btn.setFont(QFont("Yu Gothic UI Semibold", 30))
        self.btn.setStyleSheet('QPushButton {background-color: #FFDAB9}')
        self.btn.clicked.connect(self.open_second_form)

    def open_second_form(self):
        self.second_form = SecondForm(self, "")
        self.second_form.show()


class SecondForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(500, 200, 900, 600)
        self.setWindowTitle('Проверь память')
        self.lbl = QLabel(args[-1], self)
        self.lbl.adjustSize()
        # делаем фон
        self.pixmap = QPixmap('pic.jpg')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(900, 600)
        self.image.setPixmap(self.pixmap)
        # звук кнопки
        media2 = QtCore.QUrl.fromLocalFile('knopka.mp3')
        content2 = QtMultimedia.QMediaContent(media2)
        self.player2 = QtMultimedia.QMediaPlayer()
        self.player2.setMedia(content2)

        self.level = 1
        # список кнопок нажатых игроком
        self.res_lst = []
        # список всех кнопок
        self.buttons_lst = []
        self.x = 0
        # надпись послу прохождения уровней
        self.label_question = QLabel(self)
        self.label_question.setText('Но готов ли ты доказать, что твоя память может вместить все что угодно?')
        self.label_question.resize(700, 100)
        self.label_question.setFont(QFont("Yu Gothic UI Semibold", 13))
        self.label_question.move(150, 200)
        self.label_question.hide()
        # кнопки выбора для бонусного уровны после прохождения
        self.button = QPushButton(self)
        self.button.resize(200, 70)
        self.button.move(150, 270)
        self.button.setText('НЕТ, Я УСТАЛ')
        self.button.setFont(QFont("Yu Gothic UI Semibold", 14))
        self.button.clicked.connect(self.quit)
        self.button.clicked.connect(self.player2.play)
        self.button.hide()

        self.button_2 = QPushButton(self)
        self.button_2.resize(200, 70)
        self.button_2.move(500, 270)
        self.button_2.setText('ДА, Я МЕГАМОЗГ')
        self.button_2.setFont(QFont("Yu Gothic UI Semibold", 14))
        self.button_2.clicked.connect(self.third_form)
        self.button_2.clicked.connect(self.player2.play)
        self.button_2.hide()

        self.lcd = QLCDNumber(self)
        # Устанавливаем значение по умолчанию на дисплей
        self.lcd.display(6)
        self.lcd.resize(100, 50)
        self.lcd.move(400, 50)

        self.label = QLabel(self)
        self.label.setFont(QFont("Yu Gothic UI Semibold", 13))
        self.label.resize(400, 60)
        self.label.move(340, 90)

        self.start_btn = QPushButton('Начать новый уровень', self)
        self.start_btn.setFont(QFont("Yu Gothic UI Semibold", 10))
        self.start_btn.resize(200, 40)
        self.start_btn.move(340, 140)
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet('QPushButton {background-color: #D8BFD8}')
        self.start_btn.clicked.connect(self.table)
        self.start_btn.clicked.connect(self.player2.play)
        # создание фоновой музыки
        media = QtCore.QUrl.fromLocalFile('music2.mp3')
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()

        self.end_btn = QPushButton('Выйти', self)
        self.end_btn.setFont(QFont("Yu Gothic UI Semibold", 13))
        self.end_btn.resize(100, 50)
        self.end_btn.move(750, 30)
        self.end_btn.clicked.connect(self.quit)
        self.end_btn.clicked.connect(self.player2.play)

        z, j = 300, 300
        # создаем талицу из кнопок
        for _ in range(6):
            if j > 480:
                self.btn = QPushButton(self)
                self.btn.resize(90, 70)
                self.btn.move(z, 270)
                self.buttons_lst.append(self.btn)
                # делаем их не кликабельными для запоминания последовательности
                self.btn.setEnabled(False)
                # привязываем их к функции изменения цвета и считывания
                self.btn.clicked.connect(self.paint_btn)
                z += 90
                self.btn.clicked.connect(self.player2.play)
            else:
                self.btn = QPushButton(self)
                self.btn.resize(90, 70)
                self.btn.move(j, 200)
                self.buttons_lst.append(self.btn)
                self.btn.setEnabled(False)
                self.btn.clicked.connect(self.paint_btn)
                self.btn.clicked.connect(self.player2.play)
                j += 90
        z = 300
        # для 2 уровня добывляем кнопки
        for _ in range(3):
            self.btn = QPushButton(self)
            self.btn.resize(90, 70)
            self.btn.move(z, 340)
            self.buttons_lst.append(self.btn)
            # делаем их не кликабельными для запоминания последовательности
            self.btn.setEnabled(False)
            # привязываем их к функции изменения цвета и считывания
            self.btn.clicked.connect(self.paint_btn)
            # скрываем их
            self.btn.hide()
            self.btn.clicked.connect(self.player2.play)
            z += 90
        # для уровня 3 добавляем кнопки
        z = 300
        for _ in range(3):
            self.btn = QPushButton(self)
            self.btn.resize(90, 70)
            self.btn.move(z, 410)
            self.buttons_lst.append(self.btn)
            # делаем их не кликабельными для запоминания последовательности
            self.btn.setEnabled(False)
            # привязываем их к функции изменения цвета и считывания
            self.btn.clicked.connect(self.paint_btn)
            # скрываем их
            self.btn.hide()
            self.btn.clicked.connect(self.player2.play)
            z += 90
        # для уровня 4 добавляем кнопки
        z = 200
        for _ in range(4):
            self.btn = QPushButton(self)
            self.btn.resize(90, 70)
            self.btn.move(570, z)
            self.buttons_lst.append(self.btn)
            # делаем их не кликабельными для запоминания последовательности
            self.btn.setEnabled(False)
            # привязываем их к функции изменения цвета и считывания
            self.btn.clicked.connect(self.paint_btn)
            # скрываем их
            self.btn.hide()
            self.btn.clicked.connect(self.player2.play)
            z += 70
        # для уровня 5 добавляем кнопки
        z = 200
        for _ in range(4):
            self.btn = QPushButton(self)
            self.btn.resize(90, 70)
            self.btn.move(210, z)
            self.buttons_lst.append(self.btn)
            # делаем их не кликабельными для запоминания последовательности
            self.btn.setEnabled(False)
            # привязываем их к функции изменения цвета и считывания
            self.btn.clicked.connect(self.paint_btn)
            # скрываем их
            self.btn.hide()
            self.btn.clicked.connect(self.player2.play)
            z += 70
        if self.level == 1:
            self.table()

    # функция которая закрашивает рандомные кнопки каждый раз
    def table(self):
        self.start_btn.setEnabled(False)
        self.label.setText('')
        if self.level == 1:
            # список кнопок которые должен нажать игрок
            self.must_btns = random.sample(self.buttons_lst[:6], 3)
            # окрашиваем кнопки
            for i in self.must_btns:
                i.setStyleSheet('QPushButton {background-color: #FF0000}')
            self.tick_timer()
        elif self.level == 2:
            for i in self.buttons_lst[:9]:
                i.show()
                i.setEnabled(False)
                i.setStyleSheet('QPushButton {background-color: #FFFFFF}')
            self.must_btns = random.sample(self.buttons_lst[:9], 4)
            for i in self.must_btns:
                i.setStyleSheet('QPushButton {background-color: #FF0000}')
            self.tick_timer()
        elif self.level == 3:
            for i in self.buttons_lst[:12]:
                i.show()
                i.setEnabled(False)
                i.setStyleSheet('QPushButton {background-color: #FFFFFF}')
            self.must_btns = random.sample(self.buttons_lst[:12], 6)
            for i in self.must_btns:
                i.setStyleSheet('QPushButton {background-color: #FF0000}')
            self.tick_timer()
        elif self.level == 4:
            for i in self.buttons_lst[:16]:
                i.show()
                i.setEnabled(False)
                i.setStyleSheet('QPushButton {background-color: #FFFFFF}')
            self.must_btns = random.sample(self.buttons_lst[:16], 9)
            for i in self.must_btns:
                i.setStyleSheet('QPushButton {background-color: #FF0000}')
            self.tick_timer()
        elif self.level == 5:
            for i in self.buttons_lst:
                i.show()
                i.setEnabled(False)
                i.setStyleSheet('QPushButton {background-color: #FFFFFF}')
            self.must_btns = random.sample(self.buttons_lst, 10)
            for i in self.must_btns:
                i.setStyleSheet('QPushButton {background-color: #FF0000}')
            self.tick_timer()

    def btn_for_levels(self):
        self.start_btn.setEnabled(True)
        for i in self.buttons_lst:
            i.setEnabled(False)

    # таблица когда игрок должен воспроизвести картинка
    def table_for_player(self):
        self.x += 1
        self.tick_timer()
        for i in self.buttons_lst:
            i.setStyleSheet('QPushButton {background-color: #FFFFFF}')
            i.setEnabled(True)

    # фун-ция закрашивает кнопки, которые нажал игрок и в список кладет
    def paint_btn(self):
        res = self.sender()
        self.sender().setStyleSheet('QPushButton {background-color: #FF0000}')
        self.sender().setEnabled(False)
        self.res_lst.append(res)

    def tick_timer(self):
        # Получаем значение на LCD виджете
        lcd_value = self.lcd.value()
        # время на запоминание картинки
        if lcd_value > 0:
            # Устанавливаем значение на 1 меньше
            self.lcd.display(lcd_value - 1)
            # Засекаем таймер - значение в милисекундах
            # метод singleShot создает поток в фоне, отменить его нельзя
            QTimer().singleShot(1000, self.tick_timer)
        else:
            if self.x == 1:
                self.check()
            elif self.x == 2:
                self.lcd.display(6)
                self.table_for_player()
            elif self.x == 3:
                self.check()
            elif self.x == 4:
                self.lcd.display(6)
                self.table_for_player()
            elif self.x == 5:
                self.check()
            elif self.x == 6:
                self.lcd.display(6)
                self.table_for_player()
            elif self.x == 7:
                self.check()
            elif self.x == 8:
                self.lcd.display(6)
                self.table_for_player()
            elif self.x == 9:
                self.check()
            self.lcd.display(6)
            if self.level == 1:
                self.table_for_player()

    # функция которая проверяет кнопки, которые нажали с теми, которые должны быть
    def check(self):
        try:
            if len(self.res_lst) == 0:
                raise NoButtonsError
            elif len(self.res_lst) == len(self.must_btns):
                for i in self.must_btns:
                    if i in self.res_lst:
                        continue
                    else:
                        raise NumberButtonsError
            else:
                raise LengthButtonsError
            if self.level == 5:
                self.label.setText('Ты прошел все уровни!(＾▽＾)')
                self.end_game1()
            else:
                self.level += 1
                self.x += 1
                self.btn_for_levels()
                self.label.setText('Поздравляем, с новым уровнем!')
                self.res_lst = []
        except NoButtonsError:
            for i in self.buttons_lst:
                i.setEnabled(False)
            self.label.setText('Вы не нажали кнопки.')
            self.level += 1
        except LengthButtonsError:
            for i in self.buttons_lst:
                i.setEnabled(False)
            self.label.setText('Вы нажали неправильное количество кнопок.')
            self.level += 1
        except NumberButtonsError:
            for i in self.buttons_lst:
                i.setEnabled(False)
            self.label.setText('Нажаты неверные кнопки.')
            self.level += 1

    def end_game1(self):
        for i in self.buttons_lst:
            i.hide()
        self.label_question.show()
        self.button.show()

        self.button_2.show()

    def third_form(self):
        self.player.stop()
        self.button_2.setEnabled(False)
        self.third_formm = ThirdForm(self, "")
        self.third_formm.show()

    def quit(self):
        sys.exit()


class ThirdForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('bokssssssssssss.ui', self)
        self.pixmap = QPixmap('bookssss.png')
        self.image = QLabel(self)
        self.image.move(250, 40)
        self.image.resize(241, 255)
        self.checkBoxes = []
        self.image.setPixmap(self.pixmap)
        self.checkBoxes.append(self.checkBox_10)
        self.checkBoxes.append(self.checkBox_11)
        self.checkBoxes.append(self.checkBox_12)
        self.checkBoxes.append(self.checkBox_13)
        self.checkBoxes.append(self.checkBox_14)
        self.checkBoxes.append(self.checkBox_15)
        self.checkBoxes.append(self.checkBox_16)
        self.checkBoxes.append(self.checkBox_17)
        self.checkBoxes.append(self.checkBox_18)
        self.checkBoxes.append(self.checkBox)
        self.checkBoxes.append(self.checkBox_2)
        self.checkBoxes.append(self.checkBox_3)
        for i in self.checkBoxes:
            i.hide()
        self.pushButton.clicked.connect(self.result)
        self.pushButton.hide()
        self.label_2.hide()
        self.pushButton_2.clicked.connect(self.start)

        self.label = QLabel(self)
        self.label.setFont(QFont("Yu Gothic UI Semibold", 13))
        self.label.resize(800, 200)
        self.label.move(60, 100)
        self.label.hide()
        con = sqlite3.connect('books.db')
        cur = con.cursor()
        self.res = cur.execute("""SELECT books FROM book WHERE data >= 1800 AND data <= 1835 
        AND NOT author = 'Пушкин' OR data >=1900 AND author='Чехов' """).fetchall()
        con.close()

        media = QtCore.QUrl.fromLocalFile('squid2.mp3')
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()

        media2 = QtCore.QUrl.fromLocalFile('win-song.mp3')
        content2 = QtMultimedia.QMediaContent(media2)
        self.player2 = QtMultimedia.QMediaPlayer()
        self.player2.setMedia(content2)

        media3 = QtCore.QUrl.fromLocalFile('lose-song.mp3')
        content3 = QtMultimedia.QMediaContent(media3)
        self.player3 = QtMultimedia.QMediaPlayer()
        self.player3.setMedia(content3)

        self.pixmap2 = QPixmap('picc.jpg')
        self.image2 = QLabel(self)
        self.image2.move(240, 230)
        self.image2.resize(300, 300)
        self.image2.setPixmap(self.pixmap2)
        self.image2.hide()

        self.pixmap3 = QPixmap('pic3.jpg')
        self.image3 = QLabel(self)
        self.image3.move(200, 230)
        self.image3.resize(400, 300)
        self.image3.setPixmap(self.pixmap3)
        self.image3.hide()

        self.pushButton_3.clicked.connect(self.quit)

    def start(self):
        for i in self.checkBoxes:
            i.show()
        self.label_2.show()
        self.label.show()
        self.image.hide()
        self.label_3.hide()
        self.pushButton_2.hide()
        self.pushButton.show()

    def result(self):
        self.pushButton.setEnabled(False)
        self.ans = []
        for i in range(12):
            if self.checkBoxes[i].isChecked():
                self.ans.append(f'{self.checkBoxes[i].text()}')
        self.check()

    def quit(self):
        sys.exit()

    def check(self):
        try:
            assert len(self.res) == len(self.ans)
            for i in self.res:
                assert i[0] in self.ans
            self.label.setText('Ты победил! Ты прошел все этапы и поэтому являешься настоящим мегамозгом!')
            self.player.stop()
            self.player2.play()
            self.image2.show()
            self.label_2.hide()
            for i in self.checkBoxes:
                i.hide()
            self.pushButton.hide()

        except AssertionError:
            self.label.move(120, 100)
            self.label.setText('Ты проиграл :( видно запомнил не всё, поэтому улучшай память.')
            self.player.stop()
            self.player3.play()
            self.image3.show()
            self.label_2.hide()
            for i in self.checkBoxes:
                i.hide()
            self.pushButton.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.show()
    sys.exit(app.exec())
