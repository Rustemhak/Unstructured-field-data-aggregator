from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QFileDialog, QScrollArea, QWidget, QVBoxLayout
from threading import Thread

from main5_base import Ui_MainWindow
from get_result.main import get_result


class MainWindowUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_file_path)
        self.pushButton_2.clicked.connect(self.start)
        self.list_of_file_paths = []
        self.result_path = ''

    def get_file_path(self):
        print('Button pressed')
        file_name = QFileDialog.getOpenFileName()
        print(file_name)

        self.list_of_file_paths.append(file_name[0])
        _translate = QtCore.QCoreApplication.translate
        text_browser = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n" \
                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n" \
                       "p, li { white-space: pre-wrap; }\n" \
                       "</style></head>" \
                       "<body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"

        if self.list_of_file_paths:
            for file in self.list_of_file_paths:
                text_browser += f"<p><span style=\" font-size:10pt;\">{file}</span></p>"

        text_browser += "</body></html>"

        self.textBrowser.setHtml(_translate("MainWindow", text_browser))

    def start(self):
        if self.list_of_file_paths:
            print("Algorithm was starting")
            # thread = Thread(target=get_result,
            #                 args=(self.list_of_file_paths, 'pdf', False, True, None, None, self.progressBar))
            # thread.start()
            # self.result_path = thread.join()
            self.result_path = get_result(report=self.list_of_file_paths, progress_bar=self.progressBar)
            self.list_of_file_paths = []

            _translate = QtCore.QCoreApplication.translate
            text_browser = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n" \
                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n" \
                           "p, li { white-space: pre-wrap; }\n" \
                           "</style></head>" \
                           "<body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n" \
                           "</body></html>"
            self.textBrowser.setHtml(_translate("MainWindow", text_browser))

            print(self.result_path)


if __name__ == '__main__':
    app = QApplication([])
    window = QStackedWidget()
    main_window = MainWindowUi()
    scrollbar = QScrollArea(widgetResizable=True)
    scrollbar.setWidget(main_window)
    window.setFixedSize(QSize(900, 810))
    window.addWidget(scrollbar)
    window.show()
    app.exec()
