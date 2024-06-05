import unittest
from src.kmloader import ArbolBinarioDeAreas, Area
class TestArea(unittest.TestCase):

    def test_contiene(self):
        area = Area("Area 1", (-77.0878689999999978, -12.0462360000000004), (-76.7948169999999948, -11.7351469999999996), "150106-CARABAYLLO-1_prod.kml")
        self.assertTrue(area.contiene((-77.0878689999999978, -12.0462360000000004)))
        self.assertFalse(area.contiene((-76.7948169999999948, -11.7351469999999996)))

class TestArbolBinarioDeAreas(unittest.TestCase):
    def setUp(self):
        self.areas = [
            Area("Area 1", (-77.0878689999999978, -12.0462360000000004), (-76.7948169999999948, -11.7351469999999996), "150106-CARABAYLLO-1_prod.kml"),
            Area("Area 2",  (-77.0878689999999978, -12.0462360000000004), (-76.7948169999999948, -11.7351469999999996), "150106-CARABAYLLO-2_prod.kml"),
            Area("Area 3",  (-77.0878689999999978, -12.0462360000000004), (-76.7948169999999948, -11.7351469999999996), "150108-CHORRILLOS_PROD.kml")
        ]
        self.arbol = ArbolBinarioDeAreas()
        for area in self.areas:
            self.arbol.insertar(area)

    def test_buscar_kml(self):
        self.assertEqual(self.arbol.buscar_kml((5, 5)), "150106-CARABAYLLO-1_prod.kml")
        self.assertEqual(self.arbol.buscar_kml((15, 15)), "150106-CARABAYLLO-2_prod.kml")
        self.assertEqual(self.arbol.buscar_kml((25, 25)), "150108-CHORRILLOS_PROD.kml")
        self.assertIsNone(self.arbol.buscar_kml((-1, -1)))
        self.assertIsNone(self.arbol.buscar_kml((31, 31)))

if __name__ == '__main__':
    unittest.main()
