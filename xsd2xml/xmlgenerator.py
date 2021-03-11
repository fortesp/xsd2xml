#  XSD2XML  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/xsd2xml
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.
import xmlschema
import xml.etree.ElementTree as ET

from xsd2xml.xmldatafacet import XmlDefaultDataFacet


class XmlGenerator:
    """
      ``XmlGenerator(schema_file, mandatory_only=False, xmldatafacet=None)``

                - ``schema_file`` - Path to the XSD
                - ``mandatory_only`` - Generate all the fields or just the mandatory ones (minOccurs > 0)
                - ``xmldatafacet`` - Data facet class. If not provided, the default will be used.
      """

    def __init__(self, schema_file, mandatory_only=False, xmldatafacet=None):
        self.schema = xmlschema.XMLSchema(schema_file)
        self.mandatory_only = mandatory_only
        if xmldatafacet is None:
            self.xmldatafacet = XmlDefaultDataFacet()
        else:
            self.xmldatafacet = xmldatafacet

        self.ET = ET
        self.root = None

    def generate(self) -> str:
        for node in self.schema.root_elements:
            if self.mandatory_only and node.occurs[0] < 1: continue
            self.root = ET.Element(node.local_name, xmlns=self.schema.target_namespace)
            self._recur_build(node, self.root, True)

        return ET.tostring(self.root)

    def write(self, filename) -> None:

        if self.root is None:
            return

        tree = ET.ElementTree(self.root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

    def _recur_build(self, xsdnode, xmlnode, isroot=False) -> None:

        # skip if only mandatory fields
        if self.mandatory_only and xsdnode.occurs[0] < 1: return

        if not isroot:
            xmlnode = ET.SubElement(xmlnode, xsdnode.local_name)

        # simple content
        if xsdnode.type.has_simple_content():
            if xsdnode.type.is_simple():
                xmlnode.text = self._get_random_content(xsdnode.type)
            else:
                xmlnode.text = self._get_random_content(xsdnode.type.content_type)

        # complex types
        else:
            content_type = xsdnode.type.content_type
            # choice
            if content_type.model == "choice":
                selected_node = content_type._group[0]

                # find mandatory element in group
                if self.mandatory_only:
                    for subnode in content_type._group:
                        if subnode.occurs[0] < 1:
                            continue
                        else:
                            selected_node = subnode

                self._recur_build(selected_node, xmlnode)
            else:
                # sequence
                for subnode in content_type._group:
                    if not hasattr(subnode, 'process_contents'):  # xs:element
                        if hasattr(subnode, '_group'):
                            subnode = subnode._group[0]
                        self._recur_build(subnode, xmlnode)
                    else:  # xs:any
                        subnode = ET.SubElement(xmlnode, 'Any')  # any - close with any tag

        # attributes
        _attributes = dict
        if hasattr(xsdnode, "attributes"):
            _attributes = xsdnode.attributes
        else:
            if hasattr(xsdnode.type, "attributes"):
                attributes = xsdnode.type.attributes
        for attr, attr_obj in _attributes.items():
            xmlnode.attrib[attr] = self._get_random_content(attr_obj.type)

    def _get_random_content(self, nodetype) -> str:
        if self.xmldatafacet:
            datatype = nodetype.primitive_type.local_name.lower()
            call_method = getattr(self.xmldatafacet, datatype)
            return str(call_method(nodetype))
        else:
            return ""
