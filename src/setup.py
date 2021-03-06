from setuptools import setup
from os.path import isfile, join, dirname
from diethack._storage import rebuildCache
import logging

if not isfile(join(dirname(__file__), 'diethack/_cache/chunks.py')):
    logging.basicConfig(format='%(levelname)-8s %(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.INFO)
    rebuildCache()

setup(
    name='diethack',
    version='1.0.0',
    description='Diet problem solver with Dietary Reference Intakes in mind.',
    url='http://www.diethack.org',
    author='Oleg Plakhotniuk',
    author_email='contact@diethack.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='diet problem solver dri',
    packages=['diethack', 'diethack._cache']
)
