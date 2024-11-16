import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np  # Necessário para trabalhar com arrays numéricos
from point import Point
from vector import Vector
from plan import Plan
from car import Car

#Dimensões do canvas
canvas_width = 800
canvas_height = 800
scale = 20  # Escala para converter unidades de coordenadas para pixels

# Ponto médio do canvas
mid_x = canvas_width / 2
mid_y = canvas_height / 2

def transform_coords(x, y):
    """Transforma coordenadas matemáticas em coordenadas do canvas."""
    x_canvas = mid_x + x * scale
    y_canvas = mid_y - y * scale  # Inverte o eixo Y
    return x_canvas, y_canvas

class CanvasWrapper:
    def __init__(self, plano):
        self.plano = plano

def criar_canvas(aba):
    canvas = tk.Canvas(aba, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack(expand=True, fill='both')
    desenhar_pista(canvas)
    desenhar_grade(canvas)
    return canvas

def desenhar_grade(canvas):
    # Desenhar linhas de grade
    cor_grade = '#cccccc'
    
    # Desenhar linhas de grade verticais
    for x in range(-int(canvas_width / (2 * scale)), int(canvas_width / (2 * scale)) + 1):
        x_canvas, _ = transform_coords(x, 0)
        canvas.create_line(
            x_canvas, 0, x_canvas, canvas_height,
            fill=cor_grade,
            width=1,
            dash=(2, 4)  # Opcional: linhas tracejadas para suavizar a aparência
        )
    
    # Desenhar linhas de grade horizontais
    for y in range(-int(canvas_height / (2 * scale)), int(canvas_height / (2 * scale)) + 1):
        _, y_canvas = transform_coords(0, y)
        canvas.create_line(
            0, y_canvas, canvas_width, y_canvas,
            fill=cor_grade,
            width=1,
            dash=(2, 4)  # Opcional: linhas tracejadas para suavizar a aparência
        )

# Função para desenhar a pista de corrida personalizada no canvas do Tkinter
def desenhar_pista(canvas):
    global ids_pista, largada  # IDs das linhas da pista
    ids_pista = []

    # Lista de pontos da pista
    pista_coords = []

    # 1. Reta inicial de (0,0) até (0,5)
    x1, y1 = transform_coords(0, 0)
    x2, y2 = transform_coords(0, 5)
    id = canvas.create_line(x1, y1, x2, y2, fill='gray', width=80, capstyle='round')
    ids_pista.append(id)
    pista_coords.append((x1, y1))
    pista_coords.append((x2, y2))

    # 2. Reta de (0,5) até (5,10)
    x3, y3 = transform_coords(5, 10)
    id = canvas.create_line(x2, y2, x3, y3, fill='gray', width=80, capstyle='round')
    ids_pista.append(id)
    pista_coords.append((x3, y3))

    # 3. Reta de (5,10) até (10,10)
    x4, y4 = transform_coords(10, 10)
    id = canvas.create_line(x3, y3, x4, y4, fill='gray', width=80, capstyle='round')
    ids_pista.append(id)
    pista_coords.append((x4, y4))

    # 4. Reta de (10,10) até (10,-5)
    x5, y5 = transform_coords(10, -5)
    id = canvas.create_line(x4, y4, x5, y5, fill='gray', width=80, capstyle='round')
    ids_pista.append(id)
    pista_coords.append((x5, y5))

    # 5. Curva final retornando ao ponto de largada (0,0)
    # Parâmetros da curva
    raio = 5 * scale
    centro_x, centro_y = transform_coords(5, -5)
    bbox = [
        centro_x - raio,
        centro_y - raio,
        centro_x + raio,
        centro_y + raio
    ]
    # Desenhar arco (semicírculo)
    id = canvas.create_arc(bbox, start=0, extent=-180, style=tk.ARC, outline='gray', width=80)
    ids_pista.append(id)

    # Adicionar pontos da curva para a linha central
    angulos = np.linspace(0, np.pi, 100)
    curva_x = centro_x + raio * np.cos(angulos) 
    curva_y = centro_y + raio * np.sin(angulos)
    pista_coords.extend(zip(curva_x, curva_y))

    # 5. Reta final de (0,-5) até (0,0)
    x1, y1 = transform_coords(0, -5)
    x2, y2 = transform_coords(0, 0)
    id = canvas.create_line(x1, y1, x2, y2, fill='gray', width=80, capstyle='round')
    ids_pista.append(id)

    pista_coords.append((x1, y1))
    pista_coords.append((x2, y2))

    # Desenhar linha central
    for i in range(len(pista_coords) - 1):
        canvas.create_line(
            pista_coords[i][0], pista_coords[i][1],
            pista_coords[i+1][0], pista_coords[i+1][1],
            fill='white', width=2, dash=(5, 5)
        )

    # Desenhar linha de largada
    x_start1, y_start1 = transform_coords(2, 0)
    x_start2, y_start2 = transform_coords(-2, 0)
    largada = canvas.create_line(x_start1, y_start1, x_start2, y_start2, fill='black', width=5)

def desenhar_ponto_no_canvas(ponto, canvas):
    x_canvas, y_canvas = transform_coords(ponto.x, ponto.y)
    # Desenhar o ponto no canvas
    circulo = canvas.create_oval(x_canvas - 5, y_canvas - 5, x_canvas + 5, y_canvas + 5, fill='blue')
    label = f'{ponto.name}({ponto.x}, {ponto.y})' if ponto.name else f'({ponto.x}, {ponto.y})'
    texto = canvas.create_text(x_canvas + 15, y_canvas, text=label, fill='black')
    return circulo, texto

def desenhar_vetor_no_canvas(vetor, canvas):
    x_start, y_start = transform_coords(vetor.ponto_a.x, vetor.ponto_a.y)
    x_end, y_end = transform_coords(vetor.ponto_b.x, vetor.ponto_b.y)
    # Desenhar o vetor no canvas
    linha = canvas.create_line(x_start, y_start, x_end, y_end, fill='red', width=2, arrow=tk.LAST)
    # Calcular posição média para exibir o nome do vetor
    mid_x = (x_start + x_end) / 2
    mid_y = (y_start + y_end) / 2
    label = vetor.name if vetor.name else ''
    texto = canvas.create_text(mid_x, mid_y - 10, text=label, fill='black')
    return linha, texto

def main():
    plan = Plan()  # Inicializando o plano

    root = tk.Tk()
    root.title("Jogo de Corrida")

    # Contadores para limitar pontos e vetores
    qtd_vetores = 0

    # Criar o notebook (abas)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill='both')

    # Criar frames para cada aba
    frame_jogo = tk.Frame(notebook)
    notebook.add(frame_jogo, text="Jogo de Corrida")

    # Criar o frame principal
    frame_jogo_main = tk.Frame(frame_jogo)
    frame_jogo_main.pack(expand=1, fill='both')

    # Dividir o frame principal em duas seções: esquerda e direita
    frame_esquerda = tk.Frame(frame_jogo_main)
    frame_esquerda.pack(side='left', fill='both', expand=True)

    frame_direita = tk.Frame(frame_jogo_main)
    frame_direita.pack(side='right', fill='both', expand=True)

    # Seção Esquerda: Canvas
    label_canvas_jogo = tk.Label(frame_esquerda, text="Pista de Corrida")
    label_canvas_jogo.pack()
    canvas_jogo = CanvasWrapper(criar_canvas(frame_esquerda))

    # Desenhar a pista (por exemplo, linhas de chegada e partida)
    desenhar_pista(canvas_jogo.plano)

    # Lista de carros
    carros = []

    # Criar os dois carros
    player1_car = Car(position=Point(-1, 0, name="Player 1"), name="Player 1")
    player2_car = Car(position=Point(1, 0, name="Player 2"), name="Player 2")
    carros.append(player1_car)
    carros.append(player2_car)

    # Desenhar os carros no canvas
    objetos_carros_canvas = []
    for car in carros:
        circulo, texto = desenhar_ponto_no_canvas(car.position, canvas_jogo.plano)
        objetos_carros_canvas.append((circulo, texto))

    # Seção Direita: Inputs e Informações
    label_info = tk.Label(frame_direita, text="Informações do Jogo")
    label_info.pack()

    # Frame para informações dos jogadores
    frame_info_jogadores = tk.Frame(frame_direita)
    frame_info_jogadores.pack(pady=10)

    # Labels para mostrar informações dos jogadores
    labels_jogadores = []
    for car in carros:
        label = tk.Label(frame_info_jogadores, text=f"{car.name}: Posição ({car.position.x}, {car.position.y}), Velocidade (0,0)")
        label.pack()
        labels_jogadores.append(label)

    # Campo de input para o vetor de movimento
    label_input = tk.Label(frame_direita, text="Insira o vetor de movimento (dx,dy):")
    label_input.pack(pady=5)
    entry_input = tk.Entry(frame_direita)
    entry_input.pack(fill='x')

    # Botão para enviar o movimento
    btn_mover = tk.Button(frame_direita, text="Mover", command=lambda: mover_carro())
    btn_mover.pack(pady=5)

    # Variável para controlar o turno (0 para player1, 1 para player2)
    turno = [0]

    # Função para atualizar as informações dos jogadores
    def atualizar_info_jogadores():
        for i, car in enumerate(carros):
            labels_jogadores[i].config(text=f"{car.name}: Posição ({car.position.x}, {car.position.y}), Velocidade ({car.speed.ponto_b.x}, {car.speed.ponto_b.y})")

    # Função para mover o carro
    def mover_carro():
        # Obter o carro do jogador atual
        car = carros[turno[0]]
        print(turno[0])

        input_text = entry_input.get().strip()
        if not input_text:
            messagebox.showerror("Erro", "Insira um vetor no formato (dx,dy).")
            return

        try:
            dx_str, dy_str = input_text.strip().strip('()').split(',')
            dx = float(dx_str)
            dy = float(dy_str)
            print(dx, dy)
            new_speed = Vector(Point(0, 0), Point(dx, dy))

            initial_x = car.position.x
            initial_y = car.position.y

            # Tentar atualizar a velocidade do carro
            car.update_speed(new_speed)

            if car.has_lost_turn:
                messagebox.showinfo("Perdeu a Vez", f"{car.name} inseriu um vetor inválido e perdeu a vez!")
                car.has_lost_turn = False  # Resetar o flag para o próximo turno
            else:
                # Mover o carro
                car.move()

                # Verificar colisão com as paredes (implementar a lógica conforme sua pista)
                if verificar_colisao_parede(car.position):
                    car.reset_speed_on_collision()
                    messagebox.showinfo("Colisão", f"{car.name} colidiu com a parede e sua velocidade foi resetada para (0,0)!")
                elif verificar_colisao_carros(turno[0], car.position): 
                    car.reset_speed_on_collision()
                    messagebox.showinfo("Colisão", f"{car.name} colidiu com outro carro e perdeu o turno")
                    car.position.x = initial_x
                    car.position.y = initial_y
                else:
                    # Atualizar a posição do carro no canvas
                    atualizar_carro_no_canvas(car, objetos_carros_canvas[turno[0]])
        
                    # Verificar se o carro cruzou a linha de chegada
                    if verificar_linha_chegada(initial_x, initial_y, car.position):
                        messagebox.showinfo("Vencedor", f"{car.name} cruzou a linha de chegada e venceu a corrida!")
                        root.destroy()  # Fecha o jogo
                        return

            # Limpar o campo de input
            entry_input.delete(0, tk.END)

            # Alternar o turno para o próximo jogador
            turno[0] = (turno[0] + 1) % len(carros)

            # Atualizar as informações dos jogadores
            atualizar_info_jogadores()

        except Exception as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    # Função para atualizar o carro no canvas
    def atualizar_carro_no_canvas(car, objetos_canvas):
        circulo, texto = objetos_canvas

        # Remover o círculo e o texto antigos
        canvas_jogo.plano.delete(circulo)
        canvas_jogo.plano.delete(texto)

        # Desenhar o novo círculo e texto
        novo_circulo, novo_texto = desenhar_ponto_no_canvas(car.position, canvas_jogo.plano)
        objetos_carros_canvas[turno[0]] = (novo_circulo, novo_texto)


    def verificar_colisao_parede(posicao):
        """Verifica se o carro colidiu com as bordas da pista."""
        # Converter a posição do carro para coordenadas de canvas
        x_canvas, y_canvas = transform_coords(posicao.x, posicao.y)

        # Definir uma pequena área ao redor do ponto para verificar colisão
        overlapping_items = canvas_jogo.plano.find_overlapping(
            x_canvas, y_canvas,
            x_canvas, y_canvas
        )

        # Verificar se algum dos itens sobrepostos é parte das linhas da pista
        for item in overlapping_items:
            if item in ids_pista:  # IDs da pista registrados ao desenhar
                return False  # Colisão detectada
        return True  # Sem colisão

    def verificar_colisao_carros(index, position):
        if index == 0:
            return False
        print(index, index -1)
        if position.x == carros[index-1].position.x and  position.y == carros[index-1].position.y:
            return True


    def verificar_linha_chegada(x_inicial, y_inicial, posicao):
        # Verifica se os pontos inicial e final estão na faixa de x entre -2 e 2
        if (-2 <= x_inicial <= 2) and (-2 <= posicao.x <= 2):
            # Verifica se houve cruzamento no eixo y, de negativo para positivo
            if y_inicial < 0.0 and posicao.y >= 0.0:
                return True

        return False

    root.mainloop()

if __name__ == "__main__":
    main()
