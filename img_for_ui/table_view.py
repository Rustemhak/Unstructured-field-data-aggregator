import shutil
import sys

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QFileDialog, \
    QLineEdit, QLabel, QScrollArea
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy


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
        try:
            super().__init__()
            self.setWindowTitle('Results')
            self.table = QTableWidget()
            self.table.setObjectName("tableWidget")
            self.result_path = result_path
            self.resize(1200, 813)

            self.df = pd.read_excel(result_path, report_name)
            if self.df.size == 0:
                return

            self.df.fillna('', inplace=True)
            self.populateTable(self.df)

            # Создаем QScrollArea
            self.scroll = QScrollArea(self)
            self.scroll.setWidgetResizable(True)

            # Создаем содержимое для QScrollArea
            self.scrollContent = QWidget()
            self.scrollLayout = QVBoxLayout(self.scrollContent)

            # кнопка сохранения
            self.saveButton = QtWidgets.QPushButton()
            self.saveButton.setText('Сохранить')
            self.saveButton.clicked.connect(self.save_table)
            self.scrollLayout.addWidget(self.saveButton)

            # фильтры
            self.locationFilterLabel = QLabel("Местоположение:")
            self.locationFilter = QLineEdit()
            self.locationFilter.textChanged.connect(self.filterTable)
            self.scrollLayout.addWidget(self.locationFilterLabel)
            self.scrollLayout.addWidget(self.locationFilter)

            self.nameFilterLabel = QLabel("Месторождение:")
            self.nameFilter = QLineEdit()
            self.nameFilter.textChanged.connect(self.filterTable)
            self.scrollLayout.addWidget(self.nameFilterLabel)
            self.scrollLayout.addWidget(self.nameFilter)

            if 'объекты' in self.df.columns:
                self.objectFilterLabel = QLabel("Object Filter")
                self.objectFilter = QLineEdit()
                self.objectFilter.textChanged.connect(self.filterTable)
                self.scrollLayout.addWidget(self.objectFilterLabel)
                self.scrollLayout.addWidget(self.objectFilter)

            # таблица
            self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.table.setMinimumHeight(500)
            self.scrollLayout.addWidget(self.table)

            # граф
            if 'объекты' in self.df.columns:
                self.graph = self.create_graph()
                self.scrollLayout.addWidget(self.graph)

            # Устанавливаем scrollContent в качестве виджета для scroll
            self.scroll.setWidget(self.scrollContent)

            # Добавляем scroll в layout
            self.layout = QVBoxLayout(self)
            self.layout.addWidget(self.scroll)
        except Exception as ex:
            print(f'Error in Table.__init__: {ex}')

    def save_table(self):
        fname = QFileDialog.getSaveFileName(self, filter='Excel files (*.xlsx)')[0]
        try:
            shutil.copyfile(self.result_path, fname)
        except FileNotFoundError:
            print("No such file")

    def filterTable(self):
        try:
            if self.df is None:
                return

            locationFilter = self.locationFilter.text().lower()
            nameFilter = self.nameFilter.text().lower()

            filtered_df = self.df[self.df['Местоположение'].str.lower().str.contains(locationFilter) &
                                  self.df['Месторождение'].str.lower().str.contains(nameFilter)]

            if 'объекты' in self.df.columns:
                objectFilter = self.objectFilter.text().lower()
                print(filtered_df['объекты'])
                filtered_df = filtered_df[filtered_df['объекты'].str.lower().str.contains(objectFilter)]
                print(filtered_df['объекты'])

            filtered_df = filtered_df.reset_index(drop=True)
            self.populateTable(filtered_df)
        except Exception as ex:
            print(f'Error in filterTable: {ex}')

    def populateTable(self, df):
        try:
            self.table.clear()  # Clear the table
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
        except Exception as ex:
            print(f'Error in populateTable: {ex}')

    def create_graph(self):
        fig, axs = plt.subplots(3, 1, figsize=(10, 15), gridspec_kw={'hspace': 0.4})

        if 'количество залежей' in self.df.columns:
            print(self.df['количество залежей'])
            self.df['количество скважин'] = pd.to_numeric(
                self.df['количество залежей'],
                errors='coerce'
            )
            sns.barplot(x='объекты', y='количество скважин', data=self.df, ax=axs[0])
            axs[0].set_title('Количество скважин по объектам')
            axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=30)

        if 'нефтенасыщенность' in self.df.columns:
            print(self.df['нефтенасыщенность'])
            self.df['нефтенасыщенность'] = pd.to_numeric(
                self.df['нефтенасыщенность'].apply(lambda x: x.replace(',', '.')),
                errors='coerce'
            )
            sns.barplot(x='объекты', y='нефтенасыщенность', data=self.df, ax=axs[1])
            axs[1].set_title('Нефтенасыщенность по объектам')
            axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=30)

        if 'пористость' in self.df.columns:
            print(self.df['пористость'])
            self.df['пористость'] = pd.to_numeric(
                self.df['пористость'].apply(lambda x: x.replace(',', '.')),
                errors='coerce'
            )
            sns.barplot(x='объекты', y='пористость', data=self.df, ax=axs[2])
            axs[2].set_title('Пористость по объектам')
            axs[2].set_xticklabels(axs[2].get_xticklabels(), rotation=30)

        fig.subplots_adjust(top=0.97, bottom=0.1)

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.setMinimumHeight(1700)

        return canvas


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App([
        (Table('archangelsk.xlsx', 'Sheet1'), 'Архангельское'),
        # Table('Сводная_таблица_по_месторождениям.xlsx', 'Архангельское'),
    ])
    ex.show()
    sys.exit(app.exec_())
