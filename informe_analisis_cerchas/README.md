# Modelado y Evaluación Estructural – Cerchas Planas

**Descripción:**  
Conjunto de scripts y notebook en Python para el modelado, análisis y evaluación estructural de cerchas planas, aplicando el método de rigidez.  
Incluye funciones auxiliares, desarrollo del modelo y ejecución de casos de prueba.

## Archivos
- **Funciones_2.py** → Módulo con funciones auxiliares para cálculos y ensamblaje de matrices.
- **Modelado y Evaluación Estructural Cerchas.ipynb** → Notebook principal con el flujo de análisis, explicación paso a paso y visualización de resultados.
- **plane_trusses.py** → Script de análisis y resolución para cerchas planas.

## Funcionalidades
- Definición de nodos, elementos y conectividades.
- Asignación de propiedades mecánicas (área, módulo de elasticidad).
- Ensamblaje de matriz de rigidez global.
- Aplicación de cargas y restricciones.
- Cálculo de desplazamientos nodales y reacciones en apoyos.
- Visualización gráfica de la estructura y sus grados de libertad.

## Entradas
- Coordenadas nodales (m).
- Conectividad de elementos.
- Propiedades mecánicas: módulo de elasticidad (Pa), área (m²).
- Condiciones de borde.
- Cargas aplicadas (N).

## Salidas
- Desplazamientos nodales.
- Reacciones en apoyos.
- Diagramas y representación gráfica de la estructura.

**Autor:** Laura Cardona Arenas  
**Última actualización:** 2025-08-12
