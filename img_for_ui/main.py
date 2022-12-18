from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QFileDialog, QScrollArea

from get_result.main import get_result
from main5_base import Ui_MainWindow


class MainWindowUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_file_path)
        self.pushButton_2.clicked.connect(self.algorithm)
        self.list_of_file_paths = []
        self.result_path = ''

        self.algo_thread = QThread(self)
        self.algo = Algorithm(get_result, self.progressBar, report=self.list_of_file_paths)
        self.algo.moveToThread(self.algo_thread)

        self.algo.path_to_result.connect(self.processing_of_results)
        self.data_received.connect(self.algo.run)

        self.algo_thread.start()

    data_received = pyqtSignal()

    def get_file_path(self):
        print('Button pressed')
        file_name = QFileDialog.getOpenFileName()
        print(file_name[0])

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

    def algorithm(self):
        print('algorithm')
        if self.list_of_file_paths:
            self.progressBar.setValue(0)
            print("Algorithm was starting")
            self.pushButton_2.setEnabled(False)
            self.pushButton.setEnabled(False)

            self.algo.set_attr(report=self.list_of_file_paths)
            self.data_received.emit()

    def processing_of_results(self, path):
        print(f'beg process... {path}')
        self.list_of_file_paths = []
        _translate = QtCore.QCoreApplication.translate
        text_browser = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n" \
                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n" \
                       "p, li { white-space: pre-wrap; }\n" \
                       "</style></head>" \
                       "<body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n" \
                       "</body></html>"
        self.textBrowser.setHtml(_translate("MainWindow", text_browser))
        print(path)
        self.pushButton_2.setEnabled(True)
        self.pushButton.setEnabled(True)


class Algorithm(QObject):
    def __init__(self, function, progress_bar, *args, **kwargs):
        super(Algorithm, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.progress_bar = progress_bar

    path_to_result = pyqtSignal(str)

    def run(self):
        print('algo was starting')
        self.kwargs['progress_bar'] = self.progress_bar
        result = self.function(*self.args, **self.kwargs)
        print(f'algo return: {result}')
        self.path_to_result.emit(result)

    def set_attr(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


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
