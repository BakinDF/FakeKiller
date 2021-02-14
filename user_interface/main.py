from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from core import FakeKillerCore
from threading import Thread
from random import choice


def core_init(window):
    window.label_2.setText('Ожидайте окончания загрузки системы')
    window.core = FakeKillerCore()
    try:
        window.core.load_model()
    except FileNotFoundError:
        window.core.train_model()
    window.label_2.setText('Введите текст, чтобы узнать вердикт системы')


class UiFakeKiller(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(573, 743)
        MainWindow.setStyleSheet("background-color: rgb(167, 198, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 431, 471))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setStyleSheet("background-color: rgb(215, 222, 255);\n"
                                         "color: rgb(0, 0, 0);")
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 520, 431, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setUnderline(False)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(":!hover{\n"
                                   "    background-color: rgb(247, 255, 205);\n"
                                   "}\n"
                                   "\n"
                                   ":hover{\n"
                                   "    border: 4px solid black; \n"
                                   "    background-color: rgb(247, 255, 205);\n"
                                   "    padding: 10px;\n"
                                   "}")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 0, 151, 41))
        self.pushButton.setStyleSheet(":!hover{\n"
                                      "background-color: rgb(167, 198, 255);\n"
                                      "}\n"
                                      "\n"
                                      ":hover{\n"
                                      "    border: 4px solid black; \n"
                                      "    background-color: rgb(148, 179, 253);\n"
                                      "\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 600, 211, 41))
        self.pushButton_2.setStyleSheet(":!hover{\n"
                                        "background-color: rgb(167, 198, 255);\n"
                                        "}\n"
                                        "\n"
                                        ":hover{\n"
                                        "    border: 4px solid black; \n"
                                        "    background-color: rgb(148, 179, 253);\n"
                                        "\n"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 600, 211, 41))
        self.pushButton_3.setStyleSheet(":!hover{\n"
                                        "background-color: rgb(167, 198, 255);\n"
                                        "}\n"
                                        "\n"
                                        ":hover{\n"
                                        "    border: 4px solid black; \n"
                                        "    background-color: rgb(148, 179, 253);\n"
                                        "\n"
                                        "}")
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 573, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.menu.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fake Killer (Babansky Lab Corp)"))
        self.label.setText(_translate("MainWindow", "Введите текст:"))
        self.label_2.setText(_translate("MainWindow", "Введите текст, чтобы узнать вердикт системы"))
        self.pushButton.setText(_translate("MainWindow", "Очистить поле"))
        self.pushButton_2.setText(_translate("MainWindow", "Очистить поле"))
        self.pushButton_3.setText(_translate("MainWindow", "Выход"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.action.setText(_translate("MainWindow", "Справка"))
        self.action_2.setText(_translate("MainWindow", "Выход"))


class FakeKillerWindow(QMainWindow, UiFakeKiller):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.core = None
        Thread(target=core_init, args=(self,)).start()

    def initUI(self):
        self.show()
        self.pushButton_2.clicked.connect(self.clear_text)
        self.plainTextEdit.textChanged.connect(self.check_text)

    def clear_text(self):
        self.plainTextEdit.setPlainText('')
        self.label_2.setText('Введите текст, чтобы узнать вердикт системы')

    def check_text(self):
        yellow = '247, 255, 205'
        green = '192, 255, 169'
        red = '255, 151, 151'

        if self.core and self.core.model:
            score = self.core.complex_check()
            self.label_2.setText(str(score))
            color = choice([yellow, green, red])
            label_style = ":!hover{background-color: rgb(" + color + ");}\n" \
                                                                     ":hover{border: 4px solid black; " \
                                                                     "background-color: rgb(" + color + "}); " \
                                                                                                        "padding: 10px;}"
            self.label_2.setStyleSheet(label_style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FakeKillerWindow()
    sys.exit(app.exec())
