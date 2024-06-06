import logging
from logging.handlers import RotatingFileHandler
import os
from pykml import parser
from shapely.geometry import Polygon, LineString
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
        raise (FileNotFoundError)


def load_kml_files(directory):
    kml_files = []
    for file in os.listdir(directory):
        if file.endswith(".kml"):
            print(file)
            kml_files.append(load_kml_file(os.path.join(directory, file)))
    return kml_files


def create_kml_document():
    kml_output = etree.Element("kml", xmlns=KML_NAMESPACE)
    document = etree.SubElement(kml_output, "Document")
    return kml_output, document


def add_placemark_to_document(document, geometry_type, cord):
    placemark_element = etree.SubElement(document, "Placemark")
    if geometry_type == 'Polygon':
        polygon_element = etree.SubElement(placemark_element, "Polygon")
        o_b = etree.SubElement(polygon_element, "outerBoundaryIs")
        l_r = etree.SubElement(o_b, "LinearRing")
        coord_e = etree.SubElement(l_r, "coordinates")
        coord_e.text = " ".join([f"{coord[1]},{coord[0]}" for coord in cord])
    elif geometry_type == 'LineString':
        linestring_element = etree.SubElement(placemark_element, "LineString")
        coord_e = etree.SubElement(linestring_element, "coordinates")
        coord_e.text = " ".join([f"{coord[1]},{coord[0]}" for coord in cord])


def find_polygons_and_lines_in_area(kmlbuffer, area_polygon):
    logging.info(f"Consultando área: {area_polygon}")
    kml_output, document = create_kml_document()
    features_within_area = 0
    logging.info("Buscando polígonos y líneas en el área")
    for kml_file in kmlbuffer:
        for p in kml_file.Document.Folder.Placemark:
            try:
                gt = None
                cord = None
                id = None
                if hasattr(p, 'Polygon'):
                    gt = 'Polygon'
                    cord = p.Polygon.outerBoundaryIs.LinearRing.coordinates.text.strip()
                    id = p.name
                elif hasattr(p, 'LineString'):
                    gt = 'LineString'
                    cord = p.LineString.coordinates.text.strip()
                    id = p.name
                if cord:
                    ct = [tuple(map(float, c.split(',')[:2])) for c in cord.split()]
                    if gt == 'Polygon':
                        geometry = Polygon(ct)
                    elif gt == 'LineString':
                        geometry = LineString(ct)
                    if geometry.intersects(area_polygon):
                        features_within_area += 1
                        add_placemark_to_document(document, gt, ct)
            except Exception:
                logging.error(f"Error procesando el placemark ID: {id} {gt} {ct}", exc_info=True)
                continue

    if features_within_area == 0:
        return json.dumps({'error': 'No se encontraron características en el área especificada.'})

    kml_string = etree.tostring(kml_output, pretty_print=False, xml_declaration=True, encoding='UTF-8')
    logging.debug(f"Características encontradas: {features_within_area}")
    return kml_string
