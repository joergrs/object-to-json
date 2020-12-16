from setuptools import find_packages, setup

from objtojson import __version__

setup(
    name='objtojson',
    packages=find_packages(include=['objtojson']),
    version=__version__,
    description='Object to JSON serialization with none to minimal need for custom declarations',
    author='Joerg Schroeter',
    license='MIT',
    tests_require=['pytest']
)
