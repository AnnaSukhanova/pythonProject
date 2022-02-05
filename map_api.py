import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow


class MyMap(QMainWindow):
    def __init__(self):
        super().__init__()
        self.x, self.y, self.masht = '37.530887', '55.703118', '0.002'
        self.vid = 'map'
        self.metcy_and_over = {'pt=': []}
        uic.loadUi('1.ui', self)
        self.pushButton.clicked.connect(self.setImageToPixmap)
        self.map_request_str = ''
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                            self.y, '&spn=', self.masht, ',', self.masht, '&l=', self.vid]
        self.setImageToPixmap()
        self.setSelfFocus()
    def getImage(self):
        self.x = self.edit_x.toPlainText().strip()
        self.y = self.edit_y.toPlainText().strip()
        self.masht = self.mashtab.toPlainText().strip()
        if self.layer.currentIndex() == 0:
            self.vid = 'sat'
        if self.layer.currentIndex() == 1:
            self.vid = 'map'
        if self.layer.currentIndex() == 2:
            self.vid = 'skl'
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                            self.y, '&spn=', self.masht, ',', self.masht, '&l=', self.vid]
        self.map_request_str = ''.join(self.map_request) + self.addMetcyToMap()
        response = requests.get(self.map_request_str)
        if not response:
            return str('Ошибка выполнения запроса:' + '\n' + 'Http статус:' +
                       str(response.status_code) + '(' + str(response.reason) + ')')
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        # Запишем полученное изображение в файл.
        if self.layer.currentIndex() > 0:
            self.map_file = "map.png"
        else:
            self.map_file = "map.jpg"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        return 'успех'

    def setImageToPixmap(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMap()
    ex.show()
    sys.exit(app.exec())
