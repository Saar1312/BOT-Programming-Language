class Tabla:
	def __init__(self,exterior):
		self.tablaExterna = exterior
		self.tabla = {}
	def agregar(self,simbolo,valor,tipo,tabla=None):
		self.tabla[simbolo] = datos(valor,tipo,tabla) # El True es de datos.declarada (quiza no hace falta)
	def agregarTablaRobot(self,simbolo,tabla): # Para agregar 
		self.robot[simbolo] = tabla
	def buscarAqui(self,simbolo):
		if simbolo in self.tabla:
			return True
		else:
			return False
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
	def __init__(self,valor,tipo,tabla):
		self.valor = valor
		self.tipo = tipo
		#self.declarada = False # Para ahorrar tiempo y no buscar una variable en todas las tablas
		#self.robot = None
		#self.tabla = tabla
	def getValor(self):
		return self.valor
	def getTipo(self):
		return self.tipo
