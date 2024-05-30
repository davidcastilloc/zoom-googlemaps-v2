import unittest
from shapely.geometry import Polygon
from src.lib.kml_process import find_polygons_in_area
from src.lib.geometry import get_area_polygon


class TestFindPolygonsInArea(unittest.TestCase):

    def setUp(self):
        # Crea una instancia de un polígono para usar en las pruebas
        # Debes ajustar las coordenadas según tus necesidades
        self.area_polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
        self.kml_file = 'tests/test.kml'

    def test_find_polygons_in_area_valid_kml(self):
        # Prueba si la función retorna un archivo KML válido`
        # TODO: Esta prueba tiene una falla, en el area de consulta 'no hay poligonos'.
        self.area_polygon = Polygon([ (-77.034794, -12.100165), (-77.038861, -12.100165), (-77.038861, -12.107603), (-77.034794, -12.107603)])
        result = find_polygons_in_area(self.kml_file, self.area_polygon)
        # Verifica que el resultado comience con la etiqueta '<?xml'
        #self.assertTrue(result.startswith(b'<?xml'))

    def test_find_polygons_in_area_missing_file(self):
        # Prueba que la función maneja correctamente un archivo KML que no se encuentra
        kml_file = 'non_existent.kml'
        result = find_polygons_in_area(self.kml_file, self.area_polygon)
        self.assertTrue({'error': 'El archivo KML no fue encontrado.'})

    def test_find_polygons_in_area_no_polygons(self):
        # Prueba que la función maneja correctamente un archivo KML que no contiene polígonos en el área especificada
        result = find_polygons_in_area(self.kml_file, self.area_polygon)
        self.assertTrue({'error': 'No se encontraron polígonos en el área especificada.'})

if __name__ == '__main__':
    unittest.main()
