from crosshair import *
from functools import partial
import os
import json


def query_():
    with open('save.json', 'r', encoding='utf-8') as js:
        config = json.load(js)
    return config

config = query_()


class App(QtWidgets.QWidget):
    valorPadraoTam = config['tamanho']
    valorPadraoPos = config['posicao']
    localDir = os.path.abspath('./') + '\\targets'
    mirasPng = os.listdir(localDir)
    dictBotoes = dict()

    def __init__(self):
        super(App, self).__init__()
        self.resize(500, 500)
        self.setStyleSheet(
            '''
            QWidget {
            background-color: rgba(0, 0, 0, 100);
            color: #fff;
            }
            QPushButton {
                background-color: teal;
            }
            QPushButton:hover {
                background-color: gray;
            }
            ''')
        self.setWindowIcon(QtGui.QIcon('./targets/MIRA-azul.png'))
        self.layout_ = QtWidgets.QGridLayout(self)
        self.layout_.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        cont = 0
        for img in self.mirasPng:
            self.dictBotoes[img[:-4]] = QtWidgets.QPushButton()
            self.dictBotoes[img[:-4]].setIcon(
                QtGui.QIcon(
                    self.localDir + f'\\{img}'
                )
            )
            self.dictBotoes[img[:-4]].setIconSize(QtCore.QSize(40, 40))
            self.dictBotoes[img[:-4]].setText(img[5:-4])
            self.dictBotoes[img[:-4]].setCursor(QtCore.Qt.PointingHandCursor)
            self.dictBotoes[img[:-4]].clicked.connect(
                partial(self.getCross,
                self.dictBotoes[img[:-4]].text()
                )
            )
            self.layout_.addWidget(
                self.dictBotoes[img[:-4]], 0, cont, QtCore.Qt.AlignTop
            )
            cont += 1
        self.lb = QtWidgets.QLabel('Escala: %s' % self.valorPadraoTam)
        self.lb.setStyleSheet('color: teal; font: 100 15pt "Arial";')
        self.escala = QtWidgets.QSlider()
        self.escala.setOrientation(QtCore.Qt.Horizontal)
        self.escala.setMinimum(5)
        self.escala.setMaximum(60)
        self.escala.setSliderPosition(self.valorPadraoTam)
        self.escala.valueChanged.connect(self.slider_)
        self.lb2 = QtWidgets.QLabel(
            'Ajuste da posição: x-%s y-%s' %(
                self.valorPadraoPos[0],
                self.valorPadraoPos[1]
            )
        )
        self.lb2.setStyleSheet('color: teal; font: 100 15pt "Arial";')
        self.posX =  QtWidgets.QSlider()
        self.posX.setOrientation(QtCore.Qt.Horizontal)
        self.posX.setMinimum(0)
        self.posX.setMaximum(300)
        self.posX.setSliderPosition(self.valorPadraoPos[0])
        self.posX.valueChanged.connect(self.getX)
        self.posY = QtWidgets.QSlider()
        self.posY.setOrientation(QtCore.Qt.Horizontal)
        self.posY.setMinimum(0)
        self.posY.setMaximum(600)
        self.posY.setSliderPosition(self.valorPadraoPos[1])
        self.posY.valueChanged.connect(self.getY)
        bt = QtWidgets.QPushButton('Salvar')
        bt.clicked.connect(self.gravar)
        self.layout_.addWidget(self.lb, 1, 0, QtCore.Qt.AlignTop)
        self.layout_.addWidget(self.escala, 2, 0, 4, 0, QtCore.Qt.AlignTop)
        self.layout_.addWidget(self.lb2, 3, 0, 4, 0, QtCore.Qt.AlignTop)
        self.layout_.addWidget(self.posX, 4, 0, 4, 0, QtCore.Qt.AlignTop)
        self.layout_.addWidget(self.posY, 5, 0, 4, 0, QtCore.Qt.AlignTop)
        self.layout_.addWidget(bt, 6, 0, 4, 0, QtCore.Qt.AlignTop)
        self.mira = Mira()
        self.mira.lb.setIcon(QtGui.QPixmap(f'./targets/{config["mira"]}'))

    def slider_(self, valor):
        self.mira.lb.setIconSize(QtCore.QSize(valor, valor))
        self.lb.setText('Escala: %s' % valor)

    def getX(self, valor):
        self.mira.lb.move(valor, self.posY.value())
        self.lb2.setText(
            'Ajuste da posição: x-%s y-%s' %(
                valor, self.posY.value()
                )
            )

    def getY(self, valor):
        self.mira.lb.move(self.posX.value(), valor)
        self.lb2.setText(
            'Ajuste da posição: x-%s y-%s' %(
                self.posX.value(), valor
                )
            )
    
    def getCross(self, mira):
        self.mira_ = mira
        self.mira.lb.setIcon(QtGui.QPixmap(f'./targets/MIRA-{mira}.png'))

    def closeEvent(self, closeSignal):
        if closeSignal:
            conf = QtWidgets.QMessageBox.question(
                self, 'Confirmar',
                'Se fechar essa janela sua mira tambem sera fechada,' + 
                ' tem certeza que deseja fecha-la? caso' + 
                ' contrario basta responda não para deixar a mira',
                QtWidgets.QMessageBox.StandardButton.Yes,
                QtWidgets.QMessageBox.StandardButton.No
            )
            if conf == 16384:
                self.mira.destroy()
                os.system('taskkill /T /IM Python.exe /F')
            else:
                pass
    
    def gravar(self):
        config['tamanho'] = self.escala.value()
        config['posicao'] = [self.posX.value(), self.posY.value()]
        config['mira'] = f'./targets/MIRA-{self.mira_}.png'
        wJson = json.dumps(config)
        with open('save.json', 'w', encoding='utf-8') as js:
            js.write(wJson)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon('./targets/aim16.png'))
    form = App()
    form.setWindowTitle('AimCross')
    form.show()
    app.exec_()
