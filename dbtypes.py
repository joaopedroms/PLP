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