from setuptools import setup, find_packages
# INSTALL REQUIREMENTS
""" autopep8==2.2.0
blinker==1.6.3
build==1.2.1
click==8.1.7
colorama==0.4.6
flake8==7.0.0
Flask==3.0.0
Flask-Cors==4.0.1
importlib-metadata==6.8.0
itsdangerous==2.1.2
Jinja2==3.1.2
lxml==4.9.3
MarkupSafe==2.1.3
mccabe==0.7.0
numpy==1.24.4
packaging==24.0
pycodestyle==2.11.1
pyflakes==3.2.0
pykml==0.2.0
pyproject_hooks==1.1.0
Rtree==1.2.0
shapely==2.0.2
Werkzeug==3.0.0
zipp==3.17.0 """
# END INSTALL REQUIREMENTS
setup(
    name="polygon-api-v2",
    version="2.0.0",
    description="API para obtener poligonos en un area",
    author="David Castillo",
    author_email="vikruzdavid@gmail.com",
    url="https://github.com/davidcastilloc/zoom-googlemaps-v2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "autopep8==2.2.0",
        "blinker==1.6.3",
        "build==1.2.1",
        "click==8.1.7",
        "colorama==0.4.6",
        "flake8==7.0.0",
        "Flask==3.0.0",
        "Flask-Cors==4.0.1",
        "importlib-metadata==6.8.0",
        "itsdangerous==2.1.2",
        "Jinja2==3.1.2",
        "lxml==4.9.3",
        "MarkupSafe==2.1.3",
        "mccabe==0.7.0",
        "numpy==1.24.4",
        "packaging==24.0",
        "pycodestyle==2.11.1",
        "pyflakes==3.2.0",
        "pykml==0.2.0",
        "pyproject_hooks==1.1.0",
        "Rtree==1.2.0",
        "shapely==2.0.2",
        "Werkzeug==3.0.0",
        "zipp==3.17.0",
    ],
    entry_points={
        "console_scripts": [
            "app=app:app",
        ],
    },
)
