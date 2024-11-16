# main.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np  # Necessário para trabalhar com arrays numéricos
from point import Point
from vector import Vector
from plan import Plan
from car import Car

# Dimensões do canvas
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
    # Lista de pontos da pista
    pista_coords = []

    # 1. Reta inicial de (0,0) até (0,5)
    x1, y1 = transform_coords(0, 0)
    x2, y2 = transform_coords(0, 5)
    canvas.create_line(x1, y1, x2, y2, fill='gray', width=80, capstyle='round')
    pista_coords.append((x1, y1))
    pista_coords.append((x2, y2))

    # 2. Reta de (0,5) até (5,10)
    x3, y3 = transform_coords(5, 10)
    canvas.create_line(x2, y2, x3, y3, fill='gray', width=80, capstyle='round')
    pista_coords.append((x3, y3))

    # 3. Reta de (5,10) até (10,10)
    x4, y4 = transform_coords(10, 10)
    canvas.create_line(x3, y3, x4, y4, fill='gray', width=80, capstyle='round')
    pista_coords.append((x4, y4))

    # 4. Reta de (10,10) até (10,-5)
    x5, y5 = transform_coords(10, -5)
    canvas.create_line(x4, y4, x5, y5, fill='gray', width=80, capstyle='round')
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
    canvas.create_arc(bbox, start=0, extent=-180, style=tk.ARC, outline='gray', width=80)
    # Adicionar pontos da curva para a linha central
    angulos = np.linspace(0, np.pi, 100)
    curva_x = centro_x + raio * np.cos(angulos) 
    curva_y = centro_y + raio * np.sin(angulos)
    pista_coords.extend(zip(curva_x, curva_y))

    # 5. Reta final de (0,-5) até (0,0)
    x1, y1 = transform_coords(0, -5)
    x2, y2 = transform_coords(0, 0)
    canvas.create_line(x1, y1, x2, y2, fill='gray', width=80, capstyle='round')
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
    canvas.create_line(x_start1, y_start1, x_start2, y_start2, fill='black', width=5)

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
    root.title("Inserção de Pontos e Vetores")

    # Contadores para limitar pontos e vetores
    qtd_vetores = 0

    # Criar o notebook (abas)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill='both')

    # Criar frames para cada aba
    frame_pontos_vetores = tk.Frame(notebook)
    notebook.add(frame_pontos_vetores, text="Pontos e Vetores")

    # Criar o frame principal
    frame_pv_main = tk.Frame(frame_pontos_vetores)
    frame_pv_main.pack(expand=1, fill='both')

    # Dividir o frame principal em duas seções: esquerda e direita
    frame_esquerda = tk.Frame(frame_pv_main)
    frame_esquerda.pack(side='left', fill='both', expand=True)

    frame_direita = tk.Frame(frame_pv_main)
    frame_direita.pack(side='right', fill='both', expand=True)

    # Seção Esquerda: Canvas
    label_canvas_pv = tk.Label(frame_esquerda, text="Plano de Pontos e Vetores")
    label_canvas_pv.pack()
    canvas_pv = CanvasWrapper(criar_canvas(frame_esquerda))

    # Seção Direita: Inputs e Listas com Scrollbar
    # Criar um canvas para permitir a rolagem
    canvas_direita = tk.Canvas(frame_direita)
    scrollbar_direita = tk.Scrollbar(frame_direita, orient='vertical', command=canvas_direita.yview)
    canvas_direita.configure(yscrollcommand=scrollbar_direita.set)

    scrollbar_direita.pack(side='right', fill='y')
    canvas_direita.pack(side='left', fill='both', expand=True)

    # Criar um frame dentro do canvas_direita
    frame_direita_conteudo = tk.Frame(canvas_direita)
    canvas_direita.create_window((0, 0), window=frame_direita_conteudo, anchor='nw')

    # Ajustar o tamanho do canvas_direita conforme o conteúdo
    def atualizar_scroll(event):
        canvas_direita.configure(scrollregion=canvas_direita.bbox('all'))

    frame_direita_conteudo.bind('<Configure>', atualizar_scroll)

    # Inputs e Botões
    label_input = tk.Label(frame_direita_conteudo, text="Insira um Ponto ou Vetor (Ex: D(1,2) ou t=(3,4)):")
    label_input.pack(pady=5)
    entry_input = tk.Entry(frame_direita_conteudo)
    entry_input.pack(fill='x')

    btn_adicionar_pv = tk.Button(frame_direita_conteudo, text="Adicionar", command=lambda: adicionar_pv())
    btn_adicionar_pv.pack(pady=5)

    # Listas de Pontos e Vetores
    frame_pv_lists = tk.Frame(frame_direita_conteudo)
    frame_pv_lists.pack(fill='both', expand=True, padx=10, pady=10)

    # Lista de Pontos
    frame_pv_pontos = tk.Frame(frame_pv_lists)
    frame_pv_pontos.pack(side='left', fill='both', expand=True, padx=5)

    label_lista_pv_pontos = tk.Label(frame_pv_pontos, text="Lista de Pontos")
    label_lista_pv_pontos.pack()

    listbox_pv_pontos = tk.Listbox(frame_pv_pontos)
    listbox_pv_pontos.pack(expand=1, fill='both')

    # Lista de Vetores
    frame_pv_vetores = tk.Frame(frame_pv_lists)
    frame_pv_vetores.pack(side='right', fill='both', expand=True, padx=5)

    label_lista_pv_vetores = tk.Label(frame_pv_vetores, text="Lista de Vetores")
    label_lista_pv_vetores.pack()

    listbox_pv_vetores = tk.Listbox(frame_pv_vetores)
    listbox_pv_vetores.pack(expand=1, fill='both')

    # Listas para armazenar pontos e vetores desta aba
    pontos_pv = []
    vetores_pv = []
    objetos_pontos_canvas = []
    objetos_vetores_canvas = []

    # ------------------- Funções para Pontos e Vetores ------------------- #

    def update_car_on_canvas(car: Car):
        # Remove the old car representation
        # Find and remove the car's previous drawing
        for obj in objetos_pontos_canvas:
            if obj[1] == car.position.name:
                canvas_pv.plano.delete(obj[0])
                canvas_pv.plano.delete(obj[1])
                objetos_pontos_canvas.remove(obj)
                break
        # Draw the new position
        circulo, texto = desenhar_ponto_no_canvas(car.position, canvas_pv.plano)
        objetos_pontos_canvas.append((circulo, texto))
        
    def adicionar_pv():
        nonlocal qtd_vetores
        input_text = entry_input.get().strip()
        if not input_text:
            messagebox.showerror("Erro", "Insira um ponto ou vetor no formato correto.")
            return

        try:
            # Vetor no formato Nome=(x,y)
            var_name, coords = input_text.split('=')
            nome = var_name.strip()
            coords = coords.strip().strip('()')
            x_str, y_str = coords.split(',')
            x = float(x_str)
            y = float(y_str)

            vetor = Vector(Point(0, 0), Point(x, y), name=nome)

            vetores_pv.append(vetor)
            qtd_vetores += 1

            # Desenhar o vetor no canvas
            linha, texto = desenhar_vetor_no_canvas(vetor, canvas_pv.plano)
            objetos_vetores_canvas.append((linha, texto))

            atualizar_lista_pv_vetores()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar a entrada: {e}")
        finally:
            entry_input.delete(0, tk.END)

    def atualizar_lista_pv_pontos():
        listbox_pv_pontos.delete(0, tk.END)
        for i, ponto in enumerate(pontos_pv):
            nome = ponto.name if ponto.name else ''
            listbox_pv_pontos.insert(tk.END, f"{i+1}: {nome}({ponto.x}, {ponto.y})")

    def atualizar_lista_pv_vetores():
        listbox_pv_vetores.delete(0, tk.END)
        for i, vetor in enumerate(vetores_pv):
            dx = vetor.ponto_b.x
            dy = vetor.ponto_b.y
            nome = vetor.name if vetor.name else ''
            listbox_pv_vetores.insert(tk.END, f"{i+1}: {nome}({dx}, {dy})")

    player1_car = Car(position=Point(-1, 0, name="Player 1"), name="Player 1")
    player2_car = Car(position=Point(1, 0, name="Player 2"), name="Player 2")

    cars = [player1_car, player2_car]

    for car in cars:
        circulo, texto = desenhar_ponto_no_canvas(car.position, canvas_pv.plano)
        objetos_pontos_canvas.append((circulo, texto))

    pontos_pv = [car.position for car in cars]
    atualizar_lista_pv_pontos()


    def handle_player_input(car: Car):
        input_text = simpledialog.askstring("Input", f"{car.name}, enter your speed vector (dx,dy):")
        if input_text:
            try:
                dx_str, dy_str = input_text.strip().strip('()').split(',')
                dx = float(dx_str)
                dy = float(dy_str)
                new_speed = Vector(Point(0, 0), Point(dx, dy))
                car.update_speed(new_speed)
                car.move()
                # Update the car's position on the canvas
                update_car_on_canvas(car)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
                car.has_lost_turn = True
        else:
            car.has_lost_turn = True
            print(f"{car.name} did not enter a speed vector and loses the turn.")

            
    root.mainloop()
if __name__ == "__main__":
    main()
