from setuptools import setup, find_packages
from os.path import isfile
from os import exit

if not isfile('diethack/_cache/cache.py'):
    print 'Please build the cache first.'
    exit(1)

setup(
    name='diethack',
    version='0.0.0',
    description='Diet calculator for hackers.',
    url='http://www.diethack.org',
    author='Oleg Plakhotniuk',
    author_email='contact@diethack.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    keywords='diet calculator',
    packages=find_packages(exclude=['prepare.py', 'nndb'])
)
