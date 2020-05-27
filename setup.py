from setuptools import setup

setup(
    name="dicom_art",
    version="0.1.0",
    packages=["dicom_art"],
    install_requires=[
        "dicom_utils",
        "numpy",
        "matplotlib",
    ],
)
