
class Element:

    def __init__(self, name, attr={}, header=False, selfclosing=False):
        self.name = name
        self.attributes = attr
        self.content = ""
        self.header = header
        self.selfclosing = selfclosing

    def _get_attributes(self):
        if self.attributes:
            attr_str = ""
            for k, v in self.attributes.items():
                attr_str += " %s='%s'" % (k, v)
            return attr_str
        else:
            return ""

    def __str__(self):
        if self.header:
            return "<?%s%s?>" % (self.name, self._get_attributes())
        else:
            if self.content or not self.selfclosing:
                return "<%s%s>%s</%s>" % (self.name, self._get_attributes(), self.content, self.name)
            else:
                return "<%s%s/>" % (self.name, self._get_attributes())
