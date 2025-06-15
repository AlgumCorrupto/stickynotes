"""
Criado por: Paulo Artur
em junho de 2025

Esse arquivo encontra-se a janela principal da aplicação e seus elementos e funcionalidades gráficas
"""

import sys
from PyQt6.QtGui import QAction, QColor, QFont, QFontDatabase, QKeySequence, QPalette, QShortcut, QTextFrame
from PyQt6.QtWidgets import QApplication, QBoxLayout, QFrame, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit
from PyQt6.QtCore import Qt
import random
from pathlib import Path

class Visualização(QMainWindow):
    possíveisCores = [
        QColor("#d5a0e6"),
        QColor("#f63d9b"),
        QColor("#f8ce3c"),
        QColor("#54cbf5"),
        QColor("#c1e640"),
        QColor("#f6a01b")
    ]
    FATOR_DE_ZOOM = 4

    """
    Método que será executado quando a janela principal for construída.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint) # fazer que a janela quando criada não entre como tela cheia por padrão
        self.layoutPrincipal = QVBoxLayout()
        self.containerDoLayout = QWidget()
        self.containerDoLayout.setLayout(self.layoutPrincipal)

        self.blocoDeNotas = QPlainTextEdit()

        self.escolherEstilo()
        self.inscreverAtalhos()
        self.setCentralWidget(self.blocoDeNotas)

    """
    Método responsável por estilizar a janela com cores aleatóriamente selecionadas e escolher a fonte do programa
    """
    def escolherEstilo(self):
        # escolhendo a fonte
        pastaDoScript = Path(__file__).resolve().parent
        idDaFonte = QFontDatabase.addApplicationFont(str(pastaDoScript /  "Comic_Neue/ComicNeue-Regular.ttf"))
        familia = QFontDatabase.applicationFontFamilies(idDaFonte)[0]
        fonte = QFont(familia, 16)
        self.blocoDeNotas.setFont(fonte)

        self.blocoDeNotas.setFrameStyle(QFrame.Shape.NoFrame)# tirando a borda
        # escolhendo a paleta de cores
        random.seed()

        corDoFundo = self.possíveisCores[random.randint(0, len(self.possíveisCores) - 1)] 
        corDoTexto = corDoFundo.darker(300) 

        paleta = QPalette()
        paleta.setColor(QPalette.ColorRole.Base, corDoFundo)
        paleta.setColor(QPalette.ColorRole.Text, corDoTexto)
        paleta.setColor(QPalette.ColorRole.Highlight, corDoTexto)
        paleta.setColor(QPalette.ColorRole.HighlightedText, corDoFundo)

        self.blocoDeNotas.setAutoFillBackground(True)
        self.blocoDeNotas.setPalette(paleta)

    """
    Nesse método são registrados alguns atalhos
    """
    def inscreverAtalhos(self):
        self.açãoAumentarZoom = QShortcut(QKeySequence('Ctrl++'), self.blocoDeNotas)
        self.açãoDiminuirZoom = QShortcut(QKeySequence('Ctrl+-'), self.blocoDeNotas)
        self.açãoAumentarZoom.activated.connect(self.aumentarZoom)
        self.açãoDiminuirZoom.activated.connect(self.diminuirZoom)

    """
    Callbacks para aumentar e diminuir o zoom do texto

    Callbacks são funções que são executadas quando algum evento da inteface gráfica acontecer, como o pressionamento de algum botão
    """
    def aumentarZoom(self):
        fonte = self.blocoDeNotas.font()
        fonte.setPointSize(fonte.pointSize() + self.FATOR_DE_ZOOM)
        self.blocoDeNotas.setFont(fonte)
    def diminuirZoom(self):
        fonte = self.blocoDeNotas.font()
        fonte.setPointSize(fonte.pointSize() - self.FATOR_DE_ZOOM)
        self.blocoDeNotas.setFont(fonte)


