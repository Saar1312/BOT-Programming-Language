#-------------------------------------------------------------------------------
#							    ARBOL
#-------------------------------------------------------------------------------

class arbol(object):
	def __init__(self,tipo,hijos):
		self.nombre = tipo 				# Almacena el tipo de instruccion en el arbol
		self.tipo = None
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
		if self.nombre in ['MENOR_QUE','MENOR_IGUAL','MAYOR',\
						'MAYOR_IGUAL','IGUALDAD','DISTINTO']:
			binario_rel = True
		return binario_rel
	
	#---------------------------------------------------------------------------
	# Es_bin_logica()
	#
	# Verifica si el nodo es una relacion binario logica
	#---------------------------------------------------------------------------
	def Es_bin_logica(self):
		binario_log = False
		if self.nombre in ["CONJUNCION","DISYUNCION"]:
			binario_log = True
		return binario_log
	
	#---------------------------------------------------------------------------
	# Es_bin_aritmetica()
	#
	# Verifica si el nodo es una relacion binario aritmetica
	#---------------------------------------------------------------------------
	def Es_bin_aritmetica(self):
		binario_ari = False
		if self.nombre in ['SUMA','RESTA','DIVISION'\
						,'MULTIPLICACION','MODULO']:
			binario_ari = True
			binario_ari = True
		return binario_ari

	#---------------------------------------------------------------------------
	# Es_bin_aritmetica()
	#
	# Verifica si el nodo es una relacion binario aritmetica
	#---------------------------------------------------------------------------
	def es_unario(self):
		unario = False
		if self.nombre in ["NEGACION","NEGATIVO"]:
			unario = True
		return unario

	#---------------------------------------------------------------------------
	# imprimir_tipo_OP()
	#
	# Imprime el tipo de operacion
	#---------------------------------------------------------------------------
	def imprimir_tipo_OP(self,nivel):
		es_operacion = True
		op = ''
		# Operaciones relacionales
		if self.nombre == "MENOR_QUE":
			op = "'Menor que'"
		elif self.nombre == "MENOR_IGUAL":
			op = "'Menor o igual que'"
		elif self.nombre == "MAYOR":
			op = "'Mayor que'"
		elif self.nombre == "MAYOR_IGUAL":
			op = "'Mayor o igual que'"
		elif self.nombre == "IGUALDAD":
			op = "'Igual a'"
		elif self.nombre == "DISTINTO":
			op = "'Distinto a'"
		
		# Operaciones logicas	
		elif self.nombre == "DISYUNCION":
			op = "'Disyuncion'"
		elif self.nombre == "CONJUNCION":
			op = "'Conjuncion'"
		
		# Operaciones aritmeticas
		elif self.nombre == "SUMA":
			op = "'Suma'"
		elif self.nombre == "RESTA":
			op = "'Resta'"
		elif self.nombre == "MULTIPLICACION":
			op = "'Multiplicacion'"
		elif self.nombre == "DIVISION":
			op = "'Division'"
		elif self.nombre == "MODULO":
			op = "'Modulo'"
		
		else:
			es_operacion = False

		if es_operacion:
			print('\t'*(nivel+1)+'- operacion: ',end="")
			print(op)
		else:
			self.imprimirArbol(nivel)
		return es_operacion

	#---------------------------------------------------------------------------
	# Imprimir_operacion()
	#
	# Imprime el tipo de operacion y los operadores izquierdo y derecho
	#---------------------------------------------------------------------------
	def Imprimir_operacion(self,nivel,imprimir=None):		
		es_operacion = self.imprimir_tipo_OP(nivel)
		n = 1
		for i in self.hijos:
			if n == 1 and es_operacion:
				print("\t"*(nivel+1)+"- operador izquierdo: ",end="")
				n+= 1
			elif n == 2 and es_operacion:
				print("\t"*(nivel+1)+"- operador derecho: ",end="")
			imprimir = True
			i.imprimirArbol(nivel+1,imprimir)	# Imprime el nodo de cada hijo
			i.Imprimir_variables_OP(nivel)

	#---------------------------------------------------------------------------
	# Imprimir_variables_OP()
	#
	# Si es una variable la imprime sin el prefijo "VAR"
	#---------------------------------------------------------------------------
	def Imprimir_variables_OP(self,nivel):
		for h in self.hijos:
			if self.es_arbol(h):
				if h.nombre == "VAR":
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
				if h.nombre == "VAR":
					print("\t"*(nivel+1)+"- var: ",end="")
					for i in h.hijos:
						print(i)
				
				elif h.nombre == "LISTA":
					h.Imprimir_variables(nivel)
				
				elif h.nombre in ["TRUE","FALSE"]:
					print(h.nombre)
			else:
				print("",h)

	#---------------------------------------------------------------------------
	# es_arbol()
	#
	# Verifica si el argumento h es un arbol
	#---------------------------------------------------------------------------
	def es_arbol(self,h):
		if type(h) in [arbol,expresion,instContr,instRobot]:
			return True
		return False

	#---------------------------------------------------------------------------
	# Verificar_secuenciacion()
	#
	# verifica si el ultimo hijo es una instruccion, si lo es lo 
	# considera una secuenciacion y si no se ha impreso aun, 
	# imprime SECUENCIACION
	#---------------------------------------------------------------------------
	def Verificar_secuenciacion(self,secuenciado,nivel):
		for i in self.hijos:					
			if  (self.es_arbol(i))\
			and (i.nombre == 'INST_CONT')\
			and (not (secuenciado)):		
				print('\t'*(nivel-1)+'SECUENCIACION')
				secuenciado = True
		return secuenciado

	#---------------------------------------------------------------------------
	# condicion_simple()
	#
	# Verifica si la condicion es una sola variable y la 
	# almacena si ese es el caso		
	# Si la condicion es una variable sola, la imprime
	#---------------------------------------------------------------------------
	def condicion_simple(self):
		expresion_sola = ''
		for i in self.hijos:
			if str(type(i)) == '<class \'Arbol.expresion\'>':
				if len(i.hijos) == 1:
					for j in i.hijos:
						if type(j) == expresion:
							for k in j.hijos:
								if not self.es_arbol(k):
									expresion_sola = str(k)
									break
						else:
							if not self.es_arbol(j):
								expresion_sola = str(j)
								break
		if expresion_sola != '':
			print(' '+expresion_sola)
		return expresion_sola

	#---------------------------------------------------------------------------
	# imprimirArbol()
	#
	# Imprime la estructura de arbol
	#---------------------------------------------------------------------------
	def imprimirArbol(self,nivel,imprimir=None,secuenciado=False):
		if self.nombre in ["INSTRUCCIONES_ROBOT","DECLARACION_ROBOT"]: 		# Si el nodo es una intruccion
			imprimir = False 						# robot se ignora
		elif self.nombre == "EXECUTE":				# Si el nodo es del tipo execute 
			imprimir = True 						# comienza a imprimir
		
		if imprimir:
			# Si es EXECUTE no lo imprime
			if self.nombre == "EXECUTE":
				 pass
			# Si es un literal booleano imprime su valor
			elif self.nombre in ["TRUE","FALSE"]:
				print("",self.nombre)

			# Si es ACTIVATE:
			# > imprime el tipo y la lista de variables que se activen
			elif self.nombre == 'ACTIVATE':
				secuenciado = self.Verificar_secuenciacion(secuenciado,nivel)
				print('\t'*nivel+'ACTIVACION')
				self.Imprimir_variables(nivel)

			# Si es DEACTIVATE:
			# > imprime el tipo y la lista de variables que se desactiven
			elif self.nombre == 'DEACTIVATE':
				secuenciado = self.Verificar_secuenciacion(secuenciado,nivel)
				print('\t'*nivel+'DESACTIVACION')	
				self.Imprimir_variables(nivel)		
			
			# Si es ADVANCE:
			# > imprime el "- exito: " seguido por el tipo y la lista de variables 
			#   que se activen
			elif self.nombre == 'ADVANCE':
				self.Verificar_secuenciacion(secuenciado,nivel)
				print('\t'*nivel+'-exito: AVANCE')
				self.Imprimir_variables(nivel)

			# Si es CONDICIONAL o CICLO:
			# > imprime el tipo y "- guardia: " esperando que lo proxima iteracion 
			#   imprima el tipo de guardia		
			elif self.nombre in ['CONDICIONAL','CICLO']:
				secuenciado = self.Verificar_secuenciacion(secuenciado,nivel)

				print('\t'*nivel+self.nombre)
				print('\t'*(nivel+1)+'- guardia:',end="")
				
				expresion_sola = self.condicion_simple()			

			# Si la expresion tiene un operador unario primero imprime el operador
			elif self.es_unario():
				if self.nombre == "NEGACION":
					print("~",end="")
				else:
					print("-",end="")
				self.Imprimir_operacion(nivel)
				imprimir= False
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
			elif self.nombre in 	["ENTERO", "BOOLEANO", "EXPRESION"]:
				imprimir = False				
				self.Imprimir_variables(nivel)
			
			#Si es un carcater lo imprime entre comillas
			elif self.nombre == "CARACTER":
				for i in self.hijos:
					print('\'',i,'\'')



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
	def __init__(self,nombre,hijos,linea=None,tipo=None):
		arbol.__init__(self,nombre,hijos)
		self.tipo = tipo
		self.valor = None
		self.linea = linea
	def setValor(self,valor):
		self.valor = valor
	def setTipo(self,tipo):
		self.tipo = tipo

# Instruccion del robot
class instContr(arbol):
	def __init__(self,nombre,hijos,linea=None):
		arbol.__init__(self,nombre,hijos)
		self.linea = linea

# Controlador
class instRobot(arbol):
	def __init__(self,nombre,hijos):
		arbol.__init__(self,nombre,hijos)

# Tipo de variables o robots
class defTipo(arbol):
	def __init__(self,nombre,hijos,tipo=None):
		arbol.__init__(self,nombre,hijos)
		self.tipo = tipo
