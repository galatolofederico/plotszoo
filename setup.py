import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wandb-plots",
    version="0.1.0",
    author="Federico A. Galatolo",
    author_email="federico.galatolo@ing.unipi.it",
    description="Utilities to make plots using wandb",
    url="https://github.com/galatolofederico/wandb-plots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "wandb==0.10.8",
        "numpy==1.19.4",
        "pandas==1.1.4",
        "scipy==1.5.4",
        "matplotlib==3.3.2",
        "requests==2.24.0"
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