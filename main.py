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

# Função para desenhar a pista de corrida personalizada
def desenhar_pista(ax):
    # Coordenadas da pista
    pista_x = []
    pista_y = []

    # 1. Reta inicial a partir de (0,0) até (0,5)
    pista_x.extend([0, 0])
    pista_y.extend([0, 5])

    # 2.  Pequena reta de (0,5) até (10,10)
    pista_x.extend([0, 5])
    pista_y.extend([10, 10])

    # 3. Pequena reta de (10,10) até (10,-5)
    pista_x.extend([10, 10])
    pista_y.extend([10, -5])


    # 4. Curva final retornando ao ponto de largada (0,0)
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
    frame_pontos = tk.Frame(notebook)
    frame_vetores = tk.Frame(notebook)
    frame_pontos_vetores = tk.Frame(notebook)

    notebook.add(frame_pontos, text="Pontos")
    notebook.add(frame_vetores, text="Vetores")
    notebook.add(frame_pontos_vetores, text="Pontos e Vetores")

    # ------------------- Aba de Pontos ------------------- #
    # Frames para inputs e lista
    frame_pontos_main = tk.Frame(frame_pontos)
    frame_pontos_main.pack(expand=1, fill='both')

    frame_pontos_inputs = tk.Frame(frame_pontos_main)
    frame_pontos_inputs.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    frame_pontos_lista = tk.Frame(frame_pontos_main)
    frame_pontos_lista.pack(side='right', fill='both', expand=True, padx=10, pady=10)

    # Inputs para Pontos
    label_ponto = tk.Label(frame_pontos_inputs, text="Adicionar/Editar Ponto")
    label_ponto.pack()

    label_nome_ponto = tk.Label(frame_pontos_inputs, text="Nome do Ponto:")
    label_nome_ponto.pack()
    entry_nome_ponto = tk.Entry(frame_pontos_inputs)
    entry_nome_ponto.pack()

    label_x = tk.Label(frame_pontos_inputs, text="Coordenada x:")
    label_x.pack()
    entry_x = tk.Entry(frame_pontos_inputs)
    entry_x.pack()

    label_y = tk.Label(frame_pontos_inputs, text="Coordenada y:")
    label_y.pack()
    entry_y = tk.Entry(frame_pontos_inputs)
    entry_y.pack()

    btn_ponto = tk.Button(frame_pontos_inputs, text="Adicionar Ponto", command=lambda: adicionar_atualizar_ponto())
    btn_ponto.pack(pady=5)

    # Botão para exibir o plano de pontos
    btn_exibir_pontos = tk.Button(frame_pontos_inputs, text="Exibir Plano de Pontos", command=lambda: exibir_plano_pontos())
    btn_exibir_pontos.pack(pady=5)

    # Lista de Pontos
    label_lista_pontos = tk.Label(frame_pontos_lista, text="Lista de Pontos")
    label_lista_pontos.pack()

    listbox_pontos = tk.Listbox(frame_pontos_lista)
    listbox_pontos.pack(expand=1, fill='both')

    frame_ponto_botoes = tk.Frame(frame_pontos_lista)
    frame_ponto_botoes.pack(pady=5)

    btn_editar_ponto = tk.Button(frame_ponto_botoes, text="Editar Ponto", command=lambda: editar_ponto())
    btn_editar_ponto.grid(row=0, column=0, padx=5)

    btn_deletar_ponto = tk.Button(frame_ponto_botoes, text="Deletar Ponto", command=lambda: deletar_ponto())
    btn_deletar_ponto.grid(row=0, column=1, padx=5)

    # ------------------- Aba de Vetores ------------------- #
    # Frames para inputs e lista
    frame_vetores_main = tk.Frame(frame_vetores)
    frame_vetores_main.pack(expand=1, fill='both')

    frame_vetores_inputs = tk.Frame(frame_vetores_main)
    frame_vetores_inputs.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    frame_vetores_lista = tk.Frame(frame_vetores_main)
    frame_vetores_lista.pack(side='right', fill='both', expand=True, padx=10, pady=10)

    # Inputs para Vetores
    label_vetor = tk.Label(frame_vetores_inputs, text="Adicionar/Editar Vetor")
    label_vetor.pack()

    label_nome_vetor = tk.Label(frame_vetores_inputs, text="Nome do Vetor:")
    label_nome_vetor.pack()
    entry_nome_vetor = tk.Entry(frame_vetores_inputs)
    entry_nome_vetor.pack()

    label_xa = tk.Label(frame_vetores_inputs, text="x do ponto A:")
    label_xa.pack()
    entry_xa = tk.Entry(frame_vetores_inputs)
    entry_xa.pack()

    label_ya = tk.Label(frame_vetores_inputs, text="y do ponto A:")
    label_ya.pack()
    entry_ya = tk.Entry(frame_vetores_inputs)
    entry_ya.pack()

    label_xb = tk.Label(frame_vetores_inputs, text="x do ponto B:")
    label_xb.pack()
    entry_xb = tk.Entry(frame_vetores_inputs)
    entry_xb.pack()

    label_yb = tk.Label(frame_vetores_inputs, text="y do ponto B:")
    label_yb.pack()
    entry_yb = tk.Entry(frame_vetores_inputs)
    entry_yb.pack()

    btn_vetor = tk.Button(frame_vetores_inputs, text="Adicionar Vetor", command=lambda: adicionar_atualizar_vetor())
    btn_vetor.pack(pady=5)

    # Botão para exibir o plano de vetores
    btn_exibir_vetores = tk.Button(frame_vetores_inputs, text="Exibir Plano de Vetores", command=lambda: exibir_plano_vetores())
    btn_exibir_vetores.pack(pady=5)

    # Lista de Vetores
    label_lista_vetores = tk.Label(frame_vetores_lista, text="Lista de Vetores")
    label_lista_vetores.pack()

    listbox_vetores = tk.Listbox(frame_vetores_lista)
    listbox_vetores.pack(expand=1, fill='both')

    frame_vetor_botoes = tk.Frame(frame_vetores_lista)
    frame_vetor_botoes.pack(pady=5)

    btn_editar_vetor = tk.Button(frame_vetor_botoes, text="Editar Vetor", command=lambda: editar_vetor())
    btn_editar_vetor.grid(row=0, column=0, padx=5)

    btn_deletar_vetor = tk.Button(frame_vetor_botoes, text="Deletar Vetor", command=lambda: deletar_vetor())
    btn_deletar_vetor.grid(row=0, column=1, padx=5)

    # ------------------- Aba de Pontos e Vetores ------------------- #
    # Frames para inputs e listas
    frame_pv_main = tk.Frame(frame_pontos_vetores)
    frame_pv_main.pack(expand=1, fill='both')

    frame_pv_input = tk.Frame(frame_pv_main)
    frame_pv_input.pack(side='top', fill='x', padx=10, pady=10)

    frame_pv_lists = tk.Frame(frame_pv_main)
    frame_pv_lists.pack(side='top', fill='both', expand=True, padx=10, pady=10)

    # Input de texto
    label_input = tk.Label(frame_pv_input, text="Insira um Ponto ou Vetor (Ex: D(1,2) ou t=(3,4)):")
    label_input.pack()
    entry_input = tk.Entry(frame_pv_input)
    entry_input.pack(fill='x')

    btn_adicionar_pv = tk.Button(frame_pv_input, text="Adicionar", command=lambda: adicionar_pv())
    btn_adicionar_pv.pack(pady=5)

    # Frame para listas
    frame_pv_pontos = tk.Frame(frame_pv_lists)
    frame_pv_pontos.pack(side='left', fill='both', expand=True, padx=10)

    frame_pv_vetores = tk.Frame(frame_pv_lists)
    frame_pv_vetores.pack(side='right', fill='both', expand=True, padx=10)

    # Lista de Pontos
    label_lista_pv_pontos = tk.Label(frame_pv_pontos, text="Lista de Pontos")
    label_lista_pv_pontos.pack()

    listbox_pv_pontos = tk.Listbox(frame_pv_pontos)
    listbox_pv_pontos.pack(expand=1, fill='both')

    btn_deletar_pv_ponto = tk.Button(frame_pv_pontos, text="Deletar Ponto", command=lambda: deletar_pv_ponto())
    btn_deletar_pv_ponto.pack(pady=5)

    # Lista de Vetores
    label_lista_pv_vetores = tk.Label(frame_pv_vetores, text="Lista de Vetores")
    label_lista_pv_vetores.pack()

    listbox_pv_vetores = tk.Listbox(frame_pv_vetores)
    listbox_pv_vetores.pack(expand=1, fill='both')

    btn_deletar_pv_vetor = tk.Button(frame_pv_vetores, text="Deletar Vetor", command=lambda: deletar_pv_vetor())
    btn_deletar_pv_vetor.pack(pady=5)

    # Botão para exibir o plano
    btn_exibir_pv = tk.Button(frame_pv_main, text="Exibir Plano", command=lambda: exibir_plano_pv())
    btn_exibir_pv.pack(pady=5)

    # Listas para armazenar pontos e vetores desta aba
    pontos_pv = []
    vetores_pv = []

    # ------------------- Funções para Pontos ------------------- #
    def atualizar_lista_pontos():
        listbox_pontos.delete(0, tk.END)
        for i, ponto in enumerate(plan.points):
            nome = ponto.name if ponto.name else ''
            listbox_pontos.insert(tk.END, f"{i+1}: {nome}({ponto.x}, {ponto.y})")

    def adicionar_atualizar_ponto():
        nonlocal qtd_pontos, editando_ponto, indice_ponto_editando
        if not editando_ponto and qtd_pontos >= 5:
            messagebox.showerror("Erro", "Limite de 5 pontos atingido.")
            return

        try:
            nome = entry_nome_ponto.get().strip()
            x = float(entry_x.get())
            y = float(entry_y.get())
            ponto = Point(x, y, name=nome)

            if editando_ponto:
                plan.points[indice_ponto_editando] = ponto
                messagebox.showinfo("Sucesso", f"Ponto atualizado para {ponto.name}({ponto.x}, {ponto.y}).")
                btn_ponto.config(text="Adicionar Ponto")
                editando_ponto = False
                indice_ponto_editando = None
            else:
                plan.add_point(ponto)
                qtd_pontos += 1
                messagebox.showinfo("Sucesso", f"Ponto {ponto.name}({ponto.x}, {ponto.y}) adicionado.")

            atualizar_lista_pontos()
            entry_nome_ponto.delete(0, tk.END)
            entry_x.delete(0, tk.END)
            entry_y.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Insira valores numéricos válidos.")

    def editar_ponto():
        nonlocal editando_ponto, indice_ponto_editando
        selected_index = listbox_pontos.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Selecione um ponto para editar.")
            return
        index = selected_index[0]
        ponto = plan.points[index]
        entry_nome_ponto.delete(0, tk.END)
        entry_nome_ponto.insert(0, ponto.name)
        entry_x.delete(0, tk.END)
        entry_x.insert(0, str(ponto.x))
        entry_y.delete(0, tk.END)
        entry_y.insert(0, str(ponto.y))
        btn_ponto.config(text="Atualizar Ponto")
        editando_ponto = True
        indice_ponto_editando = index

    def deletar_ponto():
        nonlocal qtd_pontos
        selected_index = listbox_pontos.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Selecione um ponto para deletar.")
            return
        index = selected_index[0]
        del plan.points[index]
        qtd_pontos -= 1
        atualizar_lista_pontos()

    def exibir_plano_pontos():
        if qtd_pontos == 0:
            messagebox.showerror("Erro", "Adicione pelo menos um ponto.")
            return
        desenhar_pontos(plan.points)

    # ------------------- Funções para Vetores ------------------- #
    def atualizar_lista_vetores():
        listbox_vetores.delete(0, tk.END)
        for i, vetor in enumerate(plan.vectors):
            a = vetor.ponto_a
            b = vetor.ponto_b
            nome = vetor.name if vetor.name else ''
            listbox_vetores.insert(tk.END, f"{i+1}: {nome}: A({a.x}, {a.y}) -> B({b.x}, {b.y})")

    def adicionar_atualizar_vetor():
        nonlocal qtd_vetores, editando_vetor, indice_vetor_editando
        if not editando_vetor and qtd_vetores >= 4:
            messagebox.showerror("Erro", "Limite de 4 vetores atingido.")
            return

        try:
            nome = entry_nome_vetor.get().strip()
            x_a = float(entry_xa.get())
            y_a = float(entry_ya.get())
            x_b = float(entry_xb.get())
            y_b = float(entry_yb.get())

            ponto_a = Point(x_a, y_a)
            ponto_b = Point(x_b, y_b)
            vetor = Vector(ponto_a, ponto_b, name=nome)

            if editando_vetor:
                plan.vectors[indice_vetor_editando] = vetor
                messagebox.showinfo("Sucesso", "Vetor atualizado.")
                btn_vetor.config(text="Adicionar Vetor")
                editando_vetor = False
                indice_vetor_editando = None
            else:
                plan.add_vector(vetor)
                qtd_vetores += 1
                messagebox.showinfo("Sucesso", f"Vetor {nome} de ({x_a}, {y_a}) até ({x_b}, {y_b}) adicionado.")

            atualizar_lista_vetores()
            entry_nome_vetor.delete(0, tk.END)
            entry_xa.delete(0, tk.END)
            entry_ya.delete(0, tk.END)
            entry_xb.delete(0, tk.END)
            entry_yb.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Insira valores numéricos válidos.")

    def editar_vetor():
        nonlocal editando_vetor, indice_vetor_editando
        selected_index = listbox_vetores.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Selecione um vetor para editar.")
            return
        index = selected_index[0]
        vetor = plan.vectors[index]
        entry_nome_vetor.delete(0, tk.END)
        entry_nome_vetor.insert(0, vetor.name)
        entry_xa.delete(0, tk.END)
        entry_xa.insert(0, str(vetor.ponto_a.x))
        entry_ya.delete(0, tk.END)
        entry_ya.insert(0, str(vetor.ponto_a.y))
        entry_xb.delete(0, tk.END)
        entry_xb.insert(0, str(vetor.ponto_b.x))
        entry_yb.delete(0, tk.END)
        entry_yb.insert(0, str(vetor.ponto_b.y))
        btn_vetor.config(text="Atualizar Vetor")
        editando_vetor = True
        indice_vetor_editando = index

    def deletar_vetor():
        nonlocal qtd_vetores
        selected_index = listbox_vetores.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Selecione um vetor para deletar.")
            return
        index = selected_index[0]
        del plan.vectors[index]
        qtd_vetores -= 1
        atualizar_lista_vetores()

    def exibir_plano_vetores():
        if qtd_vetores == 0:
            messagebox.showerror("Erro", "Adicione pelo menos um vetor.")
            return
        desenhar_vetores(plan.vectors)

    # ------------------- Funções para Pontos e Vetores ------------------- #
    def adicionar_pv():
        nonlocal qtd_pontos, qtd_vetores
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
                if qtd_vetores >= 4:
                    messagebox.showerror("Erro", "Limite de 4 vetores atingido.")
                    return
                vetor = Vector(Point(0, 0), Point(x, y), name=nome)
                vetores_pv.append(vetor)
                qtd_vetores += 1
                atualizar_lista_pv_vetores()
                messagebox.showinfo("Sucesso", f"Vetor {nome}({x}, {y}) adicionado.")
            else:
                # Ponto no formato Nome(x,y)
                var_name, coords = input_text.split('(')
                nome = var_name.strip()
                coords = coords.strip().strip(')')
                x_str, y_str = coords.split(',')
                x = float(x_str)
                y = float(y_str)
                if qtd_pontos >= 5:
                    messagebox.showerror("Erro", "Limite de 5 pontos atingido.")
                    return
                ponto = Point(x, y, name=nome)
                pontos_pv.append(ponto)
                qtd_pontos += 1
                atualizar_lista_pv_pontos()
                messagebox.showinfo("Sucesso", f"Ponto {nome}({x}, {y}) adicionado.")
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

    def deletar_pv_ponto():
        nonlocal qtd_pontos
        selected_index = listbox_pv_pontos.curselection()
        if not selected_index:
            messagebox.showerror("Erro", "Selecione um ponto para deletar.")
            return
        index = selected_index[0]
        del pontos_pv[index]
        qtd_pontos -= 1
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
        atualizar_lista_pv_vetores()

    def exibir_plano_pv():
        if qtd_pontos == 0 and qtd_vetores == 0:
            messagebox.showerror("Erro", "Adicione pelo menos um ponto ou vetor.")
            return
        desenhar_pontos_vetores(pontos_pv, vetores_pv)

    root.mainloop()

if __name__ == "__main__":
    main()
