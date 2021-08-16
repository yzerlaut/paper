from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='finalyz',
    version='1.0',
    description='FinalYZ - compiling scientific documents',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yzerlaut/finalyz',
    author='Yann Zerlaut',
    author_email='yann.zerlaut@gmail.com',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ],
    keywords='science pdflatex org-mode',
    packages=find_packages(),
    # package_data={'finalyz': ['templates/*', 'templates/*.txt', 'templates/slides/*.svg']},
    package_data={'': [path.join(here, 'templates', '*.txt'), path.join(here, 'templates',  'slides', '*.svg'),
                       path.join(here, 'templates',  'slides', 'pngs', '*.png')]},
    include_package_data=True    
)
