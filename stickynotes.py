"""
Criado por Paulo Artur
Em junho de 2025

Stickynotes, uma aplicação estilo Microsoft Notepad escrito usando PyQt6.

É possível abrir um arquivo de texto usando Ctrl+O, Salvar um arquivo utilizando Ctrl+S.

Abrindo o programa pelo terminal, é possível oferecer como argumento o arquivo para o programa abrir/criar

Esse é o ponto de entrada da aplicação, o programa começa ser executado desse arquivo
"""

from estadoDaAplicação import EstadoDaAplicação
from pathlib import Path

from sys import argv

# pegar a pasta do script
pastaDoScript = Path(__file__).resolve().parent
print(pastaDoScript)

app = EstadoDaAplicação(argv) # criando uma instância de nossa aplicação

app.janelaPrincipal.show() # Mostrando a janela principal
app.exec() # Executando a aplicação
