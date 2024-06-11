# En este modulo se definen los mensajes de errores

import json

ERROR_PROCESSING = 'Error procesando el placemark {0},', \
    'con geometría {1} y coordenadas {2}'
ERROR_NO_POLYGONS = "No se encontraron poligonos en el perimetro especificado."
ERROR_NO_LINES = "No se encontraron líneas en el perimetro especificado."
ERROR_NO_AREA = "No se especificó un perimetro."

INFO_FOUND_POLYGONS = "Poligonos encontrados: {0}"
INFO_QUERY = "Consultando perimetro: {0}"
INFO_LOADING_KML = "Cargando Distritos..."
INFO_LOADED_KML = "Distritos cargados..."
INFO_STARTING_SERVER = "Iniciando servidor..."


def error_json(error):
    return json.dumps({'error': error})
