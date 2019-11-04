from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


def startapp():
    Form, Window = uic.loadUiType("res/GUI/QT/layout/main.ui")

    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()
    app.exec_()