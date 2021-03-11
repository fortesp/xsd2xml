#  XSD2XML  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/xsd2xml
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.
import datetime
import random
import rstr

from xsd2xml.helper import get_mixed_string, get_digits
from abc import ABC, abstractmethod


class DataFacet(ABC):
    @abstractmethod
    def string(self, nodetype):
        pass

    @abstractmethod
    def boolean(self, nodetype):
        pass

    @abstractmethod
    def datetime(self, nodetype):
        pass

    @abstractmethod
    def date(self, nodetype):
        pass

    @abstractmethod
    def time(self, nodetype):
        pass

    @abstractmethod
    def integer(self, nodetype):
        pass

    @abstractmethod
    def float(self, nodetype):
        pass

    @abstractmethod
    def byte(self, nodetype):
        pass

    @abstractmethod
    def decimal(self, nodetype):
        pass


# Class used by the XmlGenerator
# For each data type it outputs specific randomized data
class XmlDefaultDataFacet(DataFacet):

    def string(self, nodetype):

        _facets_str = str(nodetype.facets)
        if "Length" in _facets_str:
            lo, up = 0, 0
            for k, facet in nodetype.facets.items():
                if "minLength" in k:
                    lo = facet.value
                elif "maxLength" in k:
                    up = facet.value

            s = get_mixed_string(random.randrange(lo, up))
            return s

        if "enumeration" in _facets_str:
            enumeration = list(nodetype.facets.values())[0].enumeration
            return enumeration[random.randrange(0, len(enumeration))]

        if "pattern" in _facets_str:
            regexps = list(nodetype.facets.values())[0].regexps
            return rstr.xeger(regexps[0])

        return get_mixed_string(10)

    def boolean(self, nodetype) -> int:
        return random.randrange(0, 1)  # true / false

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
