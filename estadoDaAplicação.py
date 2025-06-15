"""
Criado por: Paulo Artur
em junho de 2025

Nesse arquivo será encontrado a classe que armazena o estado da aplicação, isso é,
a parte da aplicação que faz a interação com o sistema operacional e controla a interface gráfica.
"""

import os.path
import tempfile

from PyQt6.QtGui import QAction, QKeySequence, QShortcut
import visualização

from PyQt6.QtWidgets import QApplication, QFileDialog

class EstadoDaAplicação(QApplication):
    """
    Método __init__() no python sempre é o método que é chamado pelo construtor de algum objeto do tipo EstadoDaAplicação,
    dê uma olhada nas aulas de orientação à objetos para saber mais sobre classes, construtores e programação orientada à 
    objetos.
    """
    def __init__(self, argv):
        super().__init__(argv)
        self.janelaPrincipal = visualização.Visualização()
        self.inscreverEventos()
        # Caso for fornecido algum argumento para o programa e esse argumento começa com '/', significa que esse arquivo tem caminho absoluto
        # TODO: talvez isso não funcione no Windows
        if len(argv) > 1 and argv[1].startswith('/'):
            self.carregarArquivo(argv[1])
        # Caso for fornecdo algum argumento para o programa, não ligo para a estrutura desse arquivo e abro um arquivo temporário
        elif len(argv) > 1:
            self.carregarArquivo(os.getcwd() + "/" + argv[1])
        # Caso não for fornecido nenhum argumento para o programa
        else:
            self.carregarArquivo("")

    """
    Inscrição de eventos e atalhos
    """
    def inscreverEventos(self):
        self.janelaPrincipalAtiva = True # variável não usada
        self.açãoSalvarArquivo = QShortcut(QKeySequence('Ctrl+S'), self.janelaPrincipal.blocoDeNotas)
        self.açãoAbrirArquivo = QShortcut(QKeySequence('Ctrl+O'), self.janelaPrincipal.blocoDeNotas)
        self.açãoAbrirArquivo.activated.connect(self.abrirArquivo)
        self.açãoSalvarArquivo.activated.connect(self.salvarArquivo)

        self.janelaPrincipal.blocoDeNotas.textChanged.connect(self.callbackDeQuandoOTextoMuda)

    """
    Toda vez que um usuário digitar alguma coisa, essa função será executada
    """
    def callbackDeQuandoOTextoMuda(self):
        self.conteúdoNaRAM = self.janelaPrincipal.blocoDeNotas.toPlainText()

    """
    Função responsável por carregar algum arquivo do disco
    """
    def carregarArquivo(self, caminhoDoArquivo):
        if caminhoDoArquivo == "":
            self.éTemporário = True
            self.arquivo = tempfile.TemporaryFile(mode='a+')
        else:
            self.éTemporário = False
            self.arquivo = open(caminhoDoArquivo, "a+")
        self.arquivo.seek(0)
        self.conteúdoNaRAM = self.conteúdoNoHD = self.arquivo.read()
        self.janelaPrincipal.blocoDeNotas.setPlainText(self.conteúdoNaRAM)

    """
    Cria uma caixa de diálogo sobre abertura de arquivo
    """
    def abrirArquivo(self):
        self.janelaPrincipalAtiva = False
        caminhoDoArquivo, _ = QFileDialog.getOpenFileName(self.janelaPrincipal, "Abrir Arquivo", "Todos os Arquivos (*)")
        if caminhoDoArquivo:
            print(caminhoDoArquivo)
            self.arquivo.close()
            self.carregarArquivo(caminhoDoArquivo)
        self.janelaPrincipalAtiva = True

    def salvarArquivo(self):
        # caso não é um arquivo temporário, ele salva no arquivo já aberto
        if not self.éTemporário:
            self.arquivo.truncate(0)
            self.arquivo.seek(0)
            self.arquivo.write(self.conteúdoNaRAM)
            self.conteúdoNoHD = self.conteúdoNaRAM
        # caso for arquivo temporário, cria uma caixa de diálogo para criação de um novo arquivo com o conteúdo digitado
        else:
            self.janelaPrincipalAtiva = False # variável não utilizada
            caminhoDoArquivo, _ = QFileDialog.getSaveFileName(self.janelaPrincipal, "Salvar Novo Arquivo", "Todos os Arquivos (*)")
            if caminhoDoArquivo:
                self.éTemporário = False
                self.arquivo.close()
                with open(caminhoDoArquivo, "w") as f:
                    f.write(self.conteúdoNaRAM)
                    f.close()
                    self.carregarArquivo(caminhoDoArquivo)
            self.janelaPrincipalAtiva = True # variável não utilizada
