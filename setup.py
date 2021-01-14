import sys
import re
import ast
from setuptools import setup

readme_markdown = None
with open("README.md") as f:
    readme_markdown = f.read()

setup(
    name="tqwgp-parser",
    version="0.0.2",
    url="https://github.com/YtoTech/talk-quote-work-getpaid-parser",
    license="AGPL-3.0",
    author="Yoan Tournade",
    author_email="y@yoantournade.com",
    description="A library for parsing Talk Quote Work Get-Paid (TQWGP) text-based compliant sales and accounting documents.",
    long_description=readme_markdown,
    long_description_content_type="text/markdown",
    packages=["tqwgp-parser"],
    include_package_data=True,
    zip_safe=True,
    platforms="any",
    install_requires=["hy"],
)
