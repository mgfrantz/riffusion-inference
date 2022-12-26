from distutils.core import setup

with open('requirements.txt', 'r') as f:
    packages = [i.strip() for i in f.readlines()]

setup(name='riffusion',
      version='0.1',
      description='Python Distribution Utilities',
      author='Greg Ward',
      author_email='gward@python.net',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['riffusion'],
      install_requires=packages
     )