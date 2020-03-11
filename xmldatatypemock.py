import datetime
import random
import rstr

from lib.xsd2xml.helper import get_mixed_string, get_digits


class XmlDataTypeMock:

    def __init__(self):
        pass

    def string(self, nodetype):

        content = get_mixed_string(10)

        _facets_str = str(nodetype.facets)
        if "Length" in _facets_str:
            lo, up = 0, 0
            for k, facet in nodetype.facets.items():
                if "minLength" in k:
                    lo = facet.value
                elif "maxLength" in k:
                    up = facet.value
            content = get_mixed_string(random.randrange(lo, up))

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

    def integer(self, nodetype):  # todo - complete this part
        return random.randrange(0, 10000)

    def float(self, nodetype):  # todo - complete this part
        return random.randrange(0, 1.0)

    def byte(self, nodetype):  # todo - complete this part
        return random.randrange(0, 8)

    def decimal(self, nodetype):
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
            _content_part_2 = get_digits(2)
        else:
            _content_part_2 = "0"

        if digit_size > 0:
            if digit_size - fraction_size == 1:
                _content_part_1 = get_digits(random.randrange(1, 2))
            else:
                _content_part_1 = get_digits(random.randrange(1, digit_size - fraction_size))
        else:
            _content_part_1 = "0"

        return _content_part_1 + "." + _content_part_2
