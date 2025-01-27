import numpy as np 
import random

def imprimir_matriz(matrix, top_coord, left_coord):
    # Definir el ancho fijo de cada celda
    ancho_celda = 3  # Ajusta según lo que necesites, 3 es suficiente para "🚩" y números pequeños

    # Crear las filas superiores (coordenadas horizontales)
    header = "  " + " ".join(f"{num:>{ancho_celda}}" for num in top_coord)
    print(header)

    # Crear las filas de la matriz con coordenadas laterales
    for i, row in enumerate(matrix):
        fila = f"{left_coord[i]:<2}" + " ".join(f"{str(cell):>{ancho_celda}}" for cell in row)
        print(fila)

# Funcion que devuelva las bombas cercanas
def distancia(matrix, user_pos, bomb_list):
    der = (0,1)
    izq = (0,-1)
    arr = (1,0)
    abj = (-1,0)
    diag_arr_der = (1,1)
    diag_arr_izq = (1,-1)
    diag_abj_der = (-1,1)
    diag_abj_izq = (-1,-1)
    movimientos = [der, izq, arr, abj, diag_arr_izq, diag_arr_der, diag_abj_der, diag_abj_izq]
    # Todos los movimientos
    for mov in movimientos:
        j = 1
        next_move = True
        while next_move == True:
            bomb_cerca = 0
            for bomb in bomb_list:
                if abs(user_pos[0] - bomb[0]) <= 1 and abs(user_pos[1] - bomb[1]) <= 1:
                    bomb_cerca +=1
                    next_move = False
            
            matrix[user_pos] = bomb_cerca
            if matrix[user_pos] != 0:
                break
            
            new_mov = tuple(mov[i]*j  for i in range(len(mov)))
            new_pos = tuple(user_pos[i] + new_mov[i] for i in range(len(user_pos)))
            
            if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= N or new_pos[1] >= N:
                break
            
            if new_pos in bomb_list:
                break
            
            for bomb in bomb_list:
                if abs(new_pos[0] - bomb[0]) <= 1 and abs(new_pos[1] - bomb[1]) <= 1:
                    bomb_cerca +=1
                    
            matrix[new_pos] = bomb_cerca
            if matrix[new_pos] != 0:
                next_move = False
            
            j+=1
            
    return matrix


# Tamaño de la matriz
N = 8

# Crear la matriz llena de "?" con numpy
matrix = np.full((N, N), '?', dtype=object)

# Crear coordenadas
top_coord = np.arange(1, N+1)  # Coordenadas superiores (1 a N)
top_coord = ["" + str(num) if num > 1 else str(num) for num in top_coord]
left_coord = np.arange(1, N+1) # Coordenadas laterales (1 a N)

# Crear la matriz con coordenadas
# Añadir la fila superior (coordenadas horizontales)
final_matrix = np.vstack([
    [" "] + list(top_coord),      # Primera fila (espacio vacío + top_coord)
    np.column_stack([left_coord, matrix])  # Insertar left_coord como primera columna
])

# Imprimir matriz con coordenadas
for row in final_matrix:
    print(" ".join(map(str, row)))

bombas = 10
bomb_list = []
puestas = 0

while puestas < bombas:
    bomb_pos = (random.randint(0,N-1), random.randint(0,N-1))
    if bomb_pos not in bomb_list:
        bomb_list.append(bomb_pos)
        puestas +=1

marcadas = []
game_status = True
while game_status == True:
    accion = input("Quieres poner 'posición' o 'marcar' bomba:").strip().lower()
    user_input = input("Introduce la fila y columna separados por un espacio: ").strip().lower()
    num1, num2 = map(int, user_input.split())
    num1 = num1 -1
    num2 = num2 -1
    user_pos = (num1, num2)
    
    if accion == "marcar":
        if user_pos in marcadas:  # Evitar marcar la misma posición más de una vez
            print("Ya has marcado esta posición.")
            quitar = input("Quieres quitar esa marca?(Y/n)")
            continue
        if len(marcadas) >= bombas:
            print(f"No puedes poner mas banderas")
            continue
            
        matrix[user_pos] = "🚩"
        marcadas.append(user_pos)
        
        final_matrix = np.vstack([
        ["  "] + list(top_coord),      # Primera fila (espacio vacío + top_coord)
        np.column_stack([left_coord, matrix])  # Insertar left_coord como primera columna
                        ])
        imprimir_matriz(matrix, top_coord, left_coord)
        if len(marcadas) == bombas and all(pos in bomb_list for pos in marcadas):
            print("😄¡Enhorabuena, has ganado! 🎉")
            game_status = False
    else:
        if user_pos in bomb_list:
            print("Explosión 💣💥")
            for bomb in bomb_list:
                matrix[bomb] = "💣"
            matrix[user_pos] = "💣💥"
            print(matrix)
            break
        else:
            matrix = (distancia(matrix, user_pos, bomb_list))
            imprimir_matriz(matrix, top_coord, left_coord)



