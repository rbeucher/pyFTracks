from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy
from os import path

MAJOR = 0
MINOR = 1
MICRO = 5
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

extensions = [Extension("ketcham", ["pyFTracks/ketcham.pyx",
                                    "pyFTracks/src/ketcham.c"],
                        include_dirs=["pyFTracks/include"])]

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='pyFTracks',
    version=VERSION,
    description='Fission Track Modelling and Analysis with Python',
    ext_modules=cythonize(extensions),
    include_dirs=[numpy.get_include()],
    long_description=long_description,
    url='https://github.com/rbeucher/pyFTracks.git',
    author='Romain Beucher',
    author_email='romain.beucher@unimelb.edu.au',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=["pyFTracks"],
    keywords='geology thermochronology fission-tracks',
    install_requires=requirements,

)
