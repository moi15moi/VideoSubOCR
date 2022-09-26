import os
import re
import setuptools

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = [\'\"](.+)[\'\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="VideoSubOCR",
    url="https://github.com/moi15moi/VideoSubOCR/",
    project_urls={
        "Source": "https://github.com/moi15moi/VideoSubOCR/",
        "Tracker": "https://github.com/moi15moi/VideoSubOCR/issues/",
    },
    author="moi15moi",
    author_email="moi15moismokerlolilol@gmail.com",
    description="VideoSubFinder automation.",
    long_description_content_type="text/markdown",
    version=find_version("src", "__init__.py"),
    python_requires=">=3.7",
    py_modules=["src"],
    install_requires=[
        "Pillow",
        "pysubs2",
        "pytesseract",
        "rich",
    ],
    entry_points={"console_scripts": ["VideoSubOCR=src.__main__:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    license="GNU LGPL 3.0 or later",
)
