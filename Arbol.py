#-------------------------------------------------------------------------------
#							    ARBOL
#-------------------------------------------------------------------------------

class arbol(object):
	def __init__(self,tipo,hijos):
		self.nombre = tipo 				# Almacena el tipo de instruccion en el arbol
		if hijos:						
			self.hijos = hijos			# Almacena la lista de instruccion que 
										# componen a la expresion/instruccion
		else:
			self.hijos = []

	#---------------------------------------------------------------------------
	# Es_bin_relacional()
	#
	# Verifica si el nodo es una relacion binario relacional
	#---------------------------------------------------------------------------
	def Es_bin_relacional(self):		
		binario_rel = False
		if self.nombre == "MENOR_QUE"\
		or self.nombre == "MENOR_IGUAL"\
		or self.nombre == "MAYOR"\
		or self.nombre == "MAYOR_IGUAL"\
		or self.nombre == "IGUALDAD"\
		or self.nombre == "DISTINTO":
			binario_rel = True
		return binario_rel
	
	#---------------------------------------------------------------------------
	# Es_bin_logica()
	#
	# Verifica si el nodo es una relacion binario logica
	#---------------------------------------------------------------------------
	def Es_bin_logica(self):
		binario_log = False
		if self.nombre == "CONJUNCION"\
		or self.nombre == "DISYUNCION":
			binario_log = True
		return binario_log
	
	#---------------------------------------------------------------------------
	# Es_bin_aritmetica()
	#
	# Verifica si el nodo es una relacion binario aritmetica
	#---------------------------------------------------------------------------
	def Es_bin_aritmetica(self):
		binario_ari = False
		if self.nombre == "SUMA"\
		or self.nombre == "RESTA"\
		or self.nombre == "DIVISION"\
		or self.nombre == "MULTIPLICACION"\
		or self.nombre == "MODULO":
			binario_ari = True
		return binario_ari

	#---------------------------------------------------------------------------
	# Es_bin_aritmetica()
	#
	# Verifica si el nodo es una relacion binario aritmetica
	#---------------------------------------------------------------------------
	def es_unario(self):
		unario = False
		if self.nombre == "NEGACION"\
		or self.nombre == "NEGATIVO":
			unario = True
		return unario

	#---------------------------------------------------------------------------
	# imprimir_tipo_OP()
	#
	# Imprime el tipo de operacion
	#---------------------------------------------------------------------------
	def imprimir_tipo_OP(self):
		# Operaciones relacionales
		if self.nombre == "MENOR_QUE":
			print("'Menor que'")
		elif self.nombre == "MENOR_IGUAL":
			print("'Menor o igual que'")
		elif self.nombre == "MAYOR":
			print("'Mayor que'")
		elif self.nombre == "MAYOR_IGUAL":
			print("'Mayor o igual que'")
		elif self.nombre == "IGUALDAD":
			print("'Igual a'")
		elif self.nombre == "DISTINTO":
			print("'Distinto a'")
		
		# Operaciones logicas	
		elif self.nombre == "DISYUNCION":
			print("'Disyuncion'")
		elif self.nombre == "CONJUNCION":
			print("'Conjuncion'")
		
		# Operaciones aritmeticas
		elif self.nombre == "SUMA":
			print("'Suma'")
		elif self.nombre == "RESTA":
			print("'Resta'")
		elif self.nombre == "MULTIPLICACION":
			print("'Multiplicacion'")
		elif self.nombre == "DIVISION":
			print("'Division'")
		elif self.nombre == "MODULO":
			print("'Modulo'")

	#---------------------------------------------------------------------------
	# Imprimir_operacion()
	#
	# Imprime el tipo de operacion y los operadores izquierdo y derecho
	#---------------------------------------------------------------------------
	def Imprimir_operacion(self,nivel,imprimir=None):		
		print("\t"*(nivel+1)+"- operacion: ",end="") 	
		self.imprimir_tipo_OP()
		n = 1
		for i in self.hijos:
			if n == 1:
				print("\t"*(nivel+1)+"- operador izquierdo: ",end="")
				n+= 1
			elif n == 2:
				print("\t"*(nivel+1)+"- operador derecho: ",end="")
			imprimir = True
			i.imprimirArbol(nivel+1,imprimir)	# Imprime el nodo de cada hijo
			i.Imprimir_variables_OP(nivel)

	#---------------------------------------------------------------------------
	# Imprimir_variables_OP()
	#
	# Si es una variable la imprime sin el prefijo "- var: "
	#---------------------------------------------------------------------------
	def Imprimir_variables_OP(self,nivel):
		for h in self.hijos:
			if self.es_arbol(h):
				if h.nombre == "- var: ":
					for i in h.hijos:
						if not h.es_arbol(i): 
							print(i)
	#---------------------------------------------------------------------------
	# Imprimir_variables()
	#
	# Verifica si es una lista de variable so una variable sola, y la imprime
	#---------------------------------------------------------------------------
	def Imprimir_variables(self,nivel):
		for h in self.hijos:
			if self.es_arbol(h):
				if h.nombre == "- var: ":
					print("\t"*(nivel+1)+str(h.nombre),end="")
					for i in h.hijos:
						print(i)
				
				elif h.nombre == "- lis_var: ":
					h.Imprimir_variables(nivel)
				
				elif h.nombre == "TRUE" or h.nombre == "FALSE":
					print(h.nombre)
			else:
				print("",h)

	#---------------------------------------------------------------------------
	# es_arbol()
	#
	# Verifica si el argumento h es un arbol
	#---------------------------------------------------------------------------
	def es_arbol(self,h):
		if not ((type(h) != arbol)\
			and (type(h) != expresion)\
			and (type(h) != instContr)\
			and (type(h) != instRobot)):
				return True
		return False

	#---------------------------------------------------------------------------
	# imprimirArbol()
	#
	# Imprime la estructura de arbol
	#---------------------------------------------------------------------------
	def imprimirArbol(self,nivel,imprimir=None,secuenciado=False):
		if self.nombre == "INSTRUCCIONES_ROBOT": 		# Si el nodo es una intruccion
			imprimir = False 						# robot se ignora
		elif self.nombre == "EXECUTE":				# Si el nodo es del tipo execute 
			imprimir = True 						# comienza a imprimir
		
		if imprimir:
			# Si es EXECUTE no lo imprime
			if self.nombre == "EXECUTE":
				 pass
			# Si es un literal booleano imprime su valor
			elif self.nombre == "TRUE" or self.nombre == "FALSE":
				print("",self.nombre)
			# Si es ACTIVATE:
			# > imprime el tipo y la lista de variables que se activen
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION
			elif self.nombre == "ACTIVATE":
				for i in self.hijos:					
					if  (self.es_arbol(i))\
					and (i.nombre == "INST_CONT")\
					and (not (secuenciado)):		
						print("\t"*(nivel-1)+"SECUENCIACION")
						secuenciado = True
				print("\t"*nivel+"ACTIVACION")
				self.Imprimir_variables(nivel)
			# Si es DEACTIVATE:
			# > imprime el tipo y la lista de variables que se desactiven
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION
			elif self.nombre == "DEACTIVATE":
				for i in self.hijos:				
					if  ( self.es_arbol(i) )\
					and ( i.nombre == "INST_CONT" )\
					and ( not (secuenciado) ):		
						print("\t"*(nivel-1)+"SECUENCIACION")
						secuenciado = True
				print("\t"*nivel+"DESACTIVACION")	
				self.Imprimir_variables(nivel)		
			# Si es ADVANCE:
			# > imprime el "- exito: " seguido por el tipo y la lista de variables 
			#   que se activen
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION
			elif self.nombre == "ADVANCE":
				for i in self.hijos:
					if  ( self.es_arbol(i) )\
					and ( i.nombre == "INST_CONT" )\
					and ( not (secuenciado) ):
						print("\t"*(nivel-1)+"SECUENCIACION")
						secuenciado = True
				print("\t"*nivel+"-exito: AVANCE")
				self.Imprimir_variables(nivel)
			# Si es CONDICIONAL:
			# > imprime el tipo y "- guardia: " esperando que lo proxima iteracion 
			#   imprima el tipo de guardia
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION			
			elif self.nombre == "CONDICIONAL":
				for i in self.hijos:
					if  ( self.es_arbol(i) )\
					and ( i.nombre == "INST_CONT" )\
					and ( not (secuenciado) ):
						print("\t"*(nivel-1)+"SECUENCIACION")
						secuenciado = True
				print("\t"*nivel+self.nombre)
				print("\t"*(nivel+1)+"- guardia:",end="")
			# Si es CICLO:
			# > imprime el tipo y "- guardia: " esperando que lo proxima iteracion 
			#   imprima el tipo de guardia
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION				
			elif self.nombre == "CICLO":
				for i in self.hijos:
					if  ( self.es_arbol(i) )\
					and ( i.nombre == "INST_CONT" )\
					and ( not (secuenciado) ):
						print("\t"*(nivel-1)+"SECUENCIACION")
						secuenciado = True
				print("\t"*nivel+self.nombre)
				print("\t"*(nivel+1)+"- guardia:",end="")

			# Si la expresion tiene un operador unario primero imprime el operador
			elif self.es_unario():
				if self.nombre == "NEGACION":
					print("~",end="")
				else:
					print("-",end="")

			# Si es una relacion binaria:
			# > Verifica que tipo de relacion es lo imprime y luego imprime 
			#   la operacion
			elif self.Es_bin_relacional():
				print(" BIN_RELACIONAL")
				imprimir = False
				nivel = self.Imprimir_operacion(nivel,imprimir)
			elif self.Es_bin_logica():
				print(" BIN_LOGICA")
				imprimir = False
				nivel = self.Imprimir_operacion(nivel,imprimir)
			elif self.Es_bin_aritmetica():
				print(" BIN_ARITMETICA")
				imprimir = False
				nivel = self.Imprimir_operacion(nivel,imprimir)
			# Si es un entero booleano expresion o caracter imprime la variable
			elif self.nombre == "ENTERO"\
			or   self.nombre == "BOOLEANO"\
			or   self.nombre == "EXPRESION"\
			or   self.nombre == "CARACTER"\
			or 	 type(self) == chr:
				imprimir = False				
				self.Imprimir_variables(nivel)
		# Para los hijos del nodo verifica si es un arbol y segun sea el 
		# caso lo imprime identado o no
		for hijo in self.hijos:
			if self.es_arbol(hijo):
				if imprimir and not(secuenciado):
					hijo.imprimirArbol(nivel+1,imprimir,secuenciado)
				else:
					hijo.imprimirArbol(nivel,imprimir,secuenciado)


# Expresiones
class expresion(arbol):
	def __init__(self,nombre,hijos,tipo):
		arbol.__init__(self,nombre,hijos)
		self.tipo = tipo

# INstrouccion del robot
class instContr(arbol):
	def __init__(self,nombre,hijos):
		arbol.__init__(self,nombre,hijos)

# Controlador
class instRobot(arbol):
	def __init__(self,nombre,hijos):
		arbol.__init__(self,nombre,hijos)

class defTipo(arbol):
	def __init__(self,nombre,hijos,tipo):
		arbol.__init__(self,nombre,hijos)
		self.tipo = tipo
