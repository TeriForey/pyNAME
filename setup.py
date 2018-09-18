from setuptools import setup, find_packages
from glob import glob
from os.path import splitext, basename

setup(name='pyNAME',
      version='0.0.1',
      description='Runs NAME and plots results',
      long_description=open("README.md").read(),
      url='https://github.com/TeriForey/pyNAME',
      author='Teri Forey',
      author_email='trf5@le.ac.uk',
      license='LICENSE.txt',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
      include_package_data=True,
      scripts=['bin/pyNAME.py']
      )