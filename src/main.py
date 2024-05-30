import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from lib.kml_process import find_polygons_in_area
from lib.geometry import get_area_polygon
import logging

app = Flask(__name__)
CORS(app)

# Use environment variable for KML file path
#kml_file = os.getenv('KML_FILE_PATH', '../DATABASE/mixed-geometry-v2.kml')

# Set up logging
logging.basicConfig(level=logging.INFO)


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
    return jsonify({"name": "Polygon API", "version": "1.0.0", "description": "API para obtener poligonos en un area"})

if __name__ == '__main__':
    app.run()
