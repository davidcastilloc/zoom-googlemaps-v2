import unittest
from src.kmloader import ArbolBinarioDeAreas, Area
class TestArea(unittest.TestCase):

    def test_contiene(self):
        area = Area("Area 1", (0, 0), (10, 10), "area1.kml")
        self.assertTrue(area.contiene((5, 5)))
        self.assertFalse(area.contiene((-1, -1)))
        self.assertFalse(area.contiene((11, 11)))

class TestArbolBinarioDeAreas(unittest.TestCase):

    def setUp(self):
        self.areas = [
            Area("Area 1", (0, 0), (10, 10), "area1.kml"),
            Area("Area 2", (10, 10), (20, 20), "area2.kml"),
            Area("Area 3", (20, 20), (30, 30), "area3.kml")
        ]
        self.arbol = ArbolBinarioDeAreas()
        for area in self.areas:
            self.arbol.insertar(area)

    def test_buscar_kml(self):
        self.assertEqual(self.arbol.buscar_kml((5, 5)), "area1.kml")
        self.assertEqual(self.arbol.buscar_kml((15, 15)), "area2.kml")
        self.assertEqual(self.arbol.buscar_kml((25, 25)), "area3.kml")
        self.assertIsNone(self.arbol.buscar_kml((-1, -1)))
        self.assertIsNone(self.arbol.buscar_kml((31, 31)))

if __name__ == '__main__':
    unittest.main()
