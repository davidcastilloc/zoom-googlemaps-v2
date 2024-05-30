import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from lib.kml_process import find_polygons_in_area
from lib.geometry import get_area_polygon
import logging
from kmloader import ArbolBinarioDeAreas, Area

app = Flask(__name__)
CORS(app)

# Use environment variable for KML file path
#kml_file = os.getenv('KML_FILE_PATH', '../DATABASE/mixed-geometry-v2.kml')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Ejemplo de uso
areas = [
    Area("Area 1", (0, 0), (10, 10), "area1.kml"),
    Area("Area 2", (10, 10), (20, 20), "area2.kml"),
    Area("Area 3", (20, 20), (30, 30), "area3.kml")
]

arbol = ArbolBinarioDeAreas()
for area in areas:
    arbol.insertar(area)

def cargar_kml_area(coordenada_consulta: tuple):
    # Buscar KML por coordenadas
    # coordenada_consulta = (15, 15)
    archivo_kml = arbol.buscar_kml(coordenada_consulta)
    if archivo_kml:
        print(f"El archivo KML correspondiente es: {archivo_kml}")
    else:
        print("No se encontró un archivo KML para las coordenadas dadas.")
    return archivo_kml

#kml_file = cargar_kml_area((15, 15))

@app.post("/")
def index():
    try:
        bounds = request.get_json()
        if not bounds:
            return jsonify({"error": "Area limite no especificada"}), 400
        area_polygon = get_area_polygon(bounds)
        response = find_polygons_in_area(kml_file, area_polygon)
        return Response(response, mimetype='text/xml')
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": {"message": "Error de sistemas", "traceback": e}}), 500


@app.get("/")
def index_get():
    # Get Method  Info app version name and description
    return jsonify({"name": "Polygon API", "version": "2.0.0", "description": "API para obtener poligonos en un area"})

if __name__ == '__main__':
    app.run()
