from shapely.geometry import Polygon, Point
from rtree import index

# Crea un índice R-tree
idx = index.Index()

# Define algunas áreas (polígonos)
areas = [
    ("kml_1", Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])),
    ("kml_2", Polygon([(2, 2), (3, 2), (3, 3), (2, 3)])),
    ("kml_3", Polygon([(4, 4), (5, 4), (5, 5), (4, 5)])),
    ("kml_3", Polygon([(4, 4), (5, 4), (5, 5), (4, 5)])),
    ("kml_3", Polygon([(4, 4), (5, 4), (5, 5), (4, 5)])),
    ("kml_3", Polygon([(4, 4), (5, 4), (5, 5), (4, 5)])),
    ("kml_3", Polygon([(4, 4), (5, 4), (5, 5), (4, 5)])),
    ("kml_3", Polygon([(4, 4), (5, 4), (5, 5), (4, 5)])),
]

# Inserta las áreas en el índice
for i, (nombre, poligono) in enumerate(areas):
    idx.insert(i, poligono.bounds, obj=nombre)  # Usamos 'bounds' para obtener el rectángulo que encierra el polígono

# Realiza una consulta puntual
punto_consulta = Point(2.5, 2.5)
ids_areas_cercanas = list(idx.intersection(punto_consulta.coords[0]))


# Imprime las áreas que contienen el punto
for id_area in ids_areas_cercanas:
    nombre_area = areas[id_area][1]
    print(f"Área {nombre_area} contiene el punto")
    print(areas[id_area][0])
    print()
