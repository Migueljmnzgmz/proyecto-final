import pygame
import random
from collections import deque

WIDTH, HEIGHT = 800, 800 # hace el tamaño de la ventana
ROWS, COLS = 15, 15 # el tamaño del laberinto
CELL_SIZE = WIDTH // COLS #tamaño de la celda

WHITE = (255, 255, 255) #color del camino que el laberinto no ocupo
BLACK = (0, 0, 0) #color de las paredes
GREEN = (0, 255, 0) #color de la entrada
RED = (255, 0, 0) #color de la salida
BLUE = (0, 0, 255) #color del camino reuelto
PURPLE = (128, 0, 128) #al rededores de la pared

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #indica hacia donde se puede mover el resolvedor

def generate_maze(rows, cols):  #crea la matriz o tablero para la matriz
    maze = [[1 for _ in range(cols)] for _ in range(rows)] 

    def carve(x, y):         # el carve nos ayuda a que verifique si se puede mover en todas las direcciones y que se mueva en la correcta
        dirs = directions[:]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx * 2, y + dy * 2           
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                maze[x + dx][y + dy] = 0
                maze[nx][ny] = 0
                carve(nx, ny)

    maze[1][1] = 0
    carve(1, 1)
    maze[0][1] = 0  # Entrada
    maze[rows - 1][cols - 2] = 0  # Salida
    return maze

def draw_grid(screen): #dinuja los bordes entre las celdas
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, PURPLE, rect, 1)

def draw_maze(screen, maze, path=None):        #Dibuja el tablero y verifica que exista el camino solucion pintandolo de azul
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE if maze[i][j] == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if path:
        for x, y in path:
            pygame.draw.rect(screen, BLUE, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, GREEN, (1 * CELL_SIZE, 0 * CELL_SIZE, CELL_SIZE, CELL_SIZE)) #inicio del camino
    pygame.draw.rect(screen, RED, ((COLS - 2) * CELL_SIZE, (ROWS - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))#salida del camino

    draw_grid(screen)

def search_system(maze, start, goal):
    queue = deque([start])  #pone en espera las celdas que falta por verificar
    visited = set() #almacena las celdas ya visitadas para evitar repetir las mismas celdas
    parent = {} #almacenas las celdas buenas para reconstruir el camino cuando acabe la busqueda
    visited.add(start)  #agrega el inicio luego luego a los visitados

    while queue:  #ocupamos un while para recorrer las celdas
        current = queue.popleft()
        if current == goal:   #si el buscador llega al objetivo se acaba la busqueda
            break
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in visited:
                queue.append((nx, ny)) 
                visited.add((nx, ny))
                parent[(nx, ny)] = current  

    path = [] #todo esto para que el camino solucion se pinte de azul
    node = goal
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return []
    path.append(start)
    path.reverse()
    return path

def main():  #funcion principal , abre la ventana del juego
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Resoverdor de laberinto proyecto final por favor pongame 10")

    maze = generate_maze(ROWS, COLS)
    start = (0, 1)
    goal = (ROWS - 1, COLS - 2)
    path = search_system(maze, start, goal)

    running = True  #dibuja el juego mientras la ventana este abierta
    while running:
        screen.fill(PURPLE)
        draw_maze(screen, maze, path)
        pygame.display.flip()

        for event in pygame.event.get(): #si se cierra la ventana el juego acaba solito
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()


#Inspiraciones y ayudas de internet
#https://github.com/sahin88/Python_Pygame_Maze_Solver/blob/main/maze_solver.py
#https://www.youtube.com/watch?v=jZQ31-4_8KM
#https://www.thehexninja.com/2018/01/practical-exercise-image-carving-ii.html
#chatgpt