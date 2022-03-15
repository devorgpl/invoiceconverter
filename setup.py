from setuptools import find_packages, setup

setup(
    name='invoiceconverterlib',
    packages=find_packages(),
    version='0.1.2',
    description='Invoice converter library',
    author='Cyprian Śniegota',
    license='Apache Licence 2.0',
    install_requires=['openpyxl~=3.0.5'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest == 4.4.1'],
    test_suite='tests',
)
