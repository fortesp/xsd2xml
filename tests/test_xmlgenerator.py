import os
import unittest
import uuid

from xsd2xml import XmlGenerator
from xsd2xml import XmlValidator


class TestXmlGenerator(unittest.TestCase):

    def setUp(self) -> None:
        self.xsd_filename = 'tests/resources/pain.001.001.09.xsd'
        self.temp_filename = "tests/resources/." + str(uuid.uuid4())

    def testMandatoryFieldsOnly(self):
        xmlgenerator = XmlGenerator(self.xsd_filename, True)
        xmlgenerator.generate()

        xmlgenerator.write(self.temp_filename)
        validator = XmlValidator(self.xsd_filename)

        self.assertTrue(validator.validate(self.temp_filename))

    def testAllFields(self):
        xmlgenerator = XmlGenerator(self.xsd_filename, False)
        xmlgenerator.generate()

        xmlgenerator.write(self.temp_filename)
        validator = XmlValidator(self.xsd_filename)

        self.assertTrue(validator.validate(self.temp_filename))

    def tearDown(self) -> None:
        os.remove(self.temp_filename)


if __name__ == '__main__':
    unittest.main()
