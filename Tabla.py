A='''- Si se declara una variable me da error? ()
- La instruccion collect es como si se declarara una nueva variable
- El me es el mismo para todos los robots de un bloque de instrucciones de robot o hay que diferenciarlo?
- Hay que diferenciar entre los me de los bloques anidados?
- Las variables que aparecen en collect pueden ser usadas en seccion de instrucciones de controlador?.
Si no es asi, entonces hay que crearle una tabla a cada seccion de 
- Como hacer para almacenar el me en la tabla pero que de error si aparece en la seccion de controlador? 
'''

class Tabla:
	def __init__(self,exterior):
		self.tablaExterna = exterior
		self.tabla = {}
		self.hijos = [] # Quiza no haga falta
	def buscarAqui(self,simbolo):
		if simbolo in self.tabla:
			return True
		else:
			return False
	def agregar(self,simbolo,valor,tipo):
		self.tabla[simbolo] = datos(valor,tipo,True) # El True es de datos.declarada (quiza no hace falta)
	def buscarEnTodos(self,simbolo,opcion): # Opcion para saber si se quiere buscar el tipo/valor de un elemento
		if self.buscarAqui(simbolo):				# de la tabla o si se quiere saber si esta o no declarada
			if opcion == 'buscar':
				return True
			elif opcion == 'getTipo':
				return self.tabla[simbolo].tipo
			elif opcion == 'getValor':
				return self.tabla[simbolo].valor
		else:
			if self.tablaExterna:
				return self.tablaExterna.buscarEnTodos(simbolo,opcion)
			else:
				if opcion == 'buscar': # Si llega arriba y no lo encontro
					return False
				else:
					return None
	def tipoRobot(self):
		for simbolo,datos in self.tabla.items(): 
			if datos.robot: 			# Si no es none el atributo robot, entonces se esta en una tabla 
				return datos.tipo		# de inst de robot
										# Se esta ciclando en el diccionario y despues se esta buscando
										# en cada iteracion un elemento (O(n^2)). Cambiar si da tiempo
										# sacando for item()




class datos:
	def __init__(self,valor,tipo,declarada):
		self.valor = valor
		self.tipo = tipo
		self.declarada = False # Para ahorrar tiempo y no buscar una variable en todas las tablas
		self.robot = None
	def getValor(self):
		return self.valor
	def getTipo(self):
		return self.tipo

T = Tabla(None)
T2 = Tabla(T)
T3 = Tabla(T2)
T.agregar('a',2,'int')
T.agregar('b',3,'float')
T.agregar('c',5,'long')
T2.agregar('d',2,'longlong')
T2.agregar('e',3,'longint')
T2.agregar('f',5,'int')
T3.agregar('g',2,'int')
T3.agregar('h',3,'int')
T3.agregar('i',5,'int')
print(T.buscarAqui('a'))
print(T3.buscarEnTodos('a','getTipo'))