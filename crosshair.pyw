from PySide2 import QtWidgets, QtCore, QtGui
from time import sleep
from setup import query_

config = query_()

class Mira(QtWidgets.QDialog):
    def __init__(self, parente=None):
        self.parente = parente
        super(Mira, self).__init__(parent=self.parente)
        self.setWindowFlags(
            QtCore.Qt.WindowTransparentForInput 
            | QtCore.Qt.FramelessWindowHint 
            | QtCore.Qt.WindowStaysOnTopHint
        )
        self.resize(300, 600)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.lb = QtWidgets.QPushButton(self)
        self.lb.setIcon(QtGui.QPixmap(config["mira"]))
        self.lb.setIconSize(QtCore.QSize(config['tamanho'], config['tamanho']))
        self.lb.setStyleSheet('background: rgba(0, 0, 0, 0);')
        self.lb.resize(60, 60)
        self.lb.move(config['posicao'][0], config['posicao'][1])
        self.show()