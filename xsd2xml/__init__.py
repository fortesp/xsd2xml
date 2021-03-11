#  XSD2XML  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/xsd2xml
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.
from xsd2xml.xmlgenerator import XmlGenerator
from xsd2xml.xmlvalidator import XmlValidator
from xsd2xml.xmldatafacet import XmlDefaultDataFacet
import sys

if __name__ == "__main__":

    xsd = sys.argv[1]
    mandatory = True
    xmlfile = None

    if 2 in sys.argv:
        mandatory = bool(sys.argv[2])

    if 3 in sys.argv:
        xmlfile = sys.argv[3]

    xmlgenerator = XmlGenerator(xsd, mandatory)
    xml = xmlgenerator.generate()

    if xmlfile:
        xmlgenerator.write(xmlfile)
    else:
        print(xml)
