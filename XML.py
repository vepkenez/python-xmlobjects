from lxml import etree

class XMLsimple(object):
    def __init__(self,element):
        self.data = element

    def __repr__(self):
        return self.data.text

    def set(self,value):
        self.data.text = value 


class XMLchild(object):
    def __init__(self,element):
        self.data = element

    def __getattr__(self,name):
        v = self.data.find(name)
        if v is not None:
            ch = v.getchildren()
            if len(ch):
                return XMLchild(v)
            return XMLsimple(v)
        return None

    def __repr__(self):
        return '<' + self.__class__.__name__ + ' "' + self.data.tag + ' - ['+','.join(self.attrs[:3])+']..." >'

    @property
    def attrs(self):
        return [c.tag for c in self.data.getchildren()]

class EasyXML(object):

    def __init__(self,filepath):
        self.file = open(filepath,'rw')
        self.doc = etree.parse(self.file)
        self.root = self.doc.getroot()

    def get_nodes_by_name(self,name):
        out = []
        for e in self.root.iter(name):
            out.append(XMLchild(e))
        return out


