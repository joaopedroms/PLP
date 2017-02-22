from dbmodel import *


class Primaria(Table):
    atributo1 = Char(20)
    atributo2 = String()

    def metodo(self, param1, param2):
        pass


class Secundaria(Primaria):
    atributo3 = Boolean()

    def metodo(self):
        pass


class Terciaria(Table):
    atributo4 = Primaria()
    atributo5 = Vector(Secundaria, min=3)

    def metodo2(self, param1):
        pass

    def metodo3(self, param1, param2, param3, param4):
        pass


class Aleatoria(Table):
    atributo10 = String()

    def metodo(self):
        pass


class Filha(Aleatoria, Terciaria):
    atributo11 = List(Terciaria, min=0)
    atributo12 = Char(20)

    def metodo(self):
        pass

class Filha2(Filha, Aleatoria):
    atributo13 = Char(10)
    atributo14 = String()

    def metodo(self, param):
        pass


Table.modelo(show_roles=True)
