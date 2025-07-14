#  XSD2XML  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/xsd2xml
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xsd2xml",
    version="0.0.1",
    author="Monkey",
    author_email="somemail@emails.com",
    description="XSD to XML converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fortesp/xsd2xml",
    packages=setuptools.find_packages(),
    install_requires=['rstr'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
