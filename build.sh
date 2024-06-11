#/bin/bash
python -m build
pip uninstall -y polygon
pip install dist/polygon-2.0.0-py3-none-any.whl