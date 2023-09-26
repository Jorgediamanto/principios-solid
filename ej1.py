#comenzamos creando la clase matriz
class Matriz():
    def __init__(self, elementos: list):
        self.elementos = elementos

#a continuacion, creamos cada uno de los metodos en una clase separada, dado que se nos indica en el enunciado que cada metodo debe tener una unica responsabilidad

class Transpuesta(Matriz):
    def __init__(self, elementos: list):
        super().__init__(elementos)
    
    def transpuesta(self):
        return Matriz([[fila[i] for fila in self.elementos] for i in range(len(self.elementos[0]))])

class Imprimir(Matriz):
    def __init__(self, elementos: list):
        super().__init__(elementos)
    
    def imprimir(self):
        for fila in self.elementos:
            print(fila)

m = Imprimir([[1, 2], [3, 4]])
m.imprimir()

t = Transpuesta(m.elementos)
print(t.transpuesta().elementos)