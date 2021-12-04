import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="wavinsentio",
    version="0.3.0",
    url="https://github.com/djerik/wavinsentio",
    license='MIT',

    author="Tobias Laursen",
    author_email="djerik@gmail.com",

    description="API Wrapper for Wavin Sentio underfloor heating system",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",

    packages=find_packages(exclude=('tests',)),

    install_requires=['requests'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
