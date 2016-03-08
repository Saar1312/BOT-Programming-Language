class pila:
	def __init__(self):
		self.pila = []
		self.posTope = None
		self.tope = None
	def addTope(self,pointer): 	# Nodo es el nodo del arbol sintactico que permite saber si ya se termino de leer
		self.pila.append(pointer)# la incorporacion de alcance, lo que indica que hay que volver el apuntador del
	def popTope(self):									# arbol de tablas a la tabla externa.
		if len(self.pila) != 0:
			return self.pila.pop()
		else:
			return None
	def getPosTope(self):
		return len(self.pila) - 1
	def getTope(self):
		posTope = self.getPosTope()
		if posTope == -1:
			return None
		else:	
			return self.pila[posTope]
