from dbmodel import *

class Primaria(Table):
    atrib1 =  Char(10)
    atrib2 = Integer()
    atrib3 = Float()
    #attib5 = Vector(Table, min=3)
    def metodo1(self, arg):
        pass

class Secundaria(Primaria):
    atrib4 =  Char(30)
    atrib5 = Integer()
    attib5 = Vector(Primaria, min=1)
    def metodo2(subclass, arg2):
        pass

class Terciaria(Secundaria):
    atrib7 = String()
    attib5 = Vector(Primaria, min=1)
    def metodo3(self, arg1, arg4, arg3):
        pass

Table.show_model(show_roles=True)
