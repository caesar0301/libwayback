import os
import sys
from setuptools import setup
from libwayback import __version__

setup(
    name = "libwayback",
    version = __version__,
    url = 'https://github.com/caesar0301/libwayback',
    author = 'Jamin Chen',
    author_email = 'chenxm35@gmail.com',
    description = 'A library to parse Wayback Machine of archive.org to get a historical views of web pages.',
    long_description='''A library to parse Wayback Machine of archive.org to get a historical views of web pages. It is a useful tool to research on the evolution of web pages, page structure analysis, and among other interesting topics.''',
    license = "LICENSE",
    packages = ['libwayback'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: Freely Distributable',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
   ],
)
