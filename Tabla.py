A='''- Si se declara una variable me da error? ()
- La instruccion collect es como si se declarara una nueva variable
- El me es el mismo para todos los robots de un bloque de instrucciones de robot o hay que diferenciarlo?
- Hay que diferenciar entre los me de los bloques anidados?
- Las variables que aparecen en collect pueden ser usadas en seccion de instrucciones de controlador?.
Si no es asi, entonces hay que crearle una tabla a cada seccion de 
- Como hacer para almacenar el me en la tabla pero que de error si aparece en la seccion de controlador? 
- 
'''
class Tabla:
	def __init__(self,exterior):
		self.tablaExterna = exterior
		self.tabla = {}
	def agregar(self,simbolo,valor,tipo):
		self.tabla[simbolo] = datos(valor,tipo)
	def obtener(self): # quiza no haga falta para esta entrega
		pass

class datos:
	def __init__(self,valor,tipo):
		self.valor = valor
		self.tipo = tipo
	def getValor(self):
		return self.valor
	def getTipo(self):
		return self.tipo

a = 3
b = 4

T=Tabla(None)
T.agregar('a',a,type(a))
print(T.tabla['a'].getTipo())
print(T.tabla['a'].getValor())
