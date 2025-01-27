import tkinter as tk
import numpy as np
import random
import time

# Función que devuelve las bombas cercanas y realiza revelación recursiva
def distancia(matrix, user_pos, bomb_list, visited=None):
    if visited is None:
        visited = set()

    if user_pos in visited:
        return matrix

    visited.add(user_pos)
    der = (0, 1)
    izq = (0, -1)
    arr = (1, 0)
    abj = (-1, 0)
    diag_arr_der = (1, 1)
    diag_abj_der = (-1, 1)
    diag_arr_izq = (1, -1)
    diag_abj_izq = (-1, -1)
    movimientos = [der, izq, arr, abj, diag_arr_izq, diag_arr_der, diag_abj_der, diag_abj_izq]

    bomb_cerca = 0
    for mov in movimientos:
        new_pos = tuple(user_pos[i] + mov[i] for i in range(len(user_pos)))
        if 0 <= new_pos[0] < N and 0 <= new_pos[1] < N and new_pos in bomb_list:
            bomb_cerca += 1

    if bomb_cerca > 0:
        matrix[user_pos] = bomb_cerca
    else:
        matrix[user_pos] = " "
        for mov in movimientos:
            new_pos = tuple(user_pos[i] + mov[i] for i in range(len(user_pos)))
            if 0 <= new_pos[0] < N and 0 <= new_pos[1] < N and matrix[new_pos] == "❓":
                matrix = distancia(matrix, new_pos, bomb_list, visited)

    return matrix

# Tamaño de la matriz
N = 8

# Crear la matriz llena de "?" con numpy
matrix = np.full((N, N), '❓', dtype=object)

# Crear bombas aleatorias
bombas = 10
bomb_list = []
while len(bomb_list) < bombas:
    bomb_pos = (random.randint(0, N - 1), random.randint(0, N - 1))
    if bomb_pos not in bomb_list:
        bomb_list.append(bomb_pos)

# Inicializar variables globales
marcadas = []
game_status = True
banderas_usadas = 0
start_time = 0
temporizador_iniciado = False

# Configuración de la ventana de tkinter
root = tk.Tk()
root.title("Busca Bombas")

# Actualizar tiempo en el tablero
def actualizar_tiempo():
    if game_status and temporizador_iniciado:
        elapsed_time = int(time.time() - start_time)
        time_label.config(text=f"Tiempo: {elapsed_time} s")
        root.after(1000, actualizar_tiempo)

# Iniciar el temporizador
def iniciar_temporizador():
    global temporizador_iniciado, start_time
    if not temporizador_iniciado:  # Si aún no ha comenzado
        temporizador_iniciado = True
        start_time = time.time()
        actualizar_tiempo()

# Función para marcar una bomba
def marcar_bomba(i, j):
    global marcadas, banderas_usadas, matrix
    if game_status:
        iniciar_temporizador()  # Iniciar el temporizador al marcar
        user_pos = (i, j)
        if user_pos in marcadas:  # Desmarcar si ya está marcado
            marcadas.remove(user_pos)
            matrix[user_pos] = "❓"
            banderas_usadas -= 1
        else:  # Marcar como bandera
            if banderas_usadas < bombas:
                matrix[user_pos] = "🚩"
                marcadas.append(user_pos)
                banderas_usadas += 1
        actualizar_tablero()
        verificar_victoria()
        flag_label.config(text=f"Banderas: {banderas_usadas}/{bombas}")

# Función para revelar una celda
def revelar(i, j):
    global matrix, bomb_list, game_status
    if game_status:
        iniciar_temporizador()  # Iniciar el temporizador al revelar
        user_pos = (i, j)
        if user_pos in bomb_list:  # Si el usuario selecciona una bomba
            matrix[user_pos] = "💣💥"
            game_status = False
            print("¡Explosión 💣💥! Has perdido.")
            actualizar_tablero()
        elif matrix[user_pos] == "❓":
            matrix = distancia(matrix, user_pos, bomb_list)
            actualizar_tablero()
        if not game_status:
            detener_temporizador()

# Verificar si el jugador ha ganado
def verificar_victoria():
    global marcadas, bomb_list, game_status
    if len(marcadas) == bombas and all(pos in bomb_list for pos in marcadas):
        print("😄¡Enhorabuena, has ganado! 🎉")
        game_status = False
        detener_temporizador()
        for row in buttons:
            for button in row:
                button.config(state="disabled")

# Detener el temporizador
def detener_temporizador():
    global game_status
    if not game_status:
        elapsed_time = int(time.time() - start_time)
        time_label.config(text=f"Tiempo final: {elapsed_time} s")

# Actualizar el tablero gráfico
def actualizar_tablero():
    for i in range(N):
        for j in range(N):
            button = buttons[i][j]
            button.config(text=matrix[i, j])
            if matrix[i, j] == "🚩":
                button.config(bg="red")
            elif matrix[i, j] == "💣💥":
                button.config(bg="black", fg="white")

# Crear el tablero de botones
buttons = []
for i in range(N):
    row = []
    for j in range(N):
        button = tk.Button(root, text="❓", width=5, height=2, command=lambda i=i, j=j: revelar(i, j))
        button.grid(row=i + 2, column=j, padx=5, pady=5)

        # Asociar el clic derecho para marcar bomba
        button.bind("<Button-3>", lambda event, i=i, j=j: marcar_bomba(i, j))

        row.append(button)
    buttons.append(row)

# Crear etiquetas de información
time_label = tk.Label(root, text="Tiempo: 0 s", font=("Arial", 12))
time_label.grid(row=0, column=0, columnspan=N // 2, pady=5)

flag_label = tk.Label(root, text=f"Banderas: {banderas_usadas}/{bombas}", font=("Arial", 12))
flag_label.grid(row=0, column=N // 2, columnspan=N // 2, pady=5)

root.mainloop()
