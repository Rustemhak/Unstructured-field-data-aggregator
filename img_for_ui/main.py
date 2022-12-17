from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QFileDialog, QScrollArea, QWidget, QVBoxLayout

from main5_base import Ui_MainWindow


class MainWindowUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_file_path)
        self.list_of_file_paths = []
        self.list_of_file_labels = []
        # self.scroll = QScrollArea()
        # self.widget = QWidget()
        # self.vbox = QVBoxLayout()
        # self.vbox.addWidget(self.centralwidget)
        # self.vbox.addWidget(self.label_3)
        # self.vbox.addWidget(self.textBrowser)
        # self.vbox.addWidget(self.menubar)
        # self.vbox.addWidget(self.statusbar)
        # self.widget.setLayout(self.vbox)
        # self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scroll.setWidgetResizable(True)
        # self.scroll.setWidget(self.widget)
        #
        # self.setCentralWidget(self.scroll)

    def get_file_path(self):
        print('Button pressed')
        file_name = QFileDialog.getOpenFileName()
        print(file_name)
        # self.myTextBox.setText(file_name)

        # self.list_of_file_labels.append(label)
        # self.list_of_file_paths.append(file_name[0])
        # for i, file in enumerate(self.list_of_file_paths):
        #     print(i, file)
        #     label = QtWidgets.QLabel(self.centralwidget)
        #     label.setGeometry(QtCore.QRect(0, -40, 1211 + i*100, 811))
        #     label.setText(file)
        #     label.setScaledContents(True)
        #     label.setObjectName(f"label_{i}")
        #     self.list_of_file_labels.append(label)


if __name__ == '__main__':
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = MainWindowUi()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec())

    app = QApplication([])
    window = QStackedWidget()
    main_window = MainWindowUi()
    scrollbar = QScrollArea(widgetResizable=True)
    scrollbar.setWidget(main_window)
    window.setFixedSize(QSize(1113, 780))
    window.addWidget(scrollbar)
    window.show()
    app.exec()
