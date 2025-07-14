"""Setup script for elkoep-mqtt package."""

from setuptools import find_packages, setup

setup(
    name="elkoep-mqtt",
    version="0.2.33.beta.30",
    url="https://github.com/epdevlab/elkoep-mqtt",
    license="MIT",
    author="Elko EP s.r.o.",
    author_email="epdevlab@gmail.com",
    description="Python library for iNELS mqtt protocol",
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
