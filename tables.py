__author__ = 'vadik'

from PyQt5 import QtWidgets
from PyQt5 import QtCore
import mongo

tables = dict()
tables['itemsListTable'] = ["Cars",
                            "Drivers",
                            "Containers",
                            "Orders",
                            "Cargo"]

tables['Cars'] = ["_id",
                  "Model",
                  "LicensePlate",
                  "MaxWeight",
                  "MaxDistance",
                  "Driver",
                  "Containers"]

tables['Drivers'] = ["_id",
                     "FIO",
                     "CategoryLicense"]

tables['Containers'] = ["_id", #Number
                        "VolumeForCargo",
                        "Cargo"]

tables['Orders'] = ["_id",
                    "PickupCargo",
                    "Destination",
                    "LastDateDelivery",
                    "Created",
                    "Taken",
                    "Cargo"]

tables['Cargo'] = ["_id", "Metrics", "Count", "MinPart"]

tables['ComboBox'] = dict()
tables['ComboBox']['Cars']       = [5, 6]
tables['ComboBox']['Containers'] = [2]
tables['ComboBox']['Orders']     = [5, 6]

class ItemDelegateCombo(QtWidgets.QItemDelegate):
    def __init__(self, table, main_window, tableName):
        super(ItemDelegateCombo, self).__init__()
        QtWidgets.QItemDelegate.__init__(self)
        self.table = table
        self.comboBox = tables['ComboBox'][tableName]
        print("comboBox - ",self.comboBox)
        self.tableName = tableName
        print("tableName - ", self.tableName)
        self.main_window = main_window

    def createEditor(self, editor, QStyleOptionViewItem, index):
        print(index.column(),)
        if index.column() in self.comboBox and self.comboBox is not None:
            editor = QtWidgets.QComboBox(editor)
            name = tables[self.tableName][index.column()]
            print("name - " + str(name))
            query = mongo.getColumnFromCollection(name, '_id')
            if len(query) > 0:
                editor.addItems(query)
            else:
                editor.addItem(str("Нет " + tables[self.tableName][index.column()]),0)
            return editor
        return QtWidgets.QItemDelegate.createEditor(self, editor, QStyleOptionViewItem, index)

    def setEditorData(self, editor, index):
        if index.column() not in self.comboBox:
            value = index.model().data(index, QtCore.Qt.EditRole)
            editor.setText(value)
        else:
            item = editor.findData(editor.currentText())
            if item != -1:
                editor.setCurrentText(editor.ItemData(item))

    def setModelData(self, editor, item_model, index):
        if index.column() not in self.comboBox:
            value = editor.text()
            item_model.setData(index, value)
        else:
            text = editor.currentText()
            if text.find(str("Нет " + tables[self.tableName][index.column()])) == -1:
                item_model.setData(index, editor.currentText())