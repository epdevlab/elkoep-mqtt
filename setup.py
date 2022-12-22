"""Setup script for inels-mqtt package."""
from setuptools import setup, find_packages

setup(
    name="inels-mqtt-new",
    version="0.0.35",
    url="https://github.com/zed4805/inels-mqtt-new",
    license="MIT",
    author="Elko EP s.r.o.",
    author_email="zed4805@gmail.com",
    description="Python library for iNels mqtt protocol",
    keywords=["iNels", "Elko EP", "Home assistant integration"],
    long_description_content_type="text/markdown",
    charset="UTF-8",
    variant="GFM",
    long_description=open("README.md").read(),
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    test_suite="unittest",
)
