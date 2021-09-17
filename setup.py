import setuptools
import os

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotszoo",
    version="0.1",
    author="Federico A. Galatolo",
    author_email="federico.galatolo@ing.unipi.it",
    description="Collection of utilities to make plots",
    url="https://github.com/galatolofederico/plotszoo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy==1.19.4",
        "pandas==1.1.4",
        "scipy==1.5.4",
        "matplotlib==3.3.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
        "Intended Audience :: Science/Research",
        "Development Status :: 4 - Beta"
    ],
)