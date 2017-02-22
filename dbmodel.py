import pygraphviz as pgv
from PIL import Image

class UML:
    def __init__(self):
        self.Graph = pgv.AGraph(strict=False, directed=True)
        self.Graph.node_attr['shape'] = 'record'
        self.Graph.node_attr['fillcolor'] = '#fdffd8'
        self.Graph.node_attr['style'] = 'filled'
        self.Graph.node_attr['fontname'] = 'calibri'

    def novaClasse(self, nome, atributos, metodos):
        node_def = '{' + nome + '|'

        for atributo in atributos:
            node_def += atributo + '\l'

        node_def += '|'

        for metodo in metodos:
            node_def += metodo + '\l'

        node_def += '}'

        self.Graph.add_node(nome, label=node_def)

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
    def modelo(show_roles=False):
        diagrama = UML()

        for t in Table.__filhas__:
            bases = [c.__name__ for c in Table.__filhas__[t].__bases__ if c.__name__ != 'Table']

            if len(bases) > 0:
                print 'Table', t, 'descende de:', ', '.join(bases)
            else:
                print 'Table', t

            dct = Table.__filhas__[t].__dict__

            atribs = [a for a in dct if isinstance(dct[a], Coluna) or isinstance(dct[a], Table)]

            for a in atribs:
                if isinstance(dct[a], List):
                    diagrama.Graph.add_edge(t, dct[a].collection_type, color='#0000ff', label=str(dct[a].min) + '..*')
                if dct[a].__class__.__name__ in Table.__filhas__.keys():
                    if show_roles:
                        diagrama.Graph.add_edge(t, dct[a].__class__.__name__, color='#0000ff', label='1\n' + a)
                    else:
                        diagrama.Graph.add_edge(t, dct[a].__class__.__name__, color='#0000ff', label='1\n')
            atribsLst = ['+ ' + a + ': ' + dct[a].getStrRep() for a in atribs]

            meth = [m for m in dct if callable(dct[m]) and m != '__init__']

            methLst = []

            for m in meth:
                args = ', '.join([arg for arg in dct[m].__code__.co_varnames if arg != 'self'])
                methLst.append('+ ' + m + '(' + args + ')')

            for t2 in Table.__filhas__:
                if t != t2:
                    if issubclass(Table.__filhas__[t], Table.__filhas__[t2]):
                        diagrama.Graph.add_edge(t, t2, color='#ff0000')

            diagrama.novaClasse(t, atribsLst, methLst)

        diagrama.Graph.layout(prog='dot')
        diagrama.Graph.draw('diagrama.png')
        print diagrama.Graph
        img = Image.open('diagrama.png')
        img.show()
