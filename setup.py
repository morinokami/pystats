from setuptools import setup, find_packages

setup(
    name='pystats',
    version='0.0.1',
    license='MIT',
    url='https://github.com/morinokami/pystats',
    description='',
    long_description = '',

    author='Shinya Fujino',
    author_email='shf0811@gmail.com',

    packages=find_packages(exclude=('tests')),
    package_data={'pystats': ['data/languages.yml']},
    include_package_data=True,

    install_requires=['requests', 'pyyaml'],
)