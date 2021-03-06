__author__ = 'vadik'

from PyQt5 import QtWidgets, uic
import mongo

class Dialog(QtWidgets.QDialog):
    def __init__(self):
        # Базовый конструктор окна
        QtWidgets.QDialog.__init__(self)

        super(Dialog, self).__init__()

        # Динамически загружает визуальное представление формы
        uic.loadUi('dialog.ui', self)

        self.radioButton.clicked.connect(self.checkRadio)
        self.Ok_Can.accepted.connect(self.checkUser)

    def checkRadio(self):
        if self.radioButton.isChecked():
            self.Password_edit.setEchoMode(0)
        else:
            self.Password_edit.setEchoMode(2)

    def setMainWindow(self, main):
        self.main = main

    def checkUser(self):
        user = self.Login_edit.text()
        password = self.Password_edit.text()
        ret = mongo.checkUser(user,password)
        print("{} {} - {}".format(user,password,ret))
        self.main.show()
        self.close()


