from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open
from os import path
import subprocess
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))

with open(path.join(here,'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name = 'edc',

        version='0.1.0',
        packages = ['edc','edc.datasets','edc'],
        description = 'Convenience library for reusable utility functions and datasets',
        author = 'Elijah C',
        author_email = 'elijah.christensen@cuanschutz.edu',
        url = 'https://github.com/elijahc/edc',
        install_requires=[
            'wget',
            'tqdm',
            'pyreadstat',
            'imageio',
        ],
        classifiers = [],
)
