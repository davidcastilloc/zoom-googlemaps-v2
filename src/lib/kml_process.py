import logging
from logging.handlers import RotatingFileHandler
from pykml import parser
from shapely.geometry.polygon import Polygon
from lxml import etree
import json

# Configuración del registro de eventos
log_file = 'test_log.log'  # Nombre del archivo de registro
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] - %(message)s')

# Configuración del manejador de archivos de registro
file_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s] - %(message)s'))
logging.getLogger('').addHandler(file_handler)

KML_NAMESPACE = "http://www.opengis.net/kml/2.2"


def load_kml_file(kml_file):
    try:
        with open(kml_file, 'rb') as f:
            return parser.parse(f).getroot()
    except FileNotFoundError:
        raise(FileNotFoundError)


def create_kml_document():
    kml_output = etree.Element("kml", xmlns=KML_NAMESPACE)
    document = etree.SubElement(kml_output, "Document")
    return kml_output, document


def find_polygons_in_area(kml_file, area_polygon):
    logging.info("Consultando area: " + str(area_polygon))
    kml_root = load_kml_file(kml_file)

    if kml_root is None:
        error_message = {'error': 'El archivo KML no fue encontrado.'}
        # Retorna un mensaje de error y 0 polígonos encontrados
        return json.dumps(error_message), 0

    kml_output, document = create_kml_document()
    polygons_within_area = 0  # Inicializa el contador de polígonos encontrados
    logging.info("Buscando poligonos en el area")
    for placemark in kml_root.Document.Folder.Placemark:
        try:
            coordinates = placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text.strip()
            coordinates = coordinates.split()
            coordinates = [c.split(',')[:2] for c in coordinates]
            polygon = Polygon(coordinates)
            if polygon.intersects(area_polygon):
                # Usa el registro en lugar de print
                #if logging.getLogger().level == logging.DEBUG:
                #    logging.debug("Polígono encontrado: %s", polygon)
                polygons_within_area += 1
                # Agregar este polígono al KML de salida
                print(placemark.Polygon.outerBoundaryIs.LinearRing.coordinates)
                # Agregar este polígono al KML de salida
                placemark_element = etree.SubElement(document, "Placemark")
                polygon_element = etree.SubElement(placemark_element, "Polygon")
                outer_boundary_element = etree.SubElement(polygon_element, "outerBoundaryIs")
                linear_ring_element = etree.SubElement(outer_boundary_element, "LinearRing")
                coordinates_element = etree.SubElement(linear_ring_element, "coordinates")
                coordinates_element.text = " ".join([f"{coord[1]},{coord[0]}" for coord in coordinates])
        except AttributeError:
            # Handle the AttributeError here, or log an error if needed.
            pass

    # Comprobar si se encontraron polígonos
    if polygons_within_area == 0:
        error_message = {
            'error': 'No se encontraron polígonos en el área especificada.'}
        # Retorna un mensaje de error
        return json.dumps(error_message)

    # Convertir el documento KML en una cadena KML válida
    kml_string = etree.tostring(kml_output, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    logging.debug(f"Polígonos encontrados : {polygons_within_area}")
    return kml_string
