#/bin/bash
python -m build
pip uninstall -y PolygonsAPI
pip install dist/*.whl