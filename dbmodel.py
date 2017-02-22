import pygraphviz as pgv
from PIL import Image


class UMLDiagram:
    def __init__(self):
        self.Graph = pgv.AGraph(strict=False, directed=True)
        self.Graph.node_attr['shape'] = 'record'
        self.Graph.node_attr['fillcolor'] = '#fdffd8'
        self.Graph.node_attr['style'] = 'filled'
        self.Graph.node_attr['fontname'] = 'calibri'

    def addClass(self, name, attrs, methods):
        line_break = '|'
        align_left = '\l'

        node_def = '{' + name + line_break

        for attr in attrs:
            node_def += attr + align_left

        node_def += line_break

        for method in methods:
            node_def += method + align_left

        node_def += '}'

        self.Graph.add_node(name, label=node_def)

    def display(self):
        self.Graph.layout(prog='dot')
        self.Graph.draw('UMLDiagram.png')
        print self.Graph
        img = Image.open('UMLDiagram.png')
        img.show()

    def addRelationship(self, from_, to, card):
        self.Graph.add_edge(from_, to, color='#0000ff', label=card)

    def addExtension(self, extends, extended):
        self.Graph.add_edge(extends, extended, color='#ff0000')


class Coluna(object):
    def __init__(self, unique=False):
        self.unique = unique

    def getStrRep(self):
        return self.__class__.__name__

    def properties(self):
        pass

class Char(Coluna):
    def __init__(self, limit=1, unique=False):
        Coluna.__init__(self, unique)
        self.limit = limit

    def properties(self):
        uniqueness = ' UNIQUE ' if self.unique else ''
        return 'char(' + str(self.limit) + ')' + uniqueness

    def getStrRep(self):
        return 'Char(%d)' % self.limit

class Boolean(Coluna):
    def __init__(self, unique=False):
        Coluna.__init__(self, unique)

class String(Coluna):
    def __init__(self, unique=False):
        Coluna.__init__(self, unique)

class Integer(Coluna):
    def __init__(self, unique=False):
        Coluna.__init__(self, unique)

class Float(Coluna):
    def __init__(self, unique=False):
        Coluna.__init__(self, unique)

class DateTime(Coluna):
    def __init__(self, unique=False):
        Coluna.__init__(self, unique)

class Date(Coluna):
    def __init__(self, unique=False):
        Coluna.__init__(self, unique)

class List(Coluna):
    def __init__(self, collection_type, min, unique=False):
        self.collection_type = collection_type.__name__
        self.min = min
        Coluna.__init__(self, unique)

    def getStrRep(self):
        return "List(" + self.collection_type + ")"

class Enum(List):
    def __init__(self, collection_type, min=0, unique=False):
        List.__init__(self, collection_type, min, unique)

    def getStrRep(self):
        return "Enum(" + self.collection_type + ")"

class Vector(List):
    def __init__(self, collection_type, min=0, unique=False):
        List.__init__(self, collection_type, min, unique)

    def getStrRep(self):
        return "Vector(" + self.collection_type + ")"


class Meta(type):
    def __new__(self, nclass, base, dct):
        if nclass != 'Table':
            if '__init__' in dct:
                raise TypeError, '__init__ nao pode ser definido'

            def sqlinit(self, **kws):
                pass

            dct['__init__'] = sqlinit

        return type.__new__(self, nclass, base, dct)

    def __init__(cls, nclass, base, dct):
        if nclass != 'Table':
            Table.__filhas__[nclass] = cls
        return type.__init__(cls, nclass, base, dct)


class Table(object):
    __metaclass__ = Meta
    __filhas__ = {}

    def getStrRep(self):
        return self.__class__.__name__

    @staticmethod
    def show_model(show_roles=False):
        myDiagram = UMLDiagram()

        for t in Table.__filhas__:
            bases = [c.__name__ for c in Table.__filhas__[t].__bases__ if c.__name__ != 'Table']

            if len(bases) > 0:
                print 'Table', t, 'descende de:', ', '.join(bases)
            else:
                print 'Table', t

            dct = Table.__filhas__[t].__dict__

            atrs = [a for a in dct if isinstance(dct[a], Coluna) or isinstance(dct[a], Table)]

            for a in atrs:
                if isinstance(dct[a], List):
                    myDiagram.addRelationship(t, dct[a].collection_type, str(dct[a].min) + '..*')
                if dct[a].__class__.__name__ in Table.__filhas__.keys():
                    if show_roles:
                        myDiagram.addRelationship(t, dct[a].__class__.__name__, '1\n' + a)
                    else:
                        myDiagram.addRelationship(t, dct[a].__class__.__name__, '1\n')

            atr_str_lst = ['+ ' + a + ': ' + dct[a].getStrRep() for a in atrs]

            meth = [m for m in dct if callable(dct[m]) and m != '__init__']

            meth_str_lst = []

            for m in meth:
                args = ', '.join([arg for arg in dct[m].__code__.co_varnames if arg != 'self'])
                meth_str_lst.append('+ ' + m + '(' + args + ')')

            for t2 in Table.__filhas__:
                if t != t2:
                    if issubclass(Table.__filhas__[t], Table.__filhas__[t2]):
                        myDiagram.addExtension(t, t2)

            myDiagram.addClass(t, atr_str_lst, meth_str_lst)

        myDiagram.display()
