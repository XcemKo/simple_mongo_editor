from PyQt5 import QtWidgets, uic

class Dialog(QtWidgets.QDialog):
    def __init__(self):
        # Базовый конструктор окна
        QtWidgets.QDialog.__init__(self)

        super(Dialog, self).__init__()

        # Динамически загружает визуальное представление формы
        uic.loadUi('dialog.ui', self)

        self.radioButton.clicked.connect(self.checkRadio)

    def checkRadio(self):
        print("ChekcRadio")
        if self.radioButton.isChecked():
            self.Password_edit.setEchoMode(0)
        else:
            self.Password_edit.setEchoMode(2)

    def setMainWindow(self, main):
        self.main = main