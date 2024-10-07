# main.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from point import Point
from vector import Vector
from plan import Plan

import numpy as np  # Necessário para trabalhar com arrays numéricos

# Adicionar o Canvas para o plano cartesiano
canvas_width = 300  # Reduzido para melhor se ajustar a telas menores
canvas_height = 300

class Canvas:
    def __init__(self, plano):
        self.plano = plano

def criar_canvas(aba):
    canvas = tk.Canvas(aba, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack(expand=True, fill='both')
    desenhar_plano_cartesiano(canvas)
    return canvas

def desenhar_plano_cartesiano(canvas):
    # Limpar o canvas
    canvas.delete("all")
    
    # Desenhar os eixos
    mid_x = canvas_width / 2
    mid_y = canvas_height / 2
    scale = 20  # Escala para o plano de 6x6

    # Eixo X
    canvas.create_line(0, mid_y, canvas_width, mid_y, fill='black', width=2)
    # Eixo Y
    canvas.create_line(mid_x, 0, mid_x, canvas_height, fill='black', width=2)

    # Linhas de grade e marcas
    for i in range(-6, 7):
        if i != 0:
            # Linhas verticais
            canvas.create_line(mid_x + i * scale, 0, mid_x + i * scale, canvas_height, fill='lightgray')
            # Linhas horizontais
            canvas.create_line(0, mid_y - i * scale, canvas_width, mid_y - i * scale, fill='lightgray')

    # Marcas nos eixos
    for i in range(-6, 7):
        if i != 0:
            canvas.create_text(mid_x + i * scale, mid_y + 10, text=str(i), fill='black')
            canvas.create_text(mid_x + 10, mid_y - i * scale, text=str(i), fill='black')

    # Desenhar o ponto (0,0)
    canvas.create_oval(mid_x - 5, mid_y - 5, mid_x + 5, mid_y + 5, fill='black')
    

# Função para desenhar a pista de corrida personalizada
def desenhar_pista(ax):
    # Coordenadas da pista
    pista_x = []
    pista_y = []

    # 1. Reta inicial a partir de (0,0) até (0,5)
    pista_x.extend([0, 0])
    pista_y.extend([0, 5])

    # 2.  Pequena reta de (0,5) até (5,10)
    pista_x.extend([0, 5])
    pista_y.extend([5, 10])

    # 3. Pequena reta de (5,10) até (10,10)
    pista_x.extend([5, 10])
    pista_y.extend([10, 10])

    # 4. Pequena reta de (10,10) até (10,-5)
    pista_x.extend([10, 10])
    pista_y.extend([10, -5])

    # 5. Curva final retornando ao ponto de largada (0,0)
    angulos2 = np.linspace(0, np.pi, 100)
    raio2 = 5
    centro_x2 = 5
    centro_y2 = -5
    curva_x3 = centro_x2 + raio2 * np.cos(angulos2)
    curva_y3 = centro_y2 - raio2 * np.sin(angulos2)
    pista_x.extend(curva_x3)
    pista_y.extend(curva_y3)

    # Fechar a pista conectando ao ponto inicial
    pista_x.append(0)
    pista_y.append(0)

    # Desenhar a pista
    ax.plot(pista_x, pista_y, color='gray', linewidth=20, solid_capstyle='round', zorder=1)

    # Adicionar linha central para indicar o caminho
    ax.plot(pista_x, pista_y, color='white', linewidth=2, linestyle='--', zorder=2)

    # Adicionar a linha de largada no ponto (0,0)
    ax.plot([-0.5, 0.5], [0, 0], color='black', linewidth=5)

def desenhar_pontos(pontos):
    fig, ax = plt.subplots()
    ax.set_xlim(-5, 25)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal')  # Manter a proporção dos eixos
    ax.axis('off')  # Opcional: remover os eixos para destacar a pista

    # Desenhar a pista de corrida
    desenhar_pista(ax)

    # Plotar pontos
    for ponto in pontos:
        ax.plot(ponto.x, ponto.y, 'bo')  # pontos azuis
        label = f'{ponto.name}({ponto.x}, {ponto.y})' if ponto.name else f'({ponto.x}, {ponto.y})'
        ax.text(ponto.x + 0.5, ponto.y + 0.5, label)

    plt.title("Plano de Pontos com Pista de Corrida")
    plt.show()

def desenhar_vetores(vetores):
    fig, ax = plt.subplots()
    ax.set_xlim(-5, 25)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal')  # Manter a proporção dos eixos
    ax.axis('off')  # Opcional: remover os eixos para destacar a pista

    # Desenhar a pista de corrida
    desenhar_pista(ax)

    # Plotar vetores
    for vetor in vetores:
        ax.quiver(vetor.ponto_a.x, vetor.ponto_a.y,
                  vetor.ponto_b.x - vetor.ponto_a.x,
                  vetor.ponto_b.y - vetor.ponto_a.y,
                  angles='xy', scale_units='xy', scale=1, color='r')
        # Calcular posição média para exibir o nome do vetor
        mid_x = (vetor.ponto_a.x + vetor.ponto_b.x) / 2
        mid_y = (vetor.ponto_a.y + vetor.ponto_b.y) / 2
        label = vetor.name if vetor.name else ''
        ax.text(mid_x, mid_y, label)

    plt.title("Plano de Vetores com Pista de Corrida")
    plt.show()

def desenhar_pontos_vetores(pontos, vetores):
    fig, ax = plt.subplots()
    ax.set_xlim(-5, 25)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal')  # Manter a proporção dos eixos
    ax.axis('off')  # Opcional: remover os eixos para destacar a pista

    # Desenhar a pista de corrida
    desenhar_pista(ax)

    # Plotar pontos
    for ponto in pontos:
        ax.plot(ponto.x, ponto.y, 'bo')  # pontos azuis
        label = f'{ponto.name}({ponto.x}, {ponto.y})' if ponto.name else f'({ponto.x}, {ponto.y})'
        ax.text(ponto.x + 0.5, ponto.y + 0.5, label)

    # Plotar vetores
    for vetor in vetores:
        ax.quiver(0, 0, vetor.ponto_b.x, vetor.ponto_b.y, angles='xy', scale_units='xy', scale=1, color='r')
        # Exibir o nome do vetor próximo à sua extremidade
        label = vetor.name if vetor.name else ''
        ax.text(vetor.ponto_b.x, vetor.ponto_b.y, label)

    plt.title("Plano de Pontos e Vetores com Pista de Corrida")
    plt.show()

def main():
    plan = Plan()  # Inicializando o plano

    root = tk.Tk()
    root.title("Inserção de Pontos e Vetores")

    # Contadores para limitar pontos e vetores
    qtd_pontos = 0
    qtd_vetores = 0

    # Variáveis para controlar o modo de edição
    editando_ponto = False
    editando_vetor = False
    indice_ponto_editando = None
    indice_vetor_editando = None

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

    # Seção Esquerda: Canvases
    label_canvas_pontos = tk.Label(frame_esquerda, text="Plano de Pontos")
    label_canvas_pontos.pack()
    canvas_pontos_pv = Canvas(criar_canvas(frame_esquerda))
    indices_pontos_canvas_pv = []

    label_canvas_vetores = tk.Label(frame_esquerda, text="Plano de Vetores")
    label_canvas_vetores.pack()
    canvas_vetores_pv = Canvas(criar_canvas(frame_esquerda))
    indices_vetores_canvas_pv = []

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

    btn_editar_pv_ponto = tk.Button(frame_pv_pontos, text="Editar Ponto", command=lambda: editar_pv_ponto())
    btn_editar_pv_ponto.pack(pady=5)

    btn_deletar_pv_ponto = tk.Button(frame_pv_pontos, text="Deletar Ponto", command=lambda: deletar_pv_ponto())
    btn_deletar_pv_ponto.pack(pady=5)

    # Lista de Vetores
    frame_pv_vetores = tk.Frame(frame_pv_lists)
    frame_pv_vetores.pack(side='right', fill='both', expand=True, padx=5)

    label_lista_pv_vetores = tk.Label(frame_pv_vetores, text="Lista de Vetores")
    label_lista_pv_vetores.pack()

    listbox_pv_vetores = tk.Listbox(frame_pv_vetores)
    listbox_pv_vetores.pack(expand=1, fill='both')

    btn_editar_pv_vetor = tk.Button(frame_pv_vetores, text="Editar Vetor", command=lambda: editar_pv_vetor())
    btn_editar_pv_vetor.pack(pady=5)

    btn_deletar_pv_vetor = tk.Button(frame_pv_vetores, text="Deletar Vetor", command=lambda: deletar_pv_vetor())
    btn_deletar_pv_vetor.pack(pady=5)

    # Botão para exibir o plano
    btn_exibir_pv = tk.Button(frame_direita_conteudo, text="Exibir Plano", command=lambda: exibir_plano_pv())
    btn_exibir_pv.pack(pady=5)

    # Listas para armazenar pontos e vetores desta aba
    pontos_pv = []
    vetores_pv = []

    # ------------------- Funções para Pontos e Vetores ------------------- #

    def desenhar_vetor_no_canvas(vetor, canvas) -> int:
        mid_x = canvas_width / 2
        mid_y = canvas_height / 2
        scale = 20  # Escala para o plano de 6x6

        return canvas.create_line(mid_x + vetor.ponto_a.x * scale, mid_y - vetor.ponto_a.y * scale,
                        mid_x + vetor.ponto_b.x * scale, mid_y - vetor.ponto_b.y * scale, fill='red', width=2)
            
    def desenhar_ponto_no_canvas(ponto, canvas) -> str:
        mid_x = canvas_width / 2
        mid_y = canvas_height / 2
        scale = 20  # Escala para o plano de 6x6

        # Desenhar o ponto no canvas
        circulo = canvas.create_oval(mid_x + ponto.x * scale - 5, mid_y - ponto.y * scale - 5,
                        mid_x + ponto.x * scale + 5, mid_y - ponto.y * scale + 5,
                        fill='blue')
        label = f'{ponto.name}({ponto.x}, {ponto.y})' if ponto.name else f'({ponto.x}, {ponto.y})'
        texto = canvas.create_text(mid_x + ponto.x * scale + 8, mid_y - ponto.y * scale, text=label, fill='black')
        
        return str(str(circulo) + "-" + str(texto))

    def adicionar_pv():
        nonlocal qtd_pontos, qtd_vetores, editando_vetor, editando_ponto, indice_vetor_editando, indice_ponto_editando
        input_text = entry_input.get().strip()
        if not input_text:
            messagebox.showerror("Erro", "Insira um ponto ou vetor no formato correto.")
            return
        
        try:
            if '=' in input_text:
                # Vetor no formato Nome=(x,y)
                var_name, coords = input_text.split('=')
                nome = var_name.strip()
                coords = coords.strip().strip('()')
                x_str, y_str = coords.split(',')
                x = float(x_str)
                y = float(y_str)
                
                vetor = Vector(Point(0, 0), Point(x, y), name=nome)

                if editando_vetor:
                    vetores_pv[indice_vetor_editando] = vetor
                    messagebox.showinfo("Sucesso", "Vetor atualizado.")
                    btn_adicionar_pv.config(text="Adicionar")
                    editando_vetor = False
                    indice_vetor_editando = None
                    
                    for n in indices_vetores_canvas_pv:
                        canvas_vetores_pv.plano.delete(n)
                    
                    indices_vetores_canvas_pv.clear()    
                    
                    for v in vetores_pv:
                        indices_vetores_canvas_pv.append(desenhar_vetor_no_canvas(v, canvas_vetores_pv.plano))
                
                else:  
                    if qtd_vetores >= 4:
                        messagebox.showerror("Erro", "Limite de 4 vetores atingido.")
                        return
                    
                    vetores_pv.append(vetor)
                    indices_vetores_canvas_pv.append(desenhar_vetor_no_canvas(vetor, canvas_vetores_pv.plano))
                    qtd_vetores += 1
                    messagebox.showinfo("Sucesso", f"Vetor {nome}({x}, {y}) adicionado.")

                
                atualizar_lista_pv_vetores()
            else:
                # Ponto no formato Nome(x,y)
                var_name, coords = input_text.split('(')
                nome = var_name.strip()
                coords = coords.strip().strip(')')
                x_str, y_str = coords.split(',')
                x = float(x_str)
                y = float(y_str)
                
                ponto = Point(x, y, name=nome)

                if editando_ponto:
                    pontos_pv[indice_ponto_editando] = ponto
                    messagebox.showinfo("Sucesso", "Ponto atualizado.")
                    btn_adicionar_pv.config(text="Adicionar")
                    editando_ponto = False
                    indice_ponto_editando = None
                    
                    for n in indices_pontos_canvas_pv:
                        formatAndText = str.split(n, "-")
                        canvas_pontos_pv.plano.delete(formatAndText[0])
                        canvas_pontos_pv.plano.delete(formatAndText[1])
                    
                    indices_pontos_canvas_pv.clear()    
                    
                    for p in pontos_pv:
                        indices_pontos_canvas_pv.append(desenhar_ponto_no_canvas(p, canvas_pontos_pv.plano))

                    
                else: 
                    if qtd_pontos >= 5:
                        messagebox.showerror("Erro", "Limite de 5 pontos atingido.")
                        return
                    
                    pontos_pv.append(ponto)
                    indices_pontos_canvas_pv.append(desenhar_ponto_no_canvas(ponto, canvas_pontos_pv.plano))
                    qtd_pontos += 1

                    messagebox.showinfo("Sucesso", f"Ponto {nome}({x}, {y}) adicionado.")
                
                atualizar_lista_pv_pontos()
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


    def editar_pv_ponto():
        nonlocal editando_ponto, indice_ponto_editando
        selected_index = listbox_pv_pontos.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Selecione um ponto para editar.")
            return
        index = selected_index[0]

        ponto = pontos_pv[index]
        entry_input.insert(0, str(ponto.name + "(") + str(ponto.x) + "," + str(ponto.y) + ")")
        
        btn_adicionar_pv.config(text="Atualizar Ponto")

        editando_ponto = True
        indice_ponto_editando = index
        

    def editar_pv_vetor():
        nonlocal editando_vetor, indice_vetor_editando
        selected_index = listbox_pv_vetores.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Selecione um vetor para editar.")
            return
        index = selected_index[0]

        vetor = vetores_pv[index]
        entry_input.insert(0, str(vetor.name + "=(") + str(vetor.ponto_b.x) + "," + str(vetor.ponto_b.y) + ")")
        
        btn_adicionar_pv.config(text="Atualizar Vetor")

        editando_vetor = True
        indice_vetor_editando = index
                
    def deletar_pv_ponto():
        nonlocal qtd_pontos
        selected_index = listbox_pv_pontos.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Selecione um ponto para deletar.")
            return
        index = selected_index[0]
        del pontos_pv[index]
        qtd_pontos -= 1

        for n in indices_pontos_canvas_pv:
            formatAndText = str.split(n, "-")
            canvas_pontos_pv.plano.delete(formatAndText[0])
            canvas_pontos_pv.plano.delete(formatAndText[1])
        
        indices_pontos_canvas_pv.clear()    
        
        for p in pontos_pv:
            indices_pontos_canvas_pv.append(desenhar_ponto_no_canvas(p, canvas_pontos_pv.plano))
                
        atualizar_lista_pv_pontos()

    def deletar_pv_vetor():
        nonlocal qtd_vetores
        selected_index = listbox_pv_vetores.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Selecione um vetor para deletar.")
            return
        index = selected_index[0]
        del vetores_pv[index]
        qtd_vetores -= 1
        
        for n in indices_vetores_canvas_pv:
            canvas_vetores_pv.plano.delete(n)
                    
        indices_vetores_canvas_pv.clear()    
                    
        for v in vetores_pv:
            indices_vetores_canvas_pv.append(desenhar_vetor_no_canvas(v, canvas_vetores_pv.plano))
            
        atualizar_lista_pv_vetores()

    def exibir_plano_pv():
        if qtd_pontos == 0 and qtd_vetores == 0:
            messagebox.showerror("Erro", "Adicione pelo menos um ponto ou vetor.")
            return
        desenhar_pontos_vetores(pontos_pv, vetores_pv)

    root.mainloop()

if __name__ == "__main__":
    main()
