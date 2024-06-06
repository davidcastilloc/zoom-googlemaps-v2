import logging as log
from logging.handlers import RotatingFileHandler
import os
from pykml import parser
from shapely.geometry import Polygon, LineString
from lxml import etree

from lib.messages import ERROR_NO_POLYGONS, \
    INFO_FOUND_POLYGONS, INFO_QUERY, error_json

# Configuración del registro de eventos
log_file = 'test_log.log'  # Nombre del archivo de registro
log.basicConfig(level=log.DEBUG,
                format='%(asctime)s [%(levelname)s] - %(message)s')

# Configuración del manejador de archivos de registro
file_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=10)
file_handler.setFormatter(log.Formatter(
    '%(asctime)s [%(levelname)s] - %(message)s'))
log.getLogger('').addHandler(file_handler)

KML_NAMESPACE = "http://www.opengis.net/kml/2.2"


def load_kml_file(kml_file):
    """Carga un archivo KML.
    Args:
        kml_file (str): Nombre del archivo KML.
    Returns:
        Documento KML.
    """
    try:
        with open(kml_file, 'rb') as f:
            return parser.parse(f).getroot()
    except FileNotFoundError:
        raise (FileNotFoundError)


def load_kml_files(directory):
    """Carga todos los archivos KML en un directorio.
    Args:
        directory (str): Directorio de los archivos KML.
    Returns:
        Lista de documentos KML.
    """
    kml_files = []
    for file in os.listdir(directory):
        if file.endswith(".kml"):
            log.debug(f"Cargando {file}")
            kml_files.append(load_kml_file(os.path.join(directory, file)))
    return kml_files


def create_kml_document():
    """Crea un documento KML vacío.
    Returns:
        KML documento.
    """
    kml_output = etree.Element("kml", xmlns=KML_NAMESPACE)
    document = etree.SubElement(kml_output, "Document")
    return kml_output, document


def add_placemark_to_document(document, geometry_type, cord):
    """ agrega un placemark a un documento KML
    Args:
        document (etree.Element): el documento KML
        geometry_type (str): la geometría del placemark
        cord (list): los coordenadas del placemark
    """
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


def get_geometry_and_coordinates(p):
    """_summary_
        Extrae la geometría y los coordenadas de un placemark de un KML.

    Args:
        p (etree.Element): Un elemento de un KML.

    Returns:
        tuple: Un tuple con la geometría y los coordenadas.
    """
    if hasattr(p, 'Polygon'):
        ct = p.Polygon.outerBoundaryIs.LinearRing.coordinates.text.strip()
        coord = parse_coordinates(ct)
        return 'Polygon', coord
    elif hasattr(p, 'LineString'):
        ct = p.LineString.coordinates.text.strip()
        coord = parse_coordinates(ct)
        return 'LineString', coord
    return None, None


def parse_coordinates(ct):
    """ Parsea los coordenadas de un string de coordenadas.
    Args:
        ct (str): Un string de coordenadas.
    Returns:
        list: Una lista de coordenadas.
    """
    return [tuple(map(float, c.split(',')[:2])) for c in ct.split()]


def find_polygons_and_lines_in_area(kmlbuffer, area_polygon):
    """Busca polígonos y líneas en un área especificada.
    Args:
        kmlbuffer (list): Lista de documentos KML.
        area_polygon (Polygon): Área especificada.
    Returns:
        str: KML con los polígonos y líneas encontrados.
    """
    log.info(INFO_QUERY.format(area_polygon))
    kml_output, document = create_kml_document()
    features_count = 0
    for kml_file in kmlbuffer:
        for p in kml_file.Document.Folder.Placemark:
            try:
                gt, coord = get_geometry_and_coordinates(p)
                if coord:
                    if gt == 'Polygon':
                        geometry = Polygon(coord)
                    elif gt == 'LineString':
                        geometry = LineString(coord)
                    if geometry.intersects(area_polygon):
                        features_count += 1
                        add_placemark_to_document(document, gt, coord)
            except Exception:
                log.error(f"Error procesando el placemark {p.name}, con geometría {gt} y coordenadas {coord}")
                continue

    if features_count == 0:
        return error_json(ERROR_NO_POLYGONS)

    kml_string = etree.tostring(kml_output,
                                pretty_print=False,
                                xml_declaration=True,
                                encoding='UTF-8')
    log.debug(INFO_FOUND_POLYGONS.format(features_count))
    return kml_string
