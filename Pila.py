#-------------------------------------------------------------------------------
#							    PILA
#-------------------------------------------------------------------------------
class pila:
	
	def __init__(self):
		self.pila = []
		self.posTope = None
		self.tope = None
	#---------------------------------------------------------------------------
	# addTope()
	#
	# Anade un nodo al tope de la pila
	#---------------------------------------------------------------------------	
	def addTope(self,pointer): 		# Nodo es el nodo del arbol sintactico que permite saber si ya se termino de leer
		self.pila.append(pointer)	# la incorporacion de alcance, lo que indica que hay que volver el apuntador del
									# arbol de tablas a la tabla externa.

	#---------------------------------------------------------------------------
	# popTope()
	#
	# Saca el nodo en el tope de la pila
	#---------------------------------------------------------------------------
	def popTope(self):				
		if len(self.pila) != 0:
			return self.pila.pop()
		else:
			return None

	#---------------------------------------------------------------------------
	# getPosTope()
	#
	# regresa la posicion en la que se encuentra el tope
	#---------------------------------------------------------------------------	
	def getPosTope(self):
		return len(self.pila) - 1

	#---------------------------------------------------------------------------
	# getTope()
	#
	# Retorna el valor en el tope de la pila, sin hacer pop
	#---------------------------------------------------------------------------	
	def getTope(self):
		posTope = self.getPosTope()
		if posTope == -1:
			return None
		else:	
			return self.pila[posTope]


