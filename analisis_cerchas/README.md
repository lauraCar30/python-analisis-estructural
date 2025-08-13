# Análisis de Cerchas

**Descripción:**  
Scripts en Python para el análisis estructural de cerchas planas mediante el método de rigidez.  
Incluyen rutinas para definir geometría y propiedades, ensamblar la matriz global, aplicar condiciones de borde, resolver el sistema y visualizar resultados.

## Funcionalidades
- Definición de coordenadas nodales y conectividades.
- Asignación de propiedades mecánicas (área, módulo de elasticidad).
- Ensamblaje de la matriz de rigidez global.
- Aplicación de cargas y restricciones.
- Cálculo de desplazamientos y reacciones.
- Visualización gráfica de la cercha y sus grados de libertad.
- Representación gráfica de la matriz de rigidez global con codificación de colores.

## Archivos
- **Analisis_cerchas.py** → Funciones y rutinas principales para el análisis y graficación.
- **Programa_Cerchas.ipynb** → Cuaderno interactivo con ejecución paso a paso y visualización.

## Entradas
- Matriz de coordenadas nodales (m).
- Matriz de conectividad de elementos.
- Propiedades mecánicas: módulo de elasticidad (Pa), área (m²).
- Condiciones de borde (grados de libertad restringidos).
- Cargas aplicadas (N).

## Salidas
- Desplazamientos nodales.
- Reacciones en apoyos.
- Diagramas y representación de la estructura.

**Autor:** Laura Cardona Arenas  
**Última actualización:** 2025-08-12
