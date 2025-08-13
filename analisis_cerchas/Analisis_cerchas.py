import matplotlib.pyplot as plt
import numpy as np

def calcular_factor_escala(MC):
    x_coords = [linea[i] for linea in MC for i in [0, 2]]
    y_coords = [linea[i] for linea in MC for i in [1, 3]]
    max_coord = max(max(x_coords) - min(x_coords), max(y_coords) - min(y_coords))
    factor_escala = max_coord / 10  # Escala las flechas para que sean una décima del tamaño máximo
    return factor_escala

def graficar(MC, MGL):
    fig, ax = plt.subplots(figsize=(15, 8))

    # Calcula el factor de escala
    factor_escala = calcular_factor_escala(MC)

    # Dibujar cada elemento de la cercha
    for i, linea in enumerate(MC):
        ax.plot([linea[0], linea[2]], [linea[1], linea[3]], 'k-', linewidth=2)
        ax.text((linea[0] + linea[2]) / 2, (linea[1] + linea[3]) / 2, str(i), color='red', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.2'))

    plt.axis('equal')
    plt.grid(True)

    arrow_length = factor_escala * 0.5 
    arrow_width = factor_escala * 0.03
    arrow_head_width = factor_escala * 0.2
    arrow_head_length = factor_escala * 0.1

    # Dibujo de las flechas de grados de libertad y sus etiquetas con longitud aumentada
    for i, gl in enumerate(MGL):
        for j in range(2):
            x_start = MC[i][j*2]
            y_start = MC[i][j*2 + 1]

            for k in range(2):
                gl_index = gl[j*2 + k]
                dx = arrow_length if k == 0 else 0
                dy = arrow_length if k != 0 else 0

                ax.arrow(x_start, y_start, dx, dy, head_width=arrow_head_width, head_length=arrow_head_length, fc='blue', ec='blue', width=arrow_width, length_includes_head=True)

                if k == 0:
                    text_x = x_start + dx + arrow_head_length / 2
                    text_y = y_start
                    ha, va = 'left', 'center'
                else:
                    text_x = x_start
                    text_y = y_start + dy + arrow_head_length / 2
                    ha, va = 'center', 'bottom'

                ax.text(text_x, text_y, str(gl_index), color='darkblue', fontsize=12, ha=ha, va=va, bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.2'))

    plt.show()
    
    

def plot_colored_matrix(KG, NGL, NGLL):
    
     
    # Definir los colores por defecto dentro de la función
    color_K0 = [1, 0.8, 0.8]  # Rojo claro
    color_K1 = [1, 1, 0.8]    # Amarillo claro
    color_K2 = [0.8, 1, 0.8]  # Verde claro
    color_K3 = [0.8, 1, 1]    # Cian claro

    # Crear una matriz de colores
    colors = np.zeros((NGL, NGL, 3))

    # Asignar colores a cada sección de la matriz KG
    colors[0:NGLL, 0:NGLL, :] = color_K0
    colors[0:NGLL, NGLL:NGL, :] = color_K1
    colors[NGLL:NGL, 0:NGLL, :] = color_K2
    colors[NGLL:NGL, NGLL:NGL, :] = color_K3

    # Crear una figura y un eje para el plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Usar 'imshow' para mostrar la matriz de colores
    ax.imshow(colors, interpolation='nearest', aspect='auto')

    # Añadir la matriz KG encima de los colores como texto
    for (i, j), z in np.ndenumerate(KG):
        ax.text(j, i, '{:0.0f}'.format(z), ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='None', edgecolor='None'))

    # Establecer límites para los ejes
    ax.set_xlim(-0.5, NGL-0.5)
    ax.set_ylim(NGL-0.5, -0.5)

    # Quitar los ticks si no son necesarios
    ax.set_xticks([])
    ax.set_yticks([])

    # Mostrar la matriz
    plt.show()

