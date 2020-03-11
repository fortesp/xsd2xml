import xmlschema
import xml.etree.ElementTree as ET


class XMLGenerator:

    def __init__(self, schema_file, mandatory_only=False, xmldatatypemock=None):
        self.schema = xmlschema.XMLSchema(schema_file)
        self.mandatory_only = mandatory_only
        self.xmldatatypemock = xmldatatypemock
        self.ET = ET
        self.root = None

    def execute(self):
        for node in self.schema.root_elements:
            if self.mandatory_only and node.occurs[0] < 1: continue
            self.root = ET.Element(node.local_name, xmlns=self.schema.target_namespace)
            self._recur_build(node, self.root, True)

        return ET.tostring(self.root)

    def write(self, filename):

        if self.root is None:
            return

        tree = ET.ElementTree(self.root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

    def _get_mocked_content(self, nodetype):
        if self.xmldatatypemock:
            datatype = nodetype.primitive_type.local_name.lower()
            method = getattr(self.xmldatatypemock, datatype)
            return str(method(nodetype))
        else:
            return ""

    def _recur_build(self, xsdnode, xmlnode, isroot=False):

        if self.mandatory_only and xsdnode.occurs[0] < 1: return

        if not isroot:
            xmlnode = ET.SubElement(xmlnode, xsdnode.local_name)

        # simple content
        if xsdnode.type.has_simple_content():
            if xsdnode.type.is_simple():
                xmlnode.text = self._get_mocked_content(xsdnode.type)
            else:
                xmlnode.text = self._get_mocked_content(xsdnode.type.content_type)

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
                    if not hasattr(subnode, 'process_contents'):  # EXCEPT ANY, e.g. lax, etc. maybe todo
                        if hasattr(subnode, '_group'):
                            subnode = subnode._group[0]
                        self._recur_build(subnode, xmlnode)

        # attributes
        _attributes = dict
        if hasattr(xsdnode, "attributes"):
            _attributes = xsdnode.attributes
        else:
            if hasattr(xsdnode.type, "attributes"):
                attributes = xsdnode.type.attributes
        for attr, attr_obj in _attributes.items():
            xmlnode.attrib[attr] = self._get_mocked_content(attr_obj.type)
