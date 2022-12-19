import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
import pandas as pd  # pip install pandas


class MyApp(QWidget):
    def __init__(self, result_path, report_name):
        super().__init__()
        self.window_width, self.window_height = 700, 500
        self.resize(self.window_width, self.window_height)
        self.setWindowTitle('Results')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.result_path = result_path
        self.report_name = report_name

        self.button = QPushButton('&Загрузить данные')
        self.button.clicked.connect(
            lambda _, xl_path=self.result_path, sheet_name=self.report_name: self.loadExcelData(xl_path, sheet_name))
        layout.addWidget(self.button)

    def loadExcelData(self, excel_file_dir, worksheet_name):
        try:
            df = pd.read_excel(excel_file_dir, worksheet_name)
        except Exception as ex:
            print(ex)
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


class Table(QTableWidget):
    def __init__(self, parent, result_path, report_name):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 0, 1111, 381))
        self.setObjectName("tableWidget")

        try:
            df = pd.read_excel(result_path, report_name)
        except Exception as ex:
            print(ex)
        if df.size == 0:
            return

        df.fillna('', inplace=True)
        self.setRowCount(df.shape[0])
        self.setColumnCount(df.shape[1])
        self.setHorizontalHeaderLabels(df.columns)

        # returns pandas array object
        for row in df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.setItem(row[0], col_index, tableItem)

        self.setColumnWidth(2, 300)


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    excel_file_path = 'Сводная_таблица_по_месторождениям.xlsx'
    worksheet_name = 'Архангельское'

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 17px;
        }
    ''')

    myApp = MyApp(excel_file_path, worksheet_name)
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
