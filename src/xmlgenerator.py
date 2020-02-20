import random
import rstr
import datetime
import xmlschema

from element import Element
from datagenerator import DataGenerator


class DataFacet:

    def __init__(self):
        self.datagenerator = DataGenerator()

    def string(self, nodetype):

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

    def boolean(self, nodetype):
        return True if (random.randrange(0, 1) == 1) else False

    def datetime(self, nodetype):
        return datetime.datetime.now().isoformat()

    def date(self, nodetype):
        return self.datetime(nodetype).split('T')[0]

    def time(self, nodetype):
        return self.datetime(nodetype).split('T')[1]

    def integer(self, nodetype):   # todo - complete this part
        return random.randrange(0, 10000)

    def decimal(self, nodetype):
        digit_size, fraction_size = 0, 0
        for k, facet in nodetype.facets.items():
            if "fractionDigits" in k:
                fraction_size = facet.value
            elif "totalDigits" in k:
                digit_size = facet.value

        if digit_size > 0:
            _content_part_1 = self.datagenerator.get_digits(random.randrange(1, digit_size))
        else:
            _content_part_1 = "0"

        if fraction_size > 0:
            _content_part_2 = self.datagenerator.get_digits(random.randrange(1, fraction_size))
        else:
            _content_part_2 = "0"

        return _content_part_1 + "." + _content_part_2

    def get_content(self, nodetype):

        content = ""
        datatype = nodetype.primitive_type.local_name.lower()

        f = getattr(self, datatype)

        return f(nodetype)


class XMLGenerator:

    def __init__(self, schema_file, mandatory_only=False, data_facet=None):
        self.schema = xmlschema.XMLSchema(schema_file)
        self.mandatory_only = mandatory_only
        self.datagenerator = DataGenerator()
        self.data_facet = data_facet
        # self.prettify = prettify

    def execute(self):
        # meta
        xml_str = str(Element("xml", {"version": "1.0", "encoding": "UTF-8"}, True))
        # if self.prettify: xml_str += "\n"

        # xml
        for k, node in self.schema.elements.items():
            if self.mandatory_only and node.occurs[0] < 1: continue
            xml_str += self._recur_build(node, True)

        return xml_str

    def _get_content(self, nodetype):
        if self.data_facet:
            return self.data_facet.get_content(nodetype)
        else:
            return ""


    def _recur_build(self, node, root=False):

        if self.mandatory_only and node.occurs[0] < 1: return ""

        element = Element(node.local_name, {}, False, True)

        if root and self.schema.target_namespace:
            element.attributes['xmlns'] = self.schema.target_namespace

        # simple content
        if node.type.has_simple_content():
            if node.type.is_simple():
                element.content = self._get_content(node.type)
            else:
                element.content = self._get_content(node.type.content_type)

                # attributes
                if node.type.attributes:
                    for attr, attr_obj in node.type.attributes._attribute_group.items():
                        element.attributes[attr] = self._get_content(attr_obj.type)

        # complex types
        else:
            content_type = node.type.content_type
            # choice
            if content_type.model == "choice":
                subnode = content_type._group[0]
                element.content += self._recur_build(subnode)
            # sequence
            else:
                for subnode in content_type._group:
                    if not hasattr(subnode, 'process_contents'):  # EXCEPT ANY, e.g. lax, etc.
                        element.content += self._recur_build(subnode)

        # _new_line = "\n" if self.prettify else ""
        return str(element)
