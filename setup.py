"""Python setup.py for unmanned_aircraft_project package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("unmanned_aircraft_project", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="unmanned_aircraft_project",
    version=read("unmanned_aircraft_project", "VERSION"),
    description="NLP and SPARQL conversion for the unmanned aircraft project",
    url="https://github.com/Hylobate/unmanned-aircraft-project/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Hylobate",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["unmanned_aircraft_project = unmanned_aircraft_project.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
