from xmlgenerator import XMLGenerator, DataFacet

if __name__ == "__main__":

    xmlgenerator = XMLGenerator('resources/pain.001.001.09.xsd', None, DataFacet())
    print(xmlgenerator.execute())

