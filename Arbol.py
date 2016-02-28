#-------------------------------------------------------------------------------
#							    ARBOL
#-------------------------------------------------------------------------------

class arbol(object):
	def __init__(self,tipo,hijos):
		self.type = tipo 				# Almacena el tipo de instruccion en el arbol
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
		if self.type == 'MENOR_QUE'\
		or self.type == 'MENOR_IGUAL'\
		or self.type == 'MAYOR'\
		or self.type == 'MAYOR_IGUAL'\
		or self.type == 'IGUALDAD'\
		or self.type == 'DISTINTO':
			binario_rel = True
		return binario_rel
	
	#---------------------------------------------------------------------------
	# Es_bin_logica()
	#
	# Verifica si el nodo es una relacion binario logica
	#---------------------------------------------------------------------------
	def Es_bin_logica(self):
		binario_log = False
		if self.type == 'CONJUNCION'\
		or self.type == 'DISYUNCION':
			binario_log = True
		return binario_log
	
	#---------------------------------------------------------------------------
	# Es_bin_aritmetica()
	#
	# Verifica si el nodo es una relacion binario aritmetica
	#---------------------------------------------------------------------------
	def Es_bin_aritmetica(self):
		binario_ari = False
		if self.type == 'SUMA'\
		or self.type == 'RESTA'\
		or self.type == 'DIVISION'\
		or self.type == 'MULTIPLICACION'\
		or self.type == 'MODULO':
			binario_ari = True
		return binario_ari

	#---------------------------------------------------------------------------
	# Es_bin_aritmetica()
	#
	# Verifica si el nodo es una relacion binario aritmetica
	#---------------------------------------------------------------------------
	def es_unario(self):
		unario = False
		if self.type == 'NEGACION'\
		or self.type == 'NEGATIVO':
			unario = True
		return unario

	#---------------------------------------------------------------------------
	# imprimir_tipo_OP()
	#
	# Imprime el tipo de operacion
	#---------------------------------------------------------------------------
	def imprimir_tipo_OP(self):
		# Operaciones relacionales
		if self.type == 'MENOR_QUE':
			print('’Menor que’')
		elif self.type == 'MENOR_IGUAL':
			print('’Menor o igual que’')
		elif self.type == 'MAYOR':
			print('’Mayor que’')
		elif self.type == 'MAYOR_IGUAL':
			print('’Mayor o igual que’')
		elif self.type == 'IGUALDAD':
			print('’Igual a’')
		elif self.type == 'DISTINTO':
			print('’Distinto a’')
		
		# Operaciones logicas	
		elif self.type == 'DISYUNCION':
			print('’Disyuncion’')
		elif self.type == 'CONJUNCION':
			print('’Conjuncion’')
		
		# Operaciones aritmeticas
		elif self.type == 'SUMA':
			print('’Suma’')
		elif self.type == 'RESTA':
			print('’Resta’')
		elif self.type == 'MULTIPLICACION':
			print('’Multiplicacion’')
		elif self.type == 'DIVISION':
			print('’Division’')
		elif self.type == 'MODULO':
			print('’Modulo’')

	#---------------------------------------------------------------------------
	# Imprimir_operacion()
	#
	# Imprime el tipo de operacion y los operadores izquierdo y derecho
	#---------------------------------------------------------------------------
	def Imprimir_operacion(self,nivel,imprimir=None):		
		print('\t'*(nivel+1)+'- operacion: ',end="") 	
		self.imprimir_tipo_OP()
		n = 1
		for i in self.hijos:
			if n == 1:
				print('\t'*(nivel+1)+'- operador izquierdo: ',end="")
				n+= 1
			elif n == 2:
				print('\t'*(nivel+1)+'- operador derecho: ',end="")
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
				if h.type == '- var: ':
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
				if h.type == '- var: ':
					print('\t'*(nivel+1)+str(h.type),end='')
					for i in h.hijos:
						print(i)
				
				elif h.type == '- lis_var: ':
					h.Imprimir_variables(nivel)
				
				elif h.type == 'TRUE' or h.type == 'FALSE':
					print(h.type)
			else:
				print('',h)

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
		if self.type == 'INSTRUCCIONES_ROBOT': 		# Si el nodo es una intruccion
			imprimir = False 						# robot se ignora
		elif self.type == 'EXECUTE':				# Si el nodo es del tipo execute 
			imprimir = True 						# comienza a imprimir
		
		if imprimir:
			# Si es EXECUTE no lo imprime
			if self.type == 'EXECUTE':
				 pass
			# Si es un literal booleano imprime su valor
			elif self.type == 'TRUE' or self.type == 'FALSE':
				print('',self.type)
			# Si es ACTIVATE:
			# > imprime el tipo y la lista de variables que se activen
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION
			elif self.type == 'ACTIVATE':
				for i in self.hijos:					
					if  (self.es_arbol(i))\
					and (i.type == 'INST_CONT')\
					and (not (secuenciado)):		
						print('\t'*(nivel-1)+'SECUENCIACION')
						secuenciado = True
				print('\t'*nivel+'ACTIVACION')
				self.Imprimir_variables(nivel)
			# Si es DEACTIVATE:
			# > imprime el tipo y la lista de variables que se desactiven
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION
			elif self.type == 'DEACTIVATE':
				for i in self.hijos:				
					if  ( self.es_arbol(i) )\
					and ( i.type == 'INST_CONT' )\
					and ( not (secuenciado) ):		
						print('\t'*(nivel-1)+'SECUENCIACION')
						secuenciado = True
				print('\t'*nivel+'DESACTIVACION')	
				self.Imprimir_variables(nivel)		
			# Si es ADVANCE:
			# > imprime el "- exito: " seguido por el tipo y la lista de variables 
			#   que se activen
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION
			elif self.type == 'ADVANCE':
				for i in self.hijos:
					if  ( self.es_arbol(i) )\
					and ( i.type == 'INST_CONT' )\
					and ( not (secuenciado) ):
						print('\t'*(nivel-1)+'SECUENCIACION')
						secuenciado = True
				print('\t'*nivel+'-exito: AVANCE')
				self.Imprimir_variables(nivel)
			# Si es CONDICIONAL:
			# > imprime el tipo y "- guardia: " esperando que lo proxima iteracion 
			#   imprima el tipo de guardia
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION			
			elif self.type == 'CONDICIONAL':
				for i in self.hijos:
					if  ( self.es_arbol(i) )\
					and ( i.type == 'INST_CONT' )\
					and ( not (secuenciado) ):
						print('\t'*(nivel-1)+'SECUENCIACION')
						secuenciado = True
				print('\t'*nivel+self.type)
				print('\t'*(nivel+1)+'- guardia:',end="")
			# Si es CICLO:
			# > imprime el tipo y "- guardia: " esperando que lo proxima iteracion 
			#   imprima el tipo de guardia
			# > verifica si el ultimo hijo es una instruccion, si lo es lo 
			#   considera una secuenciacion y si no se ha impreso aun, 
			#   imprime SECUENCIACION				
			elif self.type == 'CICLO':
				for i in self.hijos:
					if  ( self.es_arbol(i) )\
					and ( i.type == 'INST_CONT' )\
					and ( not (secuenciado) ):
						print('\t'*(nivel-1)+'SECUENCIACION')
						secuenciado = True
				print('\t'*nivel+self.type)
				print('\t'*(nivel+1)+'- guardia:',end="")

			# Si la expresion tiene un operador unario primero imprime el operador
			elif self.es_unario():
				if self.type == 'NEGACION':
					print('~',end='')
				else:
					print('-',end='')

			# Si es una relacion binaria:
			# > Verifica que tipo de relacion es lo imprime y luego imprime 
			#   la operacion
			elif self.Es_bin_relacional():
				print(' BIN_RELACIONAL')
				imprimir = False
				nivel = self.Imprimir_operacion(nivel,imprimir)
			elif self.Es_bin_logica():
				print(' BIN_LOGICA')
				imprimir = False
				nivel = self.Imprimir_operacion(nivel,imprimir)
			elif self.Es_bin_aritmetica():
				print(' BIN_ARITMETICA')
				imprimir = False
				nivel = self.Imprimir_operacion(nivel,imprimir)
			# Si es un entero booleano expresion o caracter imprime la variable
			elif self.type == 'ENTERO'\
			or   self.type == 'BOOLEANO'\
			or   self.type == 'EXPRESION'\
			or   self.type == 'CARACTER'\
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
	def __init__(self,type,hijos):
		arbol.__init__(self,type,hijos)

# INstrouccion del robot
class instContr(arbol):
	def __init__(self,type,hijos):
		arbol.__init__(self,type,hijos)

# Controlador
class instRobot(arbol):
	def __init__(self,type,hijos):
		arbol.__init__(self,type,hijos)