# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 09:26:23 2023

@author: Adriana
"""
# Punto 1

# Punto 2

import numpy as np


def calcular_esfuerzos(coordenadas_nodos, elements, mats, desp):
    
    esfuerzos = []
    
    coord_deformadas = coordenadas_nodos + desp
    
    for ele in elements:
        nodo_inicial, nodo_final = ele[1], ele[2]
        coordenada_inicial = coordenadas_nodos[nodo_inicial]
        coordenada_final = coordenadas_nodos[nodo_final]
        
        longitud_inicial = np.linalg.norm(coordenada_final - coordenada_inicial)
        
        modulo_de_young, area_transversal = mats[ele[0]]
        
        coordenada_desp_inicial = coord_deformadas[nodo_inicial]
        coordenada_desp_final = coord_deformadas[nodo_final]
        
        longitud_final = np.linalg.norm(coordenada_desp_final - coordenada_desp_inicial)
        
            
        elongacion =longitud_final - longitud_inicial
        
        
        esfuerzo = (modulo_de_young * elongacion) / longitud_inicial
        esfuerzos.append(esfuerzo)
    
    return esfuerzos


# PUNTO 3

import matplotlib.pyplot as plt



def graficar(coordenadas_nodos, elements, desp= None):
    
    conect = elements[:,1:]
    conexiones_nodos = [(int(a), int(b)) for a, b in conect]
    plt.figure(figsize=(12, 4))
    for conect in conexiones_nodos:
        nodo1, nodo2 = conect
        x1, y1 = coordenadas_nodos[nodo1]
        x2, y2 = coordenadas_nodos[nodo2]
        plt.plot([x1,x2],[y1,y2], "-b",marker='o')
        plt.title("Estado Original (Azul)")
        plt.axis("image")
        
    if desp is None:
        print("no se pidiá grafica de deformaciones")

    else: 
        coord_deformadas = (coordenadas_nodos + desp*10000)
        for conect in conexiones_nodos:
            nodo1, nodo2 = conect
            x3, y3 = coord_deformadas[nodo1]
            x4, y4 = coord_deformadas[nodo2]
            plt.plot([x3,x4],[y3,y4], "-r",marker='o')
            plt.axis("image")
            plt.title("Estado Original (Azul) vs. Estado Deformado (Rojo)")
    

#PUNTO 4

from matplotlib.colors import LinearSegmentedColormap, Normalize

def vis_esfuerzos(coordenadas_nodos, elements, resultados_esfuerzos, desp=None):
    conect = elements[:, 1:]
    nodes = coordenadas_nodos

    sismic1_cmap = LinearSegmentedColormap.from_list("sismic1", [(0.0, "blue"), (0.5, "white"), (1.0, "red")])

    Esfuerzo_max = np.max(np.abs(resultados_esfuerzos))
    norm = Normalize(vmin=-Esfuerzo_max, vmax=Esfuerzo_max)

    fig = plt.figure(figsize=(12, 4))

    for i, (nodo1, nodo2) in enumerate(conect):
        x1, y1 = coordenadas_nodos[nodo1]
        x2, y2 = coordenadas_nodos[nodo2]
        esfuerzo = resultados_esfuerzos[i]

        color = sismic1_cmap(norm(esfuerzo))
        plt.plot([x1, x2], [y1, y2], color=color, linewidth=2)

    plt.gca().set_aspect("equal", adjustable="box")

    if desp is None:
        print("No se pidió grafica de deformaciones")
        
        
    else:
        plt.clf()  # Borra la figura anterior

        for i, (nodo1, nodo2) in enumerate(conect):
            x1, y1 = coordenadas_nodos[nodo1]
            x2, y2 = coordenadas_nodos[nodo2]
            esfuerzo = resultados_esfuerzos[i]
            plt.plot([x1, x2], [y1, y2], color='grey', linewidth=1)

        coords_deformadas = coordenadas_nodos + (desp*10000)

        for i, conect in enumerate(conect):
            nodo1, nodo2 = conect
            x3, y3 = coords_deformadas[nodo1]
            x4, y4 = coords_deformadas[nodo2]
            esfuerzo = resultados_esfuerzos[i]
            color = sismic1_cmap(norm(esfuerzo))
            plt.plot([x3, x4], [y3, y4], color=color, linewidth=3)

    sm = plt.cm.ScalarMappable(cmap=sismic1_cmap, norm=norm)
    sm.set_array([])
    colorbar_ax = plt.figure().add_axes([0.85, 0.1, 0.03, 0.8])  # convenciones de colores
    plt.colorbar(sm, cax=colorbar_ax, label="esfuerzos")
    ax = plt.gca()
    ax.set_facecolor("m")
    plt.show()


# Punto 5

def calc_peso(nodes, elements, mats, densidades):
    secciones = mats[:, 1:]
    num_nodes = len(nodes)
    conect = elements[:, 1:]
    carga_vertical = np.zeros(num_nodes)
    
    for i in range(len(conect)):
        nodo_inicial, nodo_final = conect[i]
        seccion = secciones[0]
        densidad = densidades[0]
        
        x1, y1 = nodes[nodo_inicial]
        x2, y2 = nodes[nodo_final]
        
        longitud = np.sqrt((x2 -x1)**2 + (y2 - y1)**2)
        peso_elemento = 0.5 * longitud + seccion *densidad * 9.81
        
        carga_vertical[nodo_inicial] += peso_elemento
        carga_vertical[nodo_final] += peso_elemento
    return carga_vertical



  
