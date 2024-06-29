# -*- coding: utf-8 -*-
"""
    API para obtener poligonos y LineStrings Recibiendo
    como parametro un perimetro
    METHODS:
        GET /
            Información sobre la API
        POST /
            Recibiendo como parametro un perimetro,
            devuelve un KML con los poligonos y LineStrings
            que se encuentran dentro del perimetro
"""
import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from kml_process import find_polygons_and_lines_in_area, load_kml_files
from geometry import get_area_polygon
import messages as msg
import logging as log

app = Flask(__name__)
CORS(app)

# Set up logging
log.basicConfig(level=log.INFO)

# KML LOAD DIRECTORY
kml_path = os.getenv("KML_FILE_PATH", "DATABASE")
with app.app_context():
    log.info(msg.INFO_LOADING_KML)
    kml_buffer = load_kml_files(os.path.join(os.getcwd(), kml_path))
    log.info(msg.INFO_LOADED_KML)
    log.info(msg.INFO_STARTING_SERVER)


@app.post("/")
def index():
    try:
        bounds = request.get_json()
        if not bounds:
            return jsonify({"error": msg.ERROR_NO_AREA}), 400
        area_polygon = get_area_polygon(bounds)
        response = find_polygons_and_lines_in_area(kml_buffer, area_polygon)
        return Response(response, mimetype="text/xml")
    except Exception as e:
        log.error(f"An error occurred: {e}")
        return jsonify({
            "error":
                {
                    "message": "Error de sistemas",
                    "traceback": e
                }
            }), 500


@app.get("/")
def index_get():
    # Get Method  Info app version name and description
    return jsonify(
        {
            "name": "Polygons API",
            "version": "2.0.0",
            "description": "API para obtener poligonos y LineStrings Recibiendo como parametro un perimetro",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
