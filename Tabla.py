#-------------------------------------------------------------------------------
#							    TABLA
#-------------------------------------------------------------------------------
class Tabla:
	def __init__(self,exterior):
		self.tablaExterna = exterior
		self.tabla = {}
	#---------------------------------------------------------------------------
	# agregar()
	#
	# anade un simbolo a la tabla de simbolos
	#---------------------------------------------------------------------------	
	def agregar(self,simbolo,valor,tipo,tabla=None):
		self.tabla[simbolo] = datos(valor,tipo,tabla) 	# El True es de datos.declarada (quiza no hace falta)

	#---------------------------------------------------------------------------
	# agregarTablaRobot()
	#
	# 
	#---------------------------------------------------------------------------	
	def agregarTablaRobot(self,simbolo,tabla): # Para agregar 
		self.robot[simbolo] = tabla

	#---------------------------------------------------------------------------
	# buscarAqui()
	#
	# Verifica si un simbolo esta en la tabla o no
	#--------------------------------------------------------------------------	
	def buscarAqui(self,simbolo):
		if simbolo in self.tabla:
			return True
		else:
			return False

	#---------------------------------------------------------------------------
	# buscarEnTodos()
	#
	# Busca un simbolo en la tabla y en sus padres
	#--------------------------------------------------------------------------	
	def buscarEnTodos(self,simbolo,opcion):	# Opcion para saber si se quiere buscar el tipo/valor de un elemento
		if self.buscarAqui(simbolo):		# de la tabla o si se quiere saber si esta o no declarada
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

#-------------------------------------------------------------------------------
#							    DATOS
#-------------------------------------------------------------------------------
class datos:
	def __init__(self,valor,tipo,tabla):
		self.valor = valor
		self.tipo = tipo
		self.tabla = tabla
		self.estado = None
		self.tieneDefault = False

	#---------------------------------------------------------------------------
	# getValor()
	#
	# Regresa el valor del dato
	#--------------------------------------------------------------------------	

	def getValor(self):
		return self.valor

	#---------------------------------------------------------------------------
	# getTipo()
	#
	# Regresa el tipo del dato
	#--------------------------------------------------------------------------	
	def getTipo(self):
		return self.tipo
