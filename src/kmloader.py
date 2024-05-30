class Area:
    def __init__(self, nombre, coord_inicial, coord_final, archivo_kml):
        self.nombre = nombre
        self.coord_inicial = coord_inicial
        self.coord_final = coord_final
        self.archivo_kml = archivo_kml

    def contiene(self, coordenada):
        return (self.coord_inicial[0] <= coordenada[0] <= self.coord_final[0] and
                self.coord_inicial[1] <= coordenada[1] <= self.coord_final[1])

class Nodo:
    def __init__(self, area):
        self.area = area
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioDeAreas:
    def __init__(self):
        self.raiz = None

    def insertar(self, area):
        if self.raiz is None:
            self.raiz = Nodo(area)
        else:
            self._insertar_recursivo(area, self.raiz)

    def _insertar_recursivo(self, area, nodo_actual):
        if area.coord_inicial < nodo_actual.area.coord_inicial:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = Nodo(area)
            else:
                self._insertar_recursivo(area, nodo_actual.izquierdo)
        else:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = Nodo(area)
            else:
                self._insertar_recursivo(area, nodo_actual.derecho)

    def buscar_kml(self, coordenada):
        return self._buscar_kml_recursivo(coordenada, self.raiz)

    def _buscar_kml_recursivo(self, coordenada, nodo_actual):
        if nodo_actual is None:
            return None
        if nodo_actual.area.contiene(coordenada):
            return nodo_actual.area.archivo_kml
        elif coordenada < nodo_actual.area.coord_inicial:
            return self._buscar_kml_recursivo(coordenada, nodo_actual.izquierdo)
        else:
            return self._buscar_kml_recursivo(coordenada, nodo_actual.derecho)
