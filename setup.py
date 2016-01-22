from setuptools import setup
from setuptools.extension import Extension

setup(
    name = 'page_finder',
    version = '0.0.1',
    install_requires = [
        'numpy',
        'scrapely'
    ],
    ext_modules = [Extension("edit_distance", ["edit_distance.c"])],
)
