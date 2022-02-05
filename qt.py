import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from math import factorial


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('file.ui', self)

        self.pushButton.clicked.connect(self.load_file)

    def load_file(self):
        with open('lines', 'r', encoding='utf8') as fin:
            data = fin.readlines()
            lst = []
            for i in range(len(list(data))):
                if i % 2 != 0:
                    self.listWidget.addItem(data[i].rstrip())
                else:
                    lst.append(data[i].rstrip())
            for i in lst:
                self.listWidget.addItem(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
