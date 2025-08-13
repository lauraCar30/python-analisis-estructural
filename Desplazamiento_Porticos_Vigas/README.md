# Desplazamiento en Pórticos y Vigas

**Descripción:**  
Script en Python para calcular los desplazamientos en estructuras tipo pórtico y viga, empleando el método de rigidez.  
Incluye el armado de matrices, aplicación de condiciones de frontera y visualización de resultados.

## Funcionalidades
- Definición de geometría, propiedades mecánicas y conectividades.
- Ensamblaje de la matriz de rigidez global.
- Aplicación de cargas y restricciones de movimiento.
- Cálculo de desplazamientos nodales y reacciones en apoyos.
- Generación de diagramas y representación gráfica de la estructura.

## Entradas
- **Coordenadas nodales**: posición de cada nodo (m).
- **Propiedades mecánicas**: módulo de elasticidad (Pa), inercia (m⁴), área (m²).
- **Conectividad**: elementos con sus nodos inicial y final.
- **Condiciones de borde**: grados de libertad restringidos.
- **Cargas**: nodales y distribuidas.

## Salidas
- Desplazamientos nodales.
- Reacciones en apoyos.
- Diagramas de momento, cortante y axial (si aplica).

**Autor:** Laura Cardona Arenas  
**Última actualización:** 2025-08-12
