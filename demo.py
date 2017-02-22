from dbmodel import *


class myClass(Table):
    attr1 = Char(20)
    attr2 = String()

    def method(self, arg1, arg2):
        pass


class subclass(myClass):
    attr3 = Boolean()

    def method(self):
        pass


class anotherClass(Table):
    attr4 = myClass()
    attr5 = Vector(subclass, min=3)

    def method2(self, param1):
        pass

    def method3(self, param1, param2, param3):
        pass


class lonelyClass(Table):
    attr10 = String()

    def method(self):
        pass


class thirdClass(Table):
    attr6 = Integer()
    attr7 = Float()
    attr8 = Date()
    attr9 = DateTime()
    lst = Enum(anotherClass)
    lst2 = List(lonelyClass, min=2)

    def method(self, param1, param2):
        pass

    def voidMethod(self):
        pass


class childOfLonelyAndThird(lonelyClass, thirdClass):
    attr11 = List(anotherClass, min=0)
    attr12 = Char(20)

    def method(self):
        pass


Table.show_model(show_roles=True)