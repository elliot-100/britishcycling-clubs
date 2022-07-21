"""A setuptools based setup module.

Based on https://github.com/pypa/sampleproject/blob/main/setup.py
"""

import pathlib

# Always prefer setuptools over distutils
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="britishcycling-clubs",
    version="0.0.2",
    description="Unofficial library to automate aspects of British/Scottish/Welsh Cycling's club Membership Manager system",
    long_description_content_type="text/markdown",
    url="https://https://github.com/elliot-100/britishcycling-clubs",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.7, <4",
    install_requires=["selenium<4.3.0"],
)
