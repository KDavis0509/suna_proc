try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md") as readme_file:
    readme = readme_file.read()


with open("LICENSE") as license_file:
    license = license_file.read()

setup(name='suna_process',
      description='Python package to process Satlantic SUNA v2 data files',
      author='John Franco Saraceno',
      author_email='saraceno@usgs.gov',
      url='https://bitbucket.org/geofranco/suna_process',
      version='1.0',
      packages=[suna_process],
      install_requires=['datetime', 'glob', 'matplotlib', 'numpy',
						'pandas', 'statsmodels'],
      license=license,
      )
