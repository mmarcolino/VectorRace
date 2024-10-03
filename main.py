import tkinter as tk
from tkinter import messagebox
from point import Point
from vector import Vector
from plan import Plan  # Importando a classe que você já tem

# Função para criar a interface gráfica no main
def main():
    plan = Plan()  # Inicializando o plano
    
    root = tk.Tk()
    root.title("Inserção de Pontos e Vetores")

    # Contadores para limitar pontos e vetores
    qtd_pontos = 0
    qtd_vetores = 0

    # Função para adicionar ponto
    def adicionar_ponto():
        nonlocal qtd_pontos
        if qtd_pontos >= 5:
            messagebox.showerror("Erro", "Limite de 5 pontos atingido.")
            return
        
        try:
            x = float(entry_x.get())
            y = float(entry_y.get())
            ponto = Point(x, y)
            plan.add_point(ponto)
            qtd_pontos += 1
            messagebox.showinfo("Sucesso", f"Ponto {ponto.x}, {ponto.y} adicionado.")
        except ValueError:
            messagebox.showerror("Erro", "Insira valores numéricos válidos.")

    # Função para adicionar vetor
    def adicionar_vetor():
        nonlocal qtd_vetores
        if qtd_vetores >= 4:
            messagebox.showerror("Erro", "Limite de 4 vetores atingido.")
            return
        
        try:
            x_a = float(entry_xa.get())
            y_a = float(entry_ya.get())
            x_b = float(entry_xb.get())
            y_b = float(entry_yb.get())

            ponto_a = Point(x_a, y_a)
            ponto_b = Point(x_b, y_b)
            vetor = Vector(ponto_a, ponto_b)
            plan.add_vector(vetor)
            qtd_vetores += 1
            messagebox.showinfo("Sucesso", f"Vetor de ({x_a}, {y_a}) até ({x_b}, {y_b}) adicionado.")
        except ValueError:
            messagebox.showerror("Erro", "Insira valores numéricos válidos.")

    # Função para finalizar e exibir o plano
    def exibir_plano():
        if qtd_pontos == 0 and qtd_vetores == 0:
            messagebox.showerror("Erro", "Adicione pelo menos um ponto ou vetor.")
            return
        # Aqui chamamos a função de exibição gráfica (exemplo com matplotlib)
        desenhar_plano(plan.points, plan.vectors)

    # Layout da interface gráfica
    label_x = tk.Label(root, text="Coordenada x:")
    label_x.pack()
    entry_x = tk.Entry(root)
    entry_x.pack()

    label_y = tk.Label(root, text="Coordenada y:")
    label_y.pack()
    entry_y = tk.Entry(root)
    entry_y.pack()

    # Para vetores, precisamos de 4 entradas (dois pontos)
    label_xa = tk.Label(root, text="Coordenada x do ponto A (vetor):")
    label_xa.pack()
    entry_xa = tk.Entry(root)
    entry_xa.pack()

    label_ya = tk.Label(root, text="Coordenada y do ponto A (vetor):")
    label_ya.pack()
    entry_ya = tk.Entry(root)
    entry_ya.pack()

    label_xb = tk.Label(root, text="Coordenada x do ponto B (vetor):")
    label_xb.pack()
    entry_xb = tk.Entry(root)
    entry_xb.pack()

    label_yb = tk.Label(root, text="Coordenada y do ponto B (vetor):")
    label_yb.pack()
    entry_yb = tk.Entry(root)
    entry_yb.pack()

    # Botões de ação
    btn_ponto = tk.Button(root, text="Adicionar Ponto", command=adicionar_ponto)
    btn_ponto.pack()

    btn_vetor = tk.Button(root, text="Adicionar Vetor", command=adicionar_vetor)
    btn_vetor.pack()

    btn_finalizar = tk.Button(root, text="Finalizar e Exibir Plano", command=exibir_plano)
    btn_finalizar.pack()

    root.mainloop()

# Função para desenhar o plano (exemplo com matplotlib)
import matplotlib.pyplot as plt

def desenhar_plano(pontos, vetores):
    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.axhline(0, color='black')
    ax.axvline(0, color='black')

    # Plotar pontos
    for ponto in pontos:
        ax.plot(ponto.x, ponto.y, 'bo')  # pontos azuis
        ax.text(ponto.x, ponto.y, f'A({ponto.x}, {ponto.y})')

    # Plotar vetores
    for vetor in vetores:
        ax.quiver(vetor.ponto_a.x, vetor.ponto_a.y, 
                  vetor.ponto_b.x - vetor.ponto_a.x, 
                  vetor.ponto_b.y - vetor.ponto_a.y, 
                  angles='xy', scale_units='xy', scale=1, color='r')

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
