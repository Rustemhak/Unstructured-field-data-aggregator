import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
import pandas as pd


class MyApp(QWidget):
    def __init__(self, result_path, report_name):
        super().__init__()

        self.window_width, self.window_height = 700, 500
        self.resize(self.window_width, self.window_height)
        self.setWindowTitle('Results')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create filters
        self.locationFilter = QLineEdit(self)
        self.locationFilter.textChanged.connect(self.filterTable)
        layout.addWidget(self.locationFilter)

        self.nameFilter = QLineEdit(self)
        self.nameFilter.textChanged.connect(self.filterTable)
        layout.addWidget(self.nameFilter)

        self.objectFilter = QLineEdit(self)
        self.objectFilter.textChanged.connect(self.filterTable)
        layout.addWidget(self.objectFilter)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.result_path = result_path
        self.report_name = report_name

        self.button = QPushButton('&Загрузить данные')
        self.button.clicked.connect(
            lambda _, xl_path=self.result_path, sheet_name=self.report_name: self.loadExcelData(xl_path, sheet_name))
        layout.addWidget(self.button)

        self.df = None

    def loadExcelData(self, excel_file_dir, worksheet_name):
        try:
            self.df = pd.read_excel(excel_file_dir, worksheet_name)
        except Exception as ex:
            print(ex)
        if self.df.size == 0:
            return

        self.df.fillna('', inplace=True)
        self.filterTable()

    def filterTable(self):
        if self.df is None:
            return

        locationFilter = self.locationFilter.text().lower()
        nameFilter = self.nameFilter.text().lower()
        objectFilter = self.objectFilter.text().lower()

        filtered_df = self.df[self.df['Месторождение'].str.contains(nameFilter) &
                              self.df['Местоположение'].str.contains(locationFilter) &
                              self.df['Объекты'].str.contains(objectFilter)]  # Update this line
        self.populateTable(filtered_df)

    def populateTable(self, df):
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for row in df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.table.setItem(row[0], col_index, tableItem)

        self.table.setColumnWidth(2, 300)


if __name__ == '__main__':
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
