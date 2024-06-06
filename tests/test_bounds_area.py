import unittest
import shapely.geometry

from polygon.geometry import get_area_polygon
# Asegúrate de importar la función desde tu módulo


class TestGetAreaPolygon(unittest.TestCase):

    def test_get_area_polygon(self):
        # Define los límites de prueba
        bounds = {
            "south": -12.099629892051706,
            "west": -77.03630851882374,
            "north": -12.09622046087039,
            "east": -77.03201698439992
        }

        # Llama a la función para obtener el polígono
        polygon = get_area_polygon(bounds)

        # Verifica que la salida sea una instancia de shapely.geometry.Polygon
        self.assertIsInstance(polygon, shapely.geometry.Polygon)

        # Verifica que el polígono tenga un área positiva
        self.assertGreater(polygon.area, 0)


if __name__ == '__main__':
    unittest.main()
