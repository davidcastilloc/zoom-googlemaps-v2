import unittest
from shapely.geometry import Polygon


class TestFindPolygonsInArea(unittest.TestCase):
    def setUp(self):
        # Crea una instancia de un polígono para usar en las pruebas
        # Debes ajustar las coordenadas según tus necesidades
        self.area_polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
        self.kml_file = 'tests/test.kml'


if __name__ == '__main__':
    unittest.main()
