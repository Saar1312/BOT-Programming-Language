#-------------------------------------------------------------------------------
#							    TABLA
#-------------------------------------------------------------------------------

import sys
from Parser import *
from Pila import *
from Arbol import *

class Tabla:
	def __init__(self,exterior):
		self.tablaExterna = exterior
		self.tabla = {}
	#---------------------------------------------------------------------------
	# agregar()
	#
	# anade un simbolo a la tabla de simbolos
	#---------------------------------------------------------------------------	
	def agregar(self,simbolo,valor,tipo,comportamientos=None,tabla=None):
		self.tabla[simbolo] = datos(valor,tipo,comportamientos,tabla) 	# El True es de datos.declarada (quiza no hace falta)

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
			elif opcion == 'getDatos':
				return self.tabla[simbolo]
		else:
			if self.tablaExterna:
				return self.tablaExterna.buscarEnTodos(simbolo,opcion)
			else:
				if opcion == 'buscar': # Si llega arriba y no lo encontro
					return False
				else:
					return None
	def fetch(self,simbolo,robot,execute): # Busca robots o variables y retorna su valor
		# acomodar: cuando se busca un robot, no busca el robot bien?
		datos = self.buscarEnTodos(robot,'getDatos')
		if execute:
			return datos
		else:
			return datos.tabla.tabla[simbolo] # Revisar si es datos.tabla.tabla o datos.tabla

	#---------------------------------------------------------------------------
	# esArbol()
	#
	# Permite saber si un objeto es un arbol
	#--------------------------------------------------------------------------	
def esArbol(h):
	if type(h) in [arbol,expresion,instContr,\
				instRobot]:
		return True
	return False

# Inicializando variables globales con las que trabaja la funcion crearTabla
tabla = Tabla(None)
pointer = tabla
tipo = None
p = pila()
bots = [] # Almacena la ultima lista de robots declarados juntos (en una misma instruccion, ej: int bot a,b)
		  # Sirve para cambiar el estado de los robots a los que pertenezca un comportamiento
comp = None # Nodo raiz de los comportamientos de un robot
	#---------------------------------------------------------------------------
	# crearTabla()
	#
	# Crea la tabla de simbolos, realiza la verificacion de tipos e imprime 
	# errores semanticos (hace toda vaina)
	#--------------------------------------------------------------------------	
def crearTabla(arbol,almacenar):
	global tipo,pointer,p,incAlcance,bots,comp
	if arbol.nombre == 'INSTRUCCIONES_ROBOT': # Crea la tabla para la inc de alcance solo si hay una inc de 
		almacenar = True					  # alcance y en esta se declaran robots
	elif arbol.nombre == 'INICIO':
		almacenar = True
	elif arbol.nombre == 'EXECUTE':
		almacenar = False
	elif arbol.nombre == 'CONDICION': # Arbol de las instrucciones On activation/default/...
		p.addTope(pointer)
		t = list(pointer.tabla.values())[0].tabla # Mueve el apuntador a la tabla de simbolos asociada a cualquiera de las variables
		pointer = t
	elif arbol.nombre == 'INC_ALCANCE': # NUEVO Para bajar el apuntador de tablas a un nuevo nivel inferior
		p.addTope(pointer)
		t = Tabla(pointer)
		pointer = t
		arbol.tabla = t
	if esArbol(arbol):
		if almacenar:
			if arbol.nombre == 'DECLARACION_ROBOT':
				tipo = arbol.hijos[0].tipo
				arbol.hijos[1].tipo = tipo
				simbolo = arbol.hijos[1].hijos[0]
				comp = arbol.hijos[3]
				t = Tabla(None) 						# t es la tabla de simbolos para las instrucciones de cada robot
				me_tabla = Tabla(None)
				t.agregar('me',None,tipo,None,me_tabla)				# No tiene padre porque la idea es que las instrucciones de robot no 
				pointer.agregar(simbolo,None,tipo,comp,t)	# usen a los robots declarados.
				bots = [simbolo]						# t no recibe ninguna tabla, por lo que tiene 3 argumentos
				
			elif arbol.nombre == 'LISTA':
				simbolo = arbol.hijos[0].hijos[0]
				arbol.hijos[0].tipo = tipo # Agregando el tipo a la variable
				t = Tabla(None)
				me_tabla = Tabla(None)
				t.agregar('me',None,tipo,None,me_tabla)
				pointer.agregar(simbolo,None,tipo,comp,t)
				bots += [simbolo]

			elif (arbol.nombre == 'COLLECT' and 
				 arbol.hijos != []): 
				if arbol.hijos[0].nombre == 'COLLECT_AS':
					tope = p.getTope()
					p.addTope(pointer)
					pointer = tope
					simbolo = arbol.hijos[0].hijos[0].hijos[0]
					arbol.hijos[0].hijos[0].tipo = tipo
					for robot,datos in pointer.tabla.items():
						datos.tabla.agregar(simbolo,None,tipo)
					pointer = p.popTope()

			elif (arbol.nombre == 'READ_AS' and
				 arbol.hijos != []):
				tope = p.getTope()
				p.addTope(pointer)
				pointer = tope
				simbolo = arbol.hijos[0].hijos[0]
				arbol.hijos[0].tipo = tipo
				for robot,datos in pointer.tabla.items():
					datos.tabla.agregar(simbolo,None,tipo)
				pointer = p.popTope()

			elif arbol.nombre == 'ACTIVACION':
				tope = p.getTope()
				p.addTope(pointer)
				pointer = tope
				for robot in bots:
					datos = pointer.tabla[robot]
					if datos.estado == 'activacion':
						print("Error en la linea %d:" % (arbol.linea))
						print("Un robot no puede tener dos comportamientos de activacion.")
						sys.exit()
					elif datos.estado == None:
						datos.estado = 'activacion'
					elif datos.estado == 'desactivacion':
						print("Error en la linea %d:" % (arbol.linea))
						print("Un comportamiento \"activation\" no puede estar precedido por \
														un \"deactivation\" .")
						sys.exit()
					elif datos.tieneDefault:
						print("Error en la linea %d:" % (arbol.linea))
						print("Un comportamiento \"activation\" no puede estar precedido por \
														un \"default\" .")
						sys.exit()
				pointer = p.popTope()

			elif arbol.nombre == 'DESACTIVACION':
				tope = p.getTope()
				p.addTope(pointer)
				pointer = tope
				for robot in bots:
					datos = pointer.tabla[robot]
					if datos.estado == 'activacion':
						datos.estado = 'desactivacion'
					elif datos.estado == None:
						print("Error en la linea %d:" % (arbol.linea))
						print("El comportamiento \"deactivation\" debe estar precedido por\
																un activacion.")
						sys.exit()
					elif datos.estado == 'desactivacion':
						print("Error en la linea %d:" % (arbol.linea))
						print("Un robot no puede tener dos comportamientos de desactivacion.")
						sys.exit()
				pointer = p.popTope()

			elif arbol.nombre == 'DEFAULT':
				tope = p.getTope()
				p.addTope(pointer)
				pointer = tope
				for robot in bots:
					datos = pointer.tabla[robot]
					if not datos.tieneDefault:
						datos.tieneDefault = True
					elif datos.tieneDefault:
						print("Error en la linea %d:" % (arbol.linea))
						print("Un robot no puede tener dos comportamientos default.")
						sys.exit()
					if datos.estado == None:
						print("Error en la linea %d:" % (arbol.linea))
						print("El comportamiento debe estar precedido por un \"activation\".")
						sys.exit()
					elif datos.estado == 'desactivacion':
						print("Error en la linea %d:" % (arbol.linea))
						print("El comportamiento no puede estar precedido por un \"deactivation\".")
						sys.exit()
				pointer = p.popTope()

			elif arbol.nombre == 'ON_EXPRESION':
				tope = p.getTope()
				p.addTope(pointer)
				pointer = tope
				for robot in bots:
					datos = pointer.tabla[robot]
					if datos.estado == None:
						print("Error en la linea %d:" % (arbol.linea))
						print("El comportamiento debe estar precedido por un \"activation\".")
						sys.exit()
					elif datos.estado == 'desactivacion':
						print("Error en la linea %d:" % (arbol.linea))
						print("El comportamiento no puede estar precedido por un \"deactivation\".")
						sys.exit()
					if datos.tieneDefault:
						print("Error en la linea %d:" % (arbol.linea))
						print("El comportamiento no puede estar precedido por un \"default\".")
						sys.exit()
				pointer = p.popTope()

		for rama in arbol.hijos:
			if rama in ['incAlcance','instRobot']: # incAlcance es un hijo de los arboles
				pointer = p.popTope()# de inc de alcance que permite saber si termino la
			else:					 # inc. de alcance para mover el apuntador de tablas
				if esArbol(rama):
					crearTabla(rama,almacenar)
					if type(rama) == expresion:
						if rama.nombre in ['CONJUNCION','DISYUNCION']:
							if rama.hijos[0].tipo == rama.hijos[1].tipo:
								if rama.hijos[0].tipo != 'bool':
									print("Error de tipos en la linea %d:" % (rama.linea))
									print("No es posible operar elementos del tipo \"%s\""%\
															  (rama.hijos[0].tipo),end=" ")
									print("con un operador booleano.")
									sys.exit()
							else:
								print("Error de tipos en la linea %d:" % (rama.linea))
								print("No es posible operar un elemento del tipo \"%s\""%\
														  (rama.hijos[0].tipo),end=" ")
								print("con otro de tipo \"%s\"."% (rama.hijos[1].tipo))
								sys.exit()

						elif rama.nombre in ['DISTINTO','IGUALDAD']:
							if rama.hijos[0].tipo != rama.hijos[1].tipo:
								print("Error de tipos en la linea %d:" % (rama.linea))
								print("No es posible operar un elemento del tipo \"%s\""%\
														  (rama.hijos[0].tipo),end=" ")
								print("con otro de tipo \"%s\"."%(rama.hijos[1].tipo))
								sys.exit()

						elif rama.nombre in ['MENOR_QUE','MENOR_IGUAL','MAYOR','MAYOR_IGUAL']:
							if rama.hijos[0].tipo == rama.hijos[1].tipo:
								if rama.hijos[0].tipo != 'int':
									print("Error de tipos en la linea %d:" % (rama.linea))
									print("No es posible operar elementos del tipo \"%s\""%\
															  (rama.hijos[0].tipo),end=" ")
									print("con un operador booleano.")
									sys.exit()
							else:
								print("Error de tipos en la linea %d:" % (rama.linea))
								print("No es posible operar un elemento del tipo \"%s\""%\
														  (rama.hijos[0].tipo),end=" ")
								print("con otro de tipo \"%s\"."% (rama.hijos[1].tipo))
								sys.exit()

						elif rama.nombre in ['SUMA','RESTA','MULTIPLICACION','DIVISION','MODULO']:
							if rama.hijos[0].tipo == rama.hijos[1].tipo:
								if rama.hijos[0].tipo != 'int':
									print("Error de tipos en la linea %d:" % (rama.linea))
									print("No es posible operar elementos del tipo \"%s\""%\
															  (rama.hijos[0].tipo),end=" ")
									print("con un operador aritmetico.")
									sys.exit()
							else:
								print("Error de tipos en la linea %d:" % (rama.linea))
								print("No es posible operar un elemento del tipo \"%s\""%\
														  (rama.hijos[0].tipo),end=" ")
								print("con otro de tipo \"%s\"."% (rama.hijos[1].tipo))
								sys.exit()

						elif rama.nombre == 'NEGACION':
							if rama.hijos[0].tipo != 'bool':
								print("Error de tipos en la linea %d:" % (rama.linea))
								print("Se esperaba una expresion de tipo booleano,",end=' ')
								print("pero fue dada una de tipo \"%s\"." % (rama.hijos[0].tipo))
								sys.exit()

						elif rama.nombre == 'NEGATIVO':
							if rama.hijos[0].tipo != 'int':
								print("Error de tipos en la linea %d:" % (rama.linea))
								print("Se esperaba una expresion de tipo entero,",end=' ')
								print("pero fue dada una de tipo \"%s\"." % (rama.hijos[0].tipo))
								sys.exit()

						elif rama.nombre == 'PARENTESIS':
							rama.tipo = rama.hijos[0].tipo

						elif rama.nombre == 'VAR':
							if rama.hijos[0] == 'me' and almacenar == False:
								print("Error en la linea %d: La variable \"me\" no puede ser . \
															utilizada en la seccion de ejecucion")
								sys.exit()
							t = pointer.buscarEnTodos(rama.hijos[0],'getTipo')
							if t: 				 # Busca el tipo en la tabla de simbolos apuntada 
								rama.tipo = t	 # actualmente y en las superiores. Si lo encuentra,
												 # retorna el tipo. Si no, retorna None y no entra
							else: 				 # en el condicional y debe dar error
								print("Error en la linea %d: La variable \"%s\" no ha sido declarada." \
															% (rama.linea, rama.hijos[0]))
								sys.exit()
						elif rama.nombre == 'ON_CONDICION':
							if rama.hijos[0].tipo != 'bool':
								print("Error en la linea %d: La condicion del robot debe evaluar en un booleano.")
								sys.exit()


#-------------------------------------------------------------------------------
#							    DATOS
#-------------------------------------------------------------------------------
class datos:
	def __init__(self,valor,tipo,comportamientos,tabla):
		self.valor = valor
		self.tipo = tipo
		self.tabla = tabla
		self.estado = None
		self.posicion = '00' # Corrdenadas del robot inicialmente
		self.tieneDefault = False 			   # Determina si un robot ya tiene un comportamiento default
		self.comportamientos = comportamientos # Almacenara el nodo que tiene como hijos los comportmientos
											   # del robot

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
