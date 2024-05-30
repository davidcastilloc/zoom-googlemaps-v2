from shapely.geometry import Polygon


def get_area_polygon(bounds):
    """
    Genera un polígono a partir de las coordenadas proporcionadas en el argumento JSON.

    Args:
        bounds (dict): Un diccionario con las coordenadas de los límites del área.

    Returns:
        Polygon: El polígono que representa el área a consultar.
    """

    # Crea un objeto Polygon a partir de las coordenadas en el orden correcto
    polygon_coordinates = [
        (bounds["west"], bounds["south"]),
        (bounds["west"], bounds["north"]),
        (bounds["east"], bounds["north"]),
        (bounds["east"], bounds["south"]),
        # Añade el primer punto nuevamente para cerrar el polígono
        (bounds["west"], bounds["south"]),
    ]
    return Polygon(polygon_coordinates)
