'''
Created on 23 April 2020
@author: Sambit Giri
Setup script

The base code in this package is forked from https://github.com/sjforeman/bskit
'''

#from setuptools import setup, find_packages
from distutils.core import setup


setup(name='bskit',
      version='0.1',
      author='Sambit Giri',
      author_email='sambit.giri@astro.su.se',
      package_dir = {'bskit' : 'bskit'},
      packages=['bskit'],
      package_data={'share':['*'],},
      install_requires=['numpy','scipy','astropy', 'numba', 'mpi4py', 'nbodykit'],
      url="https://github.com/sjforeman/bskit"
      #include_package_data=True,
)
