# -*- encoding: utf-8 -*-
import io
from glob import glob

from os.path import basename, dirname, join, splitext
from setuptools import find_packages, setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='dedrowse',
    license='GPLv2',
    version='0.1.0',
    description='Drowsiness monitor',
    long_description=read('README.md'),
    install_requires=[
        'click',
        'numpy',
        'scipy',
        'playsound',
        'imutils',
        'knobs',
        'attentive',
        'dlib'
    ],
    author='sthysel',
    author_email='sthysel@gmail.com',
    url='https://github.com/sthysel/dedrowse',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    package_data={
        'dedrowse': ['data/*.*'],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[],
    extras_require={},
    setup_requires=[],
    entry_points={
        'console_scripts': [
            'dedrowse=dedrowse.cli:cli',
        ]
    },
)
