#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup script"""

from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os import sep
from os import walk
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup

try:
    import Cython
    from Cython.Build import cythonize
except ImportError:
    Cython = None

if Cython:
    CYTHONIZED = cythonize([
        Extension(
            splitext(relpath(path, 'src').replace(sep, '.'))[0],
            sources=[path],
            include_dirs=[dirname(path)]
        )
        for root, _, _ in walk('src')
        for path in glob(join(root, '*.pyx' if Cython else '*.c'))
    ], compiler_directives={'embedsignature': True})
else:
    CYTHONIZED = None


def _read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='beluga',
    version='0.5.1',
    license='BSD 3-Clause License',
    description='Code infrastructure for deep learning to make modelling '
    + 'reproducible and maintainable',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges',
                   re.M | re.S).sub('', _read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', _read('CHANGELOG.rst'))
    ),
    author='Wolfgang Kopp',
    author_email='wolfgang.kopp@mdc-berlin.de',
    url='https://github.com/wkopp/beluga',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'beluga': ['resources/*.fa',
                             'resources/*.bed',
                             'resources/*.csv']},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    install_requires=[
        'numpy',
        'pandas',
        'Biopython',
        'pymongo',
        'keras',
        'htseq',
        'sklearn',
        'h5py',
        'pyBigWig'
    ],
    extras_require={
        "tf": ['tensorflow'],
        "tf_gpu": ['tensorflow-gpu'],
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        'cython',
    ] if Cython else [],
    entry_points={
        'console_scripts': [
            'beluga = beluga.cli:main',
        ]
    },
    ext_modules=CYTHONIZED,
)
