from setuptools import find_packages, setup

setup(
    name='objtojson',
    packages=find_packages(include=['objtojson']),
    version='0.1.0',
    description='Object to JSON serialization with none to minimal need for custom declarations',
    author='Joerg Schroeter',
    license='MIT',
    tests_require=['pytest']
)
