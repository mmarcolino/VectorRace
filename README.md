# VectorRace

Este projeto é uma aplicação em Python para manipulação de pontos e vetores em um plano cartesiano, com interface gráfica construída usando `Tkinter`. A aplicação permite inserir, editar, deletar e visualizar pontos e vetores em um canvas, além de fornecer uma pista de corrida para ilustrar as operações.

## 1. Instalação e Execução

### Passos para rodar o projeto:

#### 1.1. Clonar o Repositório
Se você ainda não possui o repositório, clone-o usando:
```bash
git clone https://github.com/usuario/projeto-vetores.git
```

#### 1.2. Instalar as Dependências
O projeto utiliza bibliotecas externas como matplotlib para visualização gráfica e tkinter para a interface de usuário. Siga as instruções de acordo com o seu sistema operacional para instalar as dependências necessárias.

Linux/Mac:

- Verifique se você tem o Python 3 instalado:
    ```bash
    python3 --version
    ```
- Instale Tkinter (caso não esteja instalado):
    ```bash
    sudo apt-get install python3-tk
    ```
    Para Mac:
    ```bash
    brew install python-tk
    ```

Windows:
- Verifique se você tem o Python 3 instalado:
    ```bash
    python --version
    ```
- Instale Tkinter (caso não esteja instalado):
    ```bash
    pip install tk
    ```

#### 1.3. Executar o Projeto
Uma vez instaladas as dependências, execute o arquivo main.py para iniciar a aplicação.

    ```bash
    python3 main.py  # Linux/Mac
    ```

    ```bash
    python main.py  # Windows
    ```

## 2. Principais Entidades do Programa
O programa trabalha com três entidades principais:
#### 2.1. Point
 - Descrição: Representa um ponto no plano cartesiano, identificado por suas coordenadas ```(x, y)``` e um nome opcional.
 - Atributos: 
    - ```x```: Coordenada X do ponto.
    - ```y```: Coordenada Y do ponto.
    - ```name```: Nome opcional para identificar o ponto.

#### 2.2. Vector
 - Descrição: Representa um vetor definido por dois pontos, o ponto de origem ```ponto_a``` e o ponto de destino ```ponto_b```.
 - Atributos: 
    - ```ponto_a```: Ponto inicial do vetor (objeto da classe ```Point```).
    - ```ponto_b```:  Ponto final do vetor (objeto da classe ```Point```).
    - ```name```: Nome opcional para identificar o vetor.

#### 2.3. Plan
 - Descrição: Representa o plano cartesiano que contém os pontos e vetores. Ele gerencia a adição e remoção de pontos e vetores.
 - Atributos: 
    - ```points```: Lista de objetos ```Point``` adicionados ao plano.
    - ```vectors```: Lista de objetos``` Vector``` adicionados ao plano.