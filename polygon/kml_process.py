import logging as log
from logging.handlers import RotatingFileHandler
import os
from pykml import parser
from shapely.geometry import Polygon, LineString, GeometryCollection
from lxml import etree

from messages import ERROR_NO_POLYGONS, INFO_FOUND_POLYGONS, INFO_QUERY, error_json

# Configuración del registro de eventos
log_file = 'test_log.log'  # Nombre del archivo de registro
log.basicConfig(level=log.DEBUG, format='%(asctime)s [%(levelname)s] - %(message)s')

# Configuración del manejador de archivos de registro
file_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=10)
file_handler.setFormatter(log.Formatter('%(asctime)s [%(levelname)s] - %(message)s'))
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

def add_placemark_to_document(document, geometry_type, coords):
    """Agrega un placemark a un documento KML.
    Args:
        document (etree.Element): el documento KML
        geometry_type (str): la geometría del placemark
        coords (list): las coordenadas del placemark
    """
    placemark_element = etree.SubElement(document, "Placemark")
    if geometry_type == 'Polygon':
        polygon_element = etree.SubElement(placemark_element, "Polygon")
        outer_boundary = etree.SubElement(polygon_element, "outerBoundaryIs")
        linear_ring = etree.SubElement(outer_boundary, "LinearRing")
        coord_element = etree.SubElement(linear_ring, "coordinates")
        coord_element.text = " ".join([f"{coord[1]},{coord[0]}" for coord in coords[0]])
        for inner_coords in coords[1:]:
            inner_boundary = etree.SubElement(polygon_element, "innerBoundaryIs")
            linear_ring = etree.SubElement(inner_boundary, "LinearRing")
            coord_element = etree.SubElement(linear_ring, "coordinates")
            coord_element.text = " ".join([f"{coord[1]},{coord[0]}" for coord in inner_coords])
    elif geometry_type == 'LineString':
        linestring_element = etree.SubElement(placemark_element, "LineString")
        coord_element = etree.SubElement(linestring_element, "coordinates")
        coord_element.text = " ".join([f"{coord[1]},{coord[0]}" for coord in coords])

def get_geometry_and_coordinates(p):
    """Extrae la geometría y las coordenadas de un placemark de un KML.
    Args:
        p (etree.Element): Un elemento de un KML.
    Returns:
        tuple: Un tuple con la geometría y las coordenadas.
    """
    if hasattr(p, 'Polygon'):
        outer_boundary = p.Polygon.outerBoundaryIs.LinearRing.coordinates.text.strip()
        outer_coords = parse_coordinates(outer_boundary)
        inner_boundaries = p.Polygon.findall('.//{http://www.opengis.net/kml/2.2}innerBoundaryIs')
        inner_coords = [parse_coordinates(b.LinearRing.coordinates.text.strip()) for b in inner_boundaries]
        return 'Polygon', [outer_coords] + inner_coords
    elif hasattr(p, 'LineString'):
        coords_text = p.LineString.coordinates.text.strip()
        coords = parse_coordinates(coords_text)
        return 'LineString', coords
    elif hasattr(p, 'MultiGeometry'):
        geometries = p.MultiGeometry.getchildren()
        multi_geometries = []
        for g in geometries:
            gt, coord = get_geometry_and_coordinates(g)
            if gt and coord:
                if gt == 'Polygon':
                    multi_geometries.append(Polygon(coord[0], coord[1:]))
                elif gt == 'LineString':
                    multi_geometries.append(LineString(coord))
        return 'MultiGeometry', multi_geometries
    return None, None

def parse_coordinates(ct):
    """Parsea las coordenadas de un string de coordenadas.
    Args:
        ct (str): Un string de coordenadas en formato "longitud,latitud".
    Returns:
        list: Una lista de coordenadas en formato [(latitud, longitud)].
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
        placemarks = kml_file.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
        for p in placemarks:
            try:
                gt, coords = get_geometry_and_coordinates(p)
                if coords:
                    if gt == 'Polygon':
                        geometry = Polygon(coords[0], coords[1:] if len(coords) > 1 else None)
                    elif gt == 'LineString':
                        geometry = LineString(coords)
                    elif gt == 'MultiGeometry':
                        geometry = GeometryCollection(coords)
                    if geometry.intersects(area_polygon):
                        features_count += 1
                        if gt == 'MultiGeometry':
                            for g in coords:
                                if isinstance(g, Polygon):
                                    add_placemark_to_document(document, 'Polygon', [list(g.exterior.coords)] + [list(ring.coords) for ring in g.interiors])
                                elif isinstance(g, LineString):
                                    add_placemark_to_document(document, 'LineString', list(g.coords))
                        else:
                            add_placemark_to_document(document, gt, coords)
            except Exception as e:
                placemark_name = p.find('.//{http://www.opengis.net/kml/2.2}name')
                placemark_name_text = placemark_name.text if placemark_name is not None else "Unknown"
                log.error(f"Error procesando el placemark {placemark_name_text}, con geometría {gt} y coordenadas {coords}: {str(e)}")
                continue

    if features_count == 0:
        return error_json(ERROR_NO_POLYGONS)

    kml_string = etree.tostring(kml_output, pretty_print=False, xml_declaration=True, encoding='UTF-8')
    log.debug(INFO_FOUND_POLYGONS.format(features_count))
    return kml_string
