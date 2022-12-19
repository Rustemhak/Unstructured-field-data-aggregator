import shutil
import sys

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QFileDialog


class App(QWidget):

    def __init__(self, tables):
        super().__init__()
        self.setWindowTitle('Results')
        self.resize(1200, 813)
        self.table_widget = MyTableWidget(self, tables)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table_widget)


class MyTableWidget(QWidget):

    def __init__(self, parent, tables):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        for table in tables:
            self.tabs.addTab(*table)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class Table(QWidget):
    def __init__(self, result_path, report_name):
        super().__init__()
        self.setWindowTitle('Results')
        self.table = QTableWidget(self)
        self.table.setGeometry(QtCore.QRect(0, 0, 1111, 381))
        self.table.setObjectName("tableWidget")
        self.result_path = result_path
        self.resize(1200, 813)

        df = pd.read_excel(result_path, report_name)

        if df.size == 0:
            return

        df.fillna('', inplace=True)
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        # returns pandas array object
        for row in df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.table.setItem(row[0], col_index, tableItem)

        self.table.setColumnWidth(2, 300)

        self.saveButton = QtWidgets.QPushButton(self)
        self.saveButton.setText('Сохранить')
        self.saveButton.clicked.connect(self.save_table)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.table)

    def save_table(self):
        fname = QFileDialog.getSaveFileName(self, filter='Excel files (*.xlsx)')[0]
        try:
            shutil.copyfile(self.result_path, fname)
        except FileNotFoundError:
            print("No such file")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App([
        Table('Сводная_таблица_по_месторождениям.xlsx', 'Архангельское'),
        Table('Сводная_таблица_по_месторождениям.xlsx', 'Архангельское'),
    ])
    ex.show()
    sys.exit(app.exec_())
