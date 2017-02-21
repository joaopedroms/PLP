from dbtypes import *
from pgv import UMLDiagram


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

        testando o acesso do git