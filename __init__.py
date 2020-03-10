from .xmlgenerator import XMLGenerator, DataFacet

if __name__ == "__main__":

    xmlgenerator = XMLGenerator('../swift/resources/schema/pain.001.001.09.alt.xsd', None, DataFacet())
    print(xmlgenerator.execute())

