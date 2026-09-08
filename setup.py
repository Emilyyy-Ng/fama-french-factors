from setuptools import setup, find_packages

setup(
    name="fama-french-factors",
    version="1.0.0",
    author="Emily Ng",
    description="Download Fama-French factor data from Ken French's data library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Emilyyy-Ng/fama-french-factors",
    py_modules=["fama_french"],  # Single file module
    install_requires=[
        "pandas>=1.0.0",
        "pandas-datareader>=0.10.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)