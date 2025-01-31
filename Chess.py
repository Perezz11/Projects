# Juego del ajedrez en python
import copy

# Para que los print sean opcionales (Si no en la funcion es_jaque_mate saldrían muchos mensajes)
def log_debug(mensaje):
    if DEBUG:
        print(mensaje)
    

def hay_jaque(pos_rey_blanco, pos_rey_negro, turno, tablero):
    # Mirar si desde la posición del rey hay alguna pieza rival amenazando
    fila_rey, col_rey = pos_rey_blanco if turno == "blanco" else pos_rey_negro
    color_rey = "blanco" if turno == "blanco" else "negro"
    
    # Amenaza de caballo, mirar las Ls desde el rey
    vectores_movi_caballo = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1, -2), (1,-2), (2,-1)]
    for i, j in vectores_movi_caballo:
        if fila_rey + i >= len(tablero) or col_rey + j >= len(tablero) or fila_rey + i < 0 or col_rey + j < 0:
            continue
        if isinstance(tablero[fila_rey + i][col_rey + j], Caballo) and tablero[fila_rey + i][col_rey + j].color != color_rey:
            return True
    
    # Amenaza de torre/reina, mirar si desde la posicion del rey hacia arriba, hacia abajo o hacia los lados hay una torre rival
    # Si hay una pieza diferente a la torre/reina aunque sea enemiga. p.e un alfil bloqueando a la torre o una pieza del mismo color, no hay jaque
    vectores_movi_recto = [(1,0), (0,1), (-1,0), (0,-1)]
    
    for i, j in vectores_movi_recto:
        nueva_fila, nueva_col = fila_rey, col_rey
        while True:
            nueva_fila +=i
            nueva_col +=j
            # Si se sale del tablero, vamos con otra dirección
            if nueva_fila >= len(tablero) or nueva_col >= len(tablero) or nueva_fila < 0 or nueva_col < 0:
                break
            
            # Si no hay ninguna pieza, sigue avanzando
            if tablero[nueva_fila][nueva_col] == " ":
                continue
            
            # Hay alguna reina o torre?
            if (isinstance(tablero[nueva_fila][nueva_col], (Torre, Reina))) and tablero[nueva_fila][nueva_col].color != color_rey:
                return True
            
            # Si hay cualquier otra pieza, no hay jaque
            if tablero[nueva_fila][nueva_col] != " ":
                break
    
    # Amenaza de alfil/reina, mirar si desde la posicion del rey hacia arriba, hacia abajo o hacia los lados hay una torre rival
    # Si hay una pieza diferente a la alfil/reina aunque sea enemiga. p.e un alfil bloqueando a la torre o una pieza del mismo color, no hay jaque
    vectores_movi_diag = [(1,1), (-1,1), (-1,-1), (1,-1)]
    
    for i, j in vectores_movi_diag:
        nueva_fila, nueva_col = fila_rey, col_rey
        while True:
            nueva_fila +=i
            nueva_col +=j
            # Si se sale del tablero, vamos con otra dirección
            if nueva_fila >= len(tablero) or nueva_col >= len(tablero) or nueva_fila < 0 or nueva_col < 0:
                break
            
            # Si no hay ninguna pieza, sigue avanzando
            if tablero[nueva_fila][nueva_col] == " ":
                continue
            
            # Hay alguna reina o alfil?
            if (isinstance(tablero[nueva_fila][nueva_col], (Alfil, Reina))) and tablero[nueva_fila][nueva_col].color != color_rey:
                return True
            
            # Si hay cualquier otra pieza, no hay jaque
            if tablero[nueva_fila][nueva_col] != " ":
                break
    
    # El peon come a distancia 1 en diagonal hacia delante la reina y el alfil están cubiertos de esta situación
    # El blanco está arriba (menor fila), miramos si hay peon fila mayor izquierda y derecha 
    if color_rey == "blanco":
        diag_peon = [(1,1),(1,-1)]
        for i, j in diag_peon:
            # Dentro del tablero
            if fila_rey + i >= len(tablero) or col_rey + j >= len(tablero) or fila_rey + i < 0 or col_rey + j < 0:
                continue
            if isinstance(tablero[fila_rey + i][col_rey + j], Peon) and tablero[fila_rey + i][col_rey + j].color != "blanco":
                return True
    # El negro está abajo (mayor fila), miramos si hay peon fila menor izquierda y derecha
    elif color_rey == "negro":
        diag_peon = [(-1,-1),(-1,1)]
        for i, j in diag_peon:
            # Dentro del tablero
            if fila_rey + i >= len(tablero) or col_rey + j >= len(tablero) or fila_rey + i < 0 or col_rey + j < 0:
                continue
            if isinstance(tablero[fila_rey + i][col_rey + j], Peon) and tablero[fila_rey + i][col_rey + j].color != "negro":
                return True 
    # Si no se cumple ninguna condición --> No hay jaque
    return False


def es_jaque_mate(pos_rey_blanco, pos_rey_negro, turno, tablero):
    # Si juega el negro y hace jaque, tenemos que mirar las piezas blancas
    jaqueado = "blanco" if turno == "negro" else "negro"
    
    # Piezas del jugador jaqueado
    piezas_jugador = [
        (pieza, (x, y)) 
        for x, fila in enumerate(tablero) 
        for y, pieza in enumerate(fila) 
        if isinstance(pieza, Pieza) and pieza.color == jaqueado
        ]
    
    # Probamos los movimientos de todas las piezas para saber si se puede evitar el jaque
    for pieza, pos_inicial in piezas_jugador:
        for i in range(8):
            for j in range(8):
                pos_final = (i,j)
                if pieza.mov_valido(pos_inicial, pos_final, tablero) == True:
                    # Si la pieza movida es el rey, actualizar su posición en el tablero virtual
                    tablero_virtual = copy.deepcopy(tablero)
                    pieza.mover_pieza(pos_inicial, pos_final, tablero_virtual)
                    # Si se mueve el Rey, guardar esa nueva posicion para ver si hay jaque
                    if isinstance(pieza, Rey):
                        if jaqueado == "blanco":
                            pos_rey_blanco_virtual = pos_final
                            sigue_en_jaque = hay_jaque(pos_rey_blanco_virtual, pos_rey_negro, jaqueado, tablero_virtual)
                        else:
                            pos_rey_negro_virtual = pos_final
                            sigue_en_jaque = hay_jaque(pos_rey_blanco, pos_rey_negro_virtual, jaqueado, tablero_virtual)
                    else:
                        # Evaluar si el rey sigue en jaque después del movimiento
                        sigue_en_jaque = hay_jaque(pos_rey_blanco, pos_rey_negro, jaqueado, tablero_virtual)
                    
                    # Si algún movimiento evita el jaque, no hay jaque mate
                    if not sigue_en_jaque:
                        print(f"Movimiento que evita el jaque: {pos_inicial} -> {pos_final}")
                        return False
                    
    # Si ningún movimiento evita el jaque, es jaque mate
    print("No hay movimientos válidos. Es jaque mate.")
    return True


def tablas(tablero):
    # Piezas del jugador blanco
    piezas_jugador_blanco = [
    (pieza, (x, y)) 
    for x, fila in enumerate(tablero) 
    for y, pieza in enumerate(fila) 
    if isinstance(pieza, Pieza) and pieza.color == "blanco"
    ]
    
    # Piezas del jugador negro
    piezas_jugador_negro = [
    (pieza, (x, y)) 
    for x, fila in enumerate(tablero) 
    for y, pieza in enumerate(fila) 
    if isinstance(pieza, Pieza) and pieza.color == "negro"
    ]
    
    lista_piezas_blancas = [type(pieza[0]).__name__ for pieza in piezas_jugador_blanco ]
    lista_piezas_negras = [type(pieza[0]).__name__ for pieza in piezas_jugador_negro]
    
        # Solo reyes
    if len(lista_piezas_blancas) == 1 and len(lista_piezas_negras) == 1:
        return True
    
    # Rey y caballo vs rey son tablas
    # Rey y alfil vs rey no son realmente tablas, pero muy mal tienes que jugar para perder
    if ((set(lista_piezas_blancas) <= {"Rey", "Caballo"} or set(lista_piezas_blancas) <= {"Rey", "Alfil"}) and set(lista_piezas_negras) <= {"Rey"}) or \
        (set(lista_piezas_blancas) <= {"Rey"} and (set(lista_piezas_negras) <= {"Rey", "Caballo"} or set(lista_piezas_negras) <= {"Rey", "Alfil"})):
        return True


class Pieza:
    def __init__(self, color):
        self.color = color
    
    def mov_valido(self, pos_inicial, pos_final, tablero):
        fila_ini, col_ini = pos_inicial
        fila_fin, col_fin = pos_final
        
        if fila_fin >= len(tablero) or col_fin >= len(tablero) or fila_fin < 0 or col_fin < 0:
            log_debug(f"Movimiento NO válido: Fuera de los límites del tablero")
            return False
        elif pos_inicial == pos_final:
            log_debug("MISMA posición inicial y final")
            return False
        # Si hay una pieza del mismo color en donde va, no vale
        if tablero[fila_fin][col_fin] != " " and tablero[fila_fin][col_fin].color == self.color:
            log_debug("Movimiento NO válido: Hay una pieza del mismo color")
            return False
        return True
    
    # Todas heredan esta funcion que es común, no implementar en las demas piezas
    def mover_pieza(self, pos_inicial, pos_final, tablero):
        if self.mov_valido(pos_inicial, pos_final, tablero) == True:
            fila_ini, col_ini = pos_inicial
            fila_fin, col_fin = pos_final
            if tablero[fila_fin][col_fin] != " ":
                pieza_capturada = tablero[fila_fin][col_fin]
                log_debug(f"Has capturado la pieza {type(pieza_capturada).__name__}")
            
            tablero[fila_ini][col_ini] = " "
            tablero[fila_fin][col_fin] = self
            
            # Promoción de los peones
            if isinstance(self, Peon):
                if (self.color == "blanco" and fila_fin == 7) or (self.color == "negro" and fila_fin == 0):
                    self.promocion(pos_final, tablero)
            
            return True
        return False

class Peon(Pieza):
    def __init__(self, color):
        super().__init__(color)
    
    def __str__(self):
        return "P" if self.color == "blanco" else "p"
    
    def mov_valido(self, pos_inicial, pos_final, tablero):
        fila_ini, col_ini = pos_inicial
        fila_fin, col_fin = pos_final
        
        if super().mov_valido(pos_inicial, pos_final, tablero) == False:
            return False
        
        # Si hay una pieza del mismo color en donde va, no vale
        if tablero[fila_fin][col_fin] != " " and tablero[fila_fin][col_fin].color == self.color:
            log_debug("Movimiento NO válido: Hay una pieza del mismo color")
            return False
        
        # Se mueve una hacia delante en la misma columna, positivo para el negro
        if self.color == "negro" and col_ini == col_fin and fila_ini - fila_fin == +1 and tablero[fila_fin][col_fin] == " ":
            return True
        # Negativo para el blanco
        if self.color == "blanco" and col_ini == col_fin and fila_ini - fila_fin == -1 and tablero[fila_fin][col_fin] == " ":
            return True
        
        # Posibilidad de mover 2 al principio. Cuidado con los rangos
        if self.color == "blanco" and fila_ini == 1:
            if col_fin == col_ini and fila_fin == 3 and tablero[fila_fin][col_fin] == " ":
                return True
        
        if self.color == "negro" and fila_ini == 6:
            if col_fin == col_ini and fila_fin == 4 and tablero[fila_fin][col_fin] == " ":
                return True
        
        # El peón come en diaognal
        if abs(col_ini - col_fin) == 1 and abs(fila_ini - fila_fin) == 1 and tablero[fila_fin][col_fin] != " ":
            return True
        
        log_debug("Movimiento NO válido: Así no se mueve el Peon")
        return False
    
    def promocion(self, pos_final, tablero):
        fila_fin, col_fin = pos_final
        new_pieza = input("A que pieza quieres promocionar?(D, T, A, C): ")
        if new_pieza == "D":
            tablero[fila_fin][col_fin] = Reina(self.color)
        elif new_pieza == "T":
            tablero[fila_fin][col_fin] = Torre(self.color)
        elif new_pieza == "A":
            tablero[fila_fin][col_fin] = Alfil(self.color)
        elif new_pieza == "C":
            tablero[fila_fin][col_fin] = Caballo(self.color)
        else:
            log_debug("Entrada no válida. Se promocionará automáticamente a una Reina.")
            tablero[fila_fin][col_fin] = Reina(self.color)



class Torre(Pieza):
    def __init__(self, color):
        super().__init__(color)
    
    def __str__(self):
            # Devuelve "T" para torres blancas y "t" para torres negras
            return "T" if self.color == "blanco" else "t"
    
    def mov_valido(self, pos_inicial, pos_final, tablero):
        fila_ini, col_ini = pos_inicial
        fila_fin, col_fin = pos_final
        
        # Primero verifica si el movimiento está dentro de los límites del tablero
        if super().mov_valido(pos_inicial, pos_final, tablero) == False:
            return False
        
        # Si no es vertical ni horizontal
        if fila_fin != fila_ini and col_fin != col_ini:
            log_debug("Movimiento NO válido: Así no se mueve la Torre")
            return False
        
        # Hay alguna pieza entre medias?
        if fila_ini == fila_fin: # Horizontal
            for i in range(min(col_ini, col_fin) + 1, max(col_ini, col_fin)):
                if tablero[fila_ini][i] != " ":
                    log_debug("Movimiento NO válido: Pieza entre medias")
                    return False
        
        if col_ini == col_fin: # Vertical
            for i in range(min(fila_ini, fila_fin) + 1, max(fila_ini, fila_fin)):
                if tablero[i][col_ini] != " ":
                    log_debug("Movimiento NO válido: Pieza entre medias")
                    return False
        
        # Si hay una pieza del mismo color
        if tablero[fila_fin][col_fin] != " " and tablero[fila_fin][col_fin].color == self.color:
            log_debug("Movimiento NO válido: Hay una pieza del mismo color")
            return False
        
        return True
    



class Caballo(Pieza):
    def __init__(self, color):
        super().__init__(color)
    
    def __str__(self):
        return "C" if self.color == "blanco" else "c"
    
    def mov_valido(self, pos_inicial, pos_final, tablero):
        # Primero verifica si el movimiento está dentro de los límites del tablero
        if super().mov_valido(pos_inicial, pos_final, tablero) == False:
            return False
        
        fila_ini, col_ini = pos_inicial
        fila_fin, col_fin = pos_final
        # Verificar movimiento del caballo
        if not ((abs(col_ini - col_fin) == 2 and abs(fila_ini - fila_fin) == 1) or 
                (abs(col_ini - col_fin) == 1 and abs(fila_ini - fila_fin) == 2)):
            log_debug("Movimiento NO válido: Así no se mueve el Caballo")
            return False
        
        # El caballo salta las piezas, por lo que no hay probema de encontrarse piezas en el camino
        
        # Si hay una pieza del mismo color
        if tablero[fila_fin][col_fin] != " " and tablero[fila_fin][col_fin].color == self.color:
            log_debug("Movimiento NO válido: Hay una pieza del mismo color")
            return False
        
        return True
    


class Alfil(Pieza):
    
    def __init__(self, color):
        super().__init__(color)
    
    def __str__(self):
        return "A" if self.color == "blanco" else "a"
    
    def mov_valido(self, pos_inicial, pos_final, tablero):
        # Primero verifica si el movimiento está dentro de los límites del tablero
        if super().mov_valido(pos_inicial, pos_final, tablero) == False:
            return False
        
        fila_ini, col_ini = pos_inicial
        fila_fin, col_fin = pos_final
        # Verificar movimiento del alfil
        if not abs(fila_fin - fila_ini) == abs(col_fin - col_ini):
            log_debug("Movimiento NO válido: Así no se mueve el Alfil")
            return False
        
        # Verificar que no haya piezas entre medias
        diferencia_filas = 1 if fila_fin > fila_ini else -1
        diferencia_cols = 1 if col_fin > col_ini else -1
        
        for i in range(1, abs(fila_fin - fila_ini)):
            if tablero[fila_ini + i*diferencia_filas][col_ini + i*diferencia_cols] != " ":
                log_debug("Movimiento NO válido: Pieza entre medias")
                return False
        
        # Si hay una pieza del mismo color
        if tablero[fila_fin][col_fin] != " " and tablero[fila_fin][col_fin].color == self.color:
            log_debug("Movimiento NO válido: Hay una pieza del mismo color")
            return False
        
        return True
    


class Reina(Pieza):
    def __init__(self, color):
        super().__init__(color)
    
    def __str__(self):
        return "D" if self.color == "blanco" else "d"
    
    def mov_valido(self, pos_inicial, pos_final, tablero):
        # Primero verifica si el movimiento está dentro de los límites del tablero
        if super().mov_valido(pos_inicial, pos_final, tablero) == False:
            return False
        
        fila_ini, col_ini = pos_inicial
        fila_fin, col_fin = pos_final
        
        # Se mueve como la torre o como el alfil? Si no como Torre y no como Alfil --> False
        if (fila_fin != fila_ini and col_fin != col_ini) and (abs(fila_fin - fila_ini) != abs(col_fin - col_ini)):
            log_debug("Movimiento NO válido: Así no se mueve la Reina")
            return False
        
        # Como la Torre
        if (fila_fin == fila_ini and col_fin != col_ini) or (fila_fin != fila_ini and col_fin == col_ini):
            # Hay alguna pieza entre medias?
            if fila_ini == fila_fin: # Horizontal
                for i in range(min(col_ini, col_fin) + 1, max(col_ini, col_fin)):
                    if tablero[fila_ini][i] != " ":
                        log_debug("Movimiento NO válido: Pieza entre medias")
                        return False
            
            if col_ini == col_fin: # Vertical
                for i in range(min(fila_ini, fila_fin) + 1, max(fila_ini, fila_fin)):
                    if tablero[i][col_ini] != " ":
                        log_debug("Movimiento NO válido: Pieza entre medias")
                        return False
        
        # Como el Alfil
        if abs(fila_fin - fila_ini) == abs(col_fin - col_ini):
            # Verificar que no haya piezas entre medias
            diferencia_filas = 1 if fila_fin > fila_ini else -1
            diferencia_cols = 1 if col_fin > col_ini else -1
            
            for i in range(1, abs(fila_fin - fila_ini)):
                if tablero[fila_ini + i*diferencia_filas][col_ini + i*diferencia_cols] != " ":
                    return False
        
        # Si hay una pieza del mismo color
        if tablero[fila_fin][col_fin] != " " and tablero[fila_fin][col_fin].color == self.color:
            log_debug("Movimiento NO válido: Hay una pieza del mismo color")
            return False
        
        return True
    


class Rey(Pieza):
    def __init__(self, color):
        super().__init__(color)
    
    def __str__(self):
        return "R" if self.color == "blanco" else "r"
    
    def mov_valido(self, pos_inicial, pos_final, tablero):
        # Primero verifica si el movimiento está dentro de los límites del tablero o en la misma posición inicial
        if super().mov_valido(pos_inicial, pos_final, tablero) == False:
            return False
        
        fila_ini, col_ini = pos_inicial
        fila_fin, col_fin = pos_final
        
        # Si hay una pieza del mismo color
        if tablero[fila_fin][col_fin] != " " and tablero[fila_fin][col_fin].color == self.color:
            log_debug("Movimiento NO válido: Hay una pieza del mismo color")
            return False

        # ENROQUE
        fila = 0 if turno == "blanco" else 7
        
        if pos_inicial == (fila,4) and pos_final == (fila,2) and (isinstance(tablero[fila][0], Torre) and tablero[fila][0].color == turno):
            if all(not hay_jaque((fila,col), pos_rey_negro, turno, tablero) for col in [2, 3, 4]):
                tablero[fila][0] = " "
                tablero[fila][3] = Torre(turno)
                print("Enrque Largo")
                return True
            
        # Enroque corto
        if pos_inicial == (fila,4) and pos_final == (fila,6) and (isinstance(tablero[fila][7], Torre) and tablero[fila][7].color == turno):
            if all(not hay_jaque((fila,col), pos_rey_negro, turno, tablero) for col in [4, 5, 6]):
                tablero[fila][7] = " "
                tablero[fila][5] = Torre(turno)
                print("Enroque Corto")
                return True
        
        # Movimiento normal del rey
        if not (abs(fila_fin - fila_ini) <= 1 and abs(col_fin - col_ini) <= 1):
            log_debug("Movimiento NO válido: Así no se mueve el Rey")
            return False        
        
        return True
    


def crear_tablero():
    tablero = [[" " for _ in range(8)] for _ in range(8)]
    
    # Piezas blancas
    tablero[0][0] = Torre("blanco")
    tablero[0][1] = Caballo("blanco")
    tablero[0][2] = Alfil("blanco")
    tablero[0][3] = Reina("blanco")
    tablero[0][4] = Rey("blanco")
    tablero[0][5] = Alfil("blanco")
    tablero[0][6] = Caballo("blanco")
    tablero[0][7] = Torre("blanco")
    tablero[1] = [Peon("blanco") for _ in range(8)]
    
    # Piezas negras
    tablero[7][0] = Torre("negro")
    tablero[7][1] = Caballo("negro")
    tablero[7][2] = Alfil("negro")
    tablero[7][3] = Reina("negro")
    tablero[7][4] = Rey("negro")
    tablero[7][5] = Alfil("negro")
    tablero[7][6] = Caballo("negro")
    tablero[7][7] = Torre("negro")
    tablero[6] = [Peon("negro") for _ in range(8)]
    
    return tablero

from prettytable import PrettyTable

def imprimir_tablero(tablero):
    # Crear un objeto PrettyTable
    x = PrettyTable()
    x.header = False  # Ocultar el encabezado superior

    # Añadir las filas del tablero, comenzando desde la última para que las filas numéricas sean visibles de abajo hacia arriba
    for i, fila in enumerate(reversed(tablero)):
        fila_imprimible = [str(8 - i)]  # Las filas numéricas en orden inverso
        for pieza in fila:
            if isinstance(pieza, Pieza):  # Mostrar la pieza si existe
                fila_imprimible.append(str(pieza))
            else:
                fila_imprimible.append(" ")  # Casillas vacías
        x.add_row(fila_imprimible)
    
    separador = [" "] + ["-" * 1] * 8
    x.add_row(separador)
    # Añadir una fila inferior con etiquetas de las columnas
    footer_row = [" "] + list("ABCDEFGH")  # Letras de columnas
    x.add_row(footer_row)
    
    # Imprimir el tablero en formato cuadrado
    print(x)

# Testing del tablero
'''tablero = crear_tablero()

imprimir_tablero(tablero) 

pieza = tablero[0][1]

pos_inicial = (0,1)
pos_final = (2,0)

pieza.mover_pieza(pos_inicial, pos_final, tablero)

log_debug(pieza.color)
imprimir_tablero(tablero)'''


def posicion_correcta(mensaje):
    while True:
        posicion = input(mensaje)
        
        if len(posicion) == 2 and posicion[0].lower() in "abcdefgh" and posicion[1] in "12345678":
            return posicion
        else:
            log_debug("Posición no válida, usa nomenclatura de ajedrez p.e: e4")


# Empieza el juego como sistema de turnos
DEBUG = True
# Empiezan las blancas
turno = "blanco"
game_status = True
# Creamos el tablero
tablero = crear_tablero()
imprimir_tablero(tablero)
while game_status == True:
    DEBUG = True
    log_debug("NOTA: El programa está pensado para usar nomenclatura de ajedrez p.e: e2")
    log_debug(f"Es turno del {turno}")
    pos_inicial = posicion_correcta("Introduce la posicion de la pieza a mover: ")
    pos_final = posicion_correcta("Introduce la posicion a donde muevas la pieza: ")
    
    # Convertimos a una lista para separar e4 a ["e", "4"]
    pos_inicial = list(pos_inicial)
    pos_final = list(pos_final)
    
    # Convertimos las letras a la posicion
    letras_a_numeros = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8}
    # Columna inicial y final
    col_ini = letras_a_numeros.get(pos_inicial[0], "Columna no encontrada")
    col_fin = letras_a_numeros.get(pos_final[0], "Columna no encontrada")
    if col_ini == "Columna no encontrada" or col_fin == "Columna no encontrada":
        log_debug("Columna no encontrada")
        continue
    
    # Le restamos 1 a las posiciones para estar de acuerdo a python (empieza en 0)
    try:
        fila_ini = int(pos_inicial[1]) - 1
        fila_fin = int(pos_final[1]) - 1
    except ValueError or fila_ini >= 8 or fila_fin >= 8: # Por si meten otra cosa que no sea un numero
        log_debug("La fila ingresada no es válida. Debe ser un número entre 1 y 8.")
        continue
    
    # Le restamos uno a las columnas también
    col_ini = col_ini - 1
    col_fin = col_fin - 1
    
    # Seleccionar la pieza del tablero excepto si no es ninguna pieza
    pieza = tablero[fila_ini][col_ini]
    if pieza == " ":
        log_debug("No has seleccionado ninguna pieza")
        continue
    
    # Chequear que la pieza sea del mismo color que del turno
    if pieza.color != turno:
        log_debug("¡¡¡Esa pieza no es tuya!!!")
        continue
    
    # Finalmente lo pasamos a lista, que es como lo entiende el programa de movimiento
    pos_inicial = (fila_ini, col_ini)
    pos_final = (fila_fin, col_fin)
    
    for i in range(8):
        for j in range(8):
            if isinstance(tablero[i][j], Rey) and tablero[i][j].color == "blanco":
                pos_rey_blanco = [i,j]
            
            elif isinstance(tablero[i][j], Rey) and tablero[i][j].color == "negro":
                pos_rey_negro = [i,j]
    
    # Crear una copia del tablero para simular el movimiento
    tablero_virtual = copy.deepcopy(tablero)
    
    # Realizar el movimiento en el tablero virtual
    if pieza.mover_pieza(pos_inicial, pos_final, tablero_virtual):
        # Verificar si el rey está en jaque después del movimiento
        if turno == "blanco":
            if hay_jaque(pos_rey_blanco, pos_rey_negro, turno, tablero_virtual):
                log_debug("Movimiento no permitido: Dejaría al rey blanco en jaque.")
                continue
        else:
            if hay_jaque(pos_rey_blanco, pos_rey_negro, turno, tablero_virtual):
                log_debug("Movimiento no permitido: Dejaría al rey negro en jaque.")
                continue
        
        # Si no hay jaque, aplicar el movimiento al tablero real
        pieza.mover_pieza(pos_inicial, pos_final, tablero)
        
        if turno == "blanco":
            if hay_jaque(pos_rey_blanco, pos_rey_negro, "negro", tablero):
                log_debug("Jaque al negro")
                if es_jaque_mate(pos_rey_blanco, pos_rey_negro, turno, tablero) == True:
                    print(f"ENHORABUENA 🥳 Jugador {turno}, has gando por jaque mate 🎉")
                    game_status = False
            
        else:
            if hay_jaque(pos_rey_blanco, pos_rey_negro, "blanco", tablero):
                log_debug("Jaque al blanco")
                DEBUG = False
                if es_jaque_mate(pos_rey_blanco, pos_rey_negro, turno, tablero) == True:
                    DEBUG = True
                    print(f"ENHORABUENA 🥳 Jugador {turno}, has gando por jaque mate 🎉")
                    game_status = False
            
        
        imprimir_tablero(tablero)
        
        # Cambiar el turno
        turno = "negro" if turno == "blanco" else "blanco"
    else:
        continue
    

# Cambiar el turno para saber el ganador
turno = "negro" if turno == "blanco" else "blanco"

