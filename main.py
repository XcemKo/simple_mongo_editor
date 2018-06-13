__author__ = 'vadik'

from tables import *
from dialog import Dialog
import mongo
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtCore import Qt

def clearTable(table):
    len = table.rowCount()
    for i in range(0,len):
        table.removeRow(0)

class MainWindow(QtWidgets.QMainWindow):
    def insertRow(self):
        self.Table.insertRow(self.Table.rowCount())

    def removeRow(self):
        self.Table.removeRow(self.Table.rowCount()-1)

    def fill_row(self):
        documents = mongo.getDocuments(self.currentTable)
        for i, doc in enumerate(documents):
            self.insertRow()
            for j, item in enumerate(doc):
                self.Table.setItem(i,j, QtWidgets.QTableWidgetItem(str(doc[item])))

    def do_table(self):
        table = self.Table
        column = table.columnCount()
        row = table.rowCount()
        maps=[]

        if row == 0: #если нет строк в таблице
            return
        for i in range(0,row):
            str = dict()
            for k in range(0,column):
                #print("{} {} {}".format(i,k,table.item(i, k)))
                try:
                    str[table.horizontalHeaderItem(k).text()] = int(table.item(i, k).text())
                except:
                    str[table.horizontalHeaderItem(k).text()] = table.item(i ,k).text()
            maps.append(str)
        mapsBase = mongo.getDocuments(self.currentTable)

        #ПЕРЕДЕЛАТЬ!!
        minLen = min(len(maps),len(mapsBase))
        for i in range(0, minLen):
            if (maps[i] != mapsBase[i]):
                print(maps[i])
                print(mapsBase[i])
                mongo.updateDoc(self.currentTable, maps[i]['_id'], maps[i])
        if(len(maps) > len(mapsBase)):
            for i in range(len(mapsBase),len(maps)):
                mongo.insertDoc(self.currentTable,maps[i]['_id'], maps[i])

    def __init__(self):
        # Базовый конструктор окна
        QtWidgets.QMainWindow.__init__(self)

        super(MainWindow, self).__init__()

        # Динамически загружает визуальное представление формы
        uic.loadUi('mainwindow.ui', self)

        toolBar = self.mainToolBar
        toolBar.addAction("Add", self.insertRow)
        toolBar.addAction("Delete", self.removeRow)
        self.currentTable = 'Cars'
        self.tableList.clear()
        self.tableList.addItems(tables['itemsListTable'])
        self.tableList.itemClicked.connect(self.checkItemListTable)

        self.Table.clear()
        clearTable(self.Table)
        self.Table.setHorizontalHeaderLabels(tables['Cars'])
        self.Table.setItemDelegate(ItemDelegateCombo(self.Table,
                                                     self.__weakref__,
                                                     self.currentTable)
                                   )

    def checkItemListTable(self, item):
        if item.text() == self.currentTable:
            return
        if tables.get(item.text()) is not None:
            self.do_table()
            self.Table.clear()
            clearTable(self.Table)

            self.Table.setColumnCount(len(tables[item.text()]))
            # headers = tables[item.text()][1:]
            headers = tables[item.text()]
            self.Table.setHorizontalHeaderLabels(headers)
            self.currentTable = item.text()
            if tables['ComboBox'].get(item.text()) is not None:
                self.Table.setItemDelegate(ItemDelegateCombo(self.Table,
                                                             main_window,
                                                             self.currentTable)
                                           )
            self.fill_row()

    def closeMainWindow(self):
        self.close()

    def keyPressEvent(self, e):
        print (e.key())
        if e.key() == Qt.Key_Escape:
                self.closeMainWindow()

# class TableList(QtWidgets.QListWidget):
#
#     def __init__(self):
#         print ("init")
#         QtWidgets.QListWidget.__init__(self)
#         super(TableList, self).__init__()
#         self.clear()


if __name__ == "__main__":
    """
    Создание основного окна программы
    """
    app = QtWidgets.QApplication(sys.argv)
    global main_window
    main_window = MainWindow()

    dialog = Dialog()
    dialog.Login_edit.setFocus()
    dialog.Password_edit.setEchoMode(2)
    dialog.setMainWindow(main_window)
    dialog.show()

    app.exec_()  # запуск приложения
