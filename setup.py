from distutils.core import setup

with open('requirements.txt', 'r') as f:
    packages = [i.strip() for i in f.readlines()]

setup(name='riffusion',
      version='0.1',
      packages=['riffusion'],
      install_requires=packages
     )