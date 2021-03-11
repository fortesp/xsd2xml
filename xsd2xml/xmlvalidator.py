#  XSD2XML  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/xsd2xml
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.
from lxml import etree


class XmlValidator:

    def __init__(self, xsd_path: str):
        xmlschema_doc = etree.parse(xsd_path)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def validate(self, et: etree) -> bool:
        return self.xmlschema.validate(et)

    def validate(self, xml_path: str) -> bool:
        xml_doc = etree.parse(xml_path)
        return self.xmlschema.validate(xml_doc)
