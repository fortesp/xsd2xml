import random
import rstr
import datetime
import xmlschema
import xml.etree.ElementTree as ET

from util.datagenerator import DataGenerator


class DataFacet:

    def __init__(self):
        self.datagenerator = DataGenerator()

    def string(self, node, nodetype):

        content = ""

        _facets_str = str(nodetype.facets)
        if "Length" in _facets_str:
            lo, up = 0, 0
            for k, facet in nodetype.facets.items():
                if "minLength" in k:
                    lo = facet.value
                elif "maxLength" in k:
                    up = facet.value
            content = self.datagenerator.get_mixed_string(random.randrange(lo, up))

        if "enumeration" in _facets_str:
            enumeration = list(nodetype.facets.values())[0].enumeration
            content = enumeration[random.randrange(0, len(enumeration))]

        if "pattern" in _facets_str:
            regexps = list(nodetype.facets.values())[0].regexps
            content = rstr.xeger(regexps[0]).upper()

        return content

    def boolean(self, node, nodetype):
        return True if (random.randrange(0, 1) == 1) else False

    def datetime(self, node, nodetype):
        return datetime.datetime.now().isoformat()

    def date(self, node, nodetype):
        return self.datetime(node, nodetype).split('T')[0]

    def time(self, node, nodetype):
        return self.datetime(node, nodetype).split('T')[1]

    def integer(self, node, nodetype):  # todo - complete this part
        return random.randrange(0, 10000)

    def float(self, node, nodetype):  # todo - complete this part
        return random.randrange(0, 1.0)

    def byte(self, node, nodetype):  # todo - complete this part
        return random.randrange(0, 8)

    def decimal(self, node, nodetype):
        digit_size, fraction_size = 0, 0
        # print(nodetype.facets)
        for k, facet in nodetype.facets.items():
            if not k is None:
                if "fractionDigits" in k:
                    fraction_size = facet.value
                elif "totalDigits" in k:
                    digit_size = facet.value
        # elif "assertion" in k:            #for xsd 1.1
        #    assertion = facet.path

        if fraction_size > 0:
            _content_part_2 = self.datagenerator.get_digits(2)
        else:
            _content_part_2 = "0"

        if digit_size > 0:
            if digit_size - fraction_size == 1:
                _content_part_1 = self.datagenerator.get_digits(random.randrange(1, 2))
            else:
                _content_part_1 = self.datagenerator.get_digits(random.randrange(1, digit_size - fraction_size))
        else:
            _content_part_1 = "0"

        return _content_part_1 + "." + _content_part_2

    def get_content(self, node, nodetype):

        datatype = nodetype.primitive_type.local_name.lower()
        method = getattr(self, datatype)

        return method(node, nodetype)


class XMLGenerator:

    def __init__(self, schema_file, mandatory_only=False, datafacet=None):
        self.schema = xmlschema.XMLSchema(schema_file)
        self.mandatory_only = mandatory_only
        self.datagenerator = DataGenerator()
        self.datafacet = datafacet
        self.ET = ET
        self.root = None

    def execute(self):

        for k, node in self.schema.elements.items():
            if self.mandatory_only and node.occurs[0] < 1: continue
            self.root = ET.Element(node.local_name, xmlns=self.schema.target_namespace)
            self._recur_build(node, self.root, True)

        return ET.tostring(self.root)

    def write(self, filename):

        if self.root is None:
            return

        tree = ET.ElementTree(self.root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

    # get generated content
    def _get_content(self, xsdnode, nodetype):
        if self.datafacet:
            return str(self.datafacet.get_content(xsdnode, nodetype))
        else:
            return ""

    def _recur_build(self, xsdnode, xmlnode, isroot=False):

        if self.mandatory_only and xsdnode.occurs[0] < 1: return

        if not isroot:
            xmlnode = ET.SubElement(xmlnode, xsdnode.local_name)

        # simple content
        if xsdnode.type.has_simple_content():
            if xsdnode.type.is_simple():
                xmlnode.text = self._get_content(xsdnode, xsdnode.type)
            else:
                xmlnode.text = self._get_content(xsdnode, xsdnode.type.content_type)

                # attributes
                if xsdnode.type.attributes:
                    for attr, attr_obj in xsdnode.type.attributes._attribute_group.items():
                        xmlnode.attrib[attr] = self._get_content(xsdnode, attr_obj.type)

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
