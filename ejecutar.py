#-------------------------------------------------------------------------------
#							    EJECUTAR
#-------------------------------------------------------------------------------

from Tabla import Tabla,tabla,datos
from Arbol import *
from Pila import *
from errores import *
import sys

pointer = tabla
p = pila()
bot = None 			# Variable "global" que guarda el robot actual al que se le esta aplicando
					# una activacion, desactivacion, etc.
datos = None 		# Almacena los datos del robot actual
execute = False 	# Permite saber si una expresion esta en una seccion de execute o en un create
matriz = {} 
ciclo = False

#---------------------------------------------------------------------------
# mover_en_direccion()
#
# funcion que meuve a un bot segun la direccion indicada
#---------------------------------------------------------------------------
def mover_en_direccion(arb,datos,x,y):		
	x,y = datos.posicion
	if arb.hijos[0].nombre == 'UP':
		datos.posicion = (x,y+1)
	elif arb.hijos[0].nombre == 'DOWN':
		datos.posicion = (x,y-1)
	elif arb.hijos[0].nombre == 'RIGHT':
		datos.posicion = (x+1,y)
	elif arb.hijos[0].nombre == 'LEFT':
		datos.posicion = (x-1,y)
	return datos.posicion

#---------------------------------------------------------------------------
# send()
#
# funcion que imprime el contenido del bot
#---------------------------------------------------------------------------
def send(dato):
	if dato == '\\n':
		print()
	elif dato == '\\t':
		print('\t',end='')
	else:
		print(dato,end ='') # No borrar

#---------------------------------------------------------------------------
# ejecutar()
#
# Funcion donde se ejecuta el argumento pasado a ./bot
#---------------------------------------------------------------------------
def ejecutar(arb,comportamiento=None): 							# comportamiento es el tipo de comportamiento que se quiere ejecutar
	global pointer,p,bot,datos,execute,ciclo
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion INICIO, EXECUTE, ELSE, INST_CONT, 
	#  INST_ROBOT, INST_IF, INSTRUCCIONES_ROBOT
	#  (Se agrega INST_ROBOT para seguir ejecutando el arbol cuando hay varias 
	#  instrucciones de robot seguidas)
	#---------------------------------------------------------------------------
	if arb.nombre in  ['INICIO','EXECUTE','ELSE','INST_CONT','INST_ROBOT','INST_IF','INSTRUCCIONES_ROBOT']:
		ejecutar(arb.hijos[0])
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion DECLARACION_ROBOT
	#---------------------------------------------------------------------------
	elif arb.nombre == 'DECLARACION_ROBOT': 					# Se va directo al execute (no le interesa la seccion declare)
		if len(arb.hijos) == 5:
			ejecutar(arb.hijos[4])
		elif len(arb.hijos) == 6:
			ejecutar(arb.hijos[5])
		elif len(arb.hijos) == 4:
			ejecutar(arb.hijos[3])
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion ACTIVATE, DEACTIVATE ADVANCE
	#---------------------------------------------------------------------------	
	elif arb.nombre in ['ACTIVATE','DEACTIVATE','ADVANCE']:
		robot = arb.hijos[0].hijos[0] 							# Actualiza la variable global bot con el robot que esta 
																# siendo activado
		bot = robot
		datos = pointer.buscarEnTodos(robot,'getDatos') 		# desactivado o avanzado
		ejecutar(datos.comportamientos,arb.nombre) 				# Pasa por parametro el tipo de comportamiento
		if len(arb.hijos) >= 2:									# para saber cual ejecutar de la lista de comport.
			if arb.hijos[1].nombre == 'LISTA':
				seguir = True
				robot = arb.hijos[1] 							# Recorre la lista de robots para ir activando cada uno
				bot = robot.hijos[0].hijos[0]
				while seguir:
					datos = pointer.buscarEnTodos(robot.hijos[0].hijos[0],'getDatos') 	# Busca el simbolo del ident de 
																						# la lista
					
					ejecutar(datos.comportamientos,arb.nombre) 							# - datos.comportamientos es el nodo raiz de los 
															   							# comportamientos del robot que esta siendo
															   							# desactivado/activado/avanzado
															   							# - arb.nombre es el nombre del comportamiento 
															   							# que se va a ejecutar de ese arbol de comportamientos
					if len(robot.hijos) == 2:
						robot = robot.hijos[1]
						bot = robot.hijos[0].hijos[0]
					else:
						seguir = False
			else:
				ejecutar(arb.hijos[1])
			
			if len(arb.hijos) == 3:
				ejecutar(arb.hijos[2])
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion CONDICIONAL
	#---------------------------------------------------------------------------
	elif arb.nombre == 'CONDICIONAL':
		execute = True
		condicion = evaluar(arb.hijos[0])
		execute = False
		if type(condicion) == bool:
			if condicion: 										# Si se cumple la condicion del if
				ejecutar(arb.hijos[1].hijos[0])
			else: 												# Si no se cumple la condicion del if
				if arb.hijos[1].nombre == 'ELSE': 				# Si hay un else (si no hay, no se hace nada)
					ejecutar(arb.hijos[1].hijos[1])
			if len(arb.hijos) == 3: 							# Si hay mas instrucciones despues de terminar el if
				ejecutar(arb.hijos[2]) 							# Continua la ejecucion de las instrucciones despues del if	
		else:
			error_ejecucion(1,None,None,arb.hijos[0].linea)
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion CICLO
	#---------------------------------------------------------------------------
	elif arb.nombre == 'CICLO':
		execute = True
		condicion = evaluar(arb.hijos[0])
		execute = False
		if type(condicion) == bool:
			while condicion:
				ciclo = True
				ejecutar(arb.hijos[1])
				execute = True
				condicion = evaluar(arb.hijos[0])
				execute = False
				ciclo = False
		else:
			error_ejecucion(2,None,None,arb.hijos[0].linea)

		if len(arb.hijos) == 3:
			ejecutar(arb.hijos[2])
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion INC_ALCANCE
	#---------------------------------------------------------------------------
	elif arb.nombre == 'INC_ALCANCE':
		p.addTope(pointer)
		pointer = arb.tabla
		ejecutar(arb.hijos[0])
		if len(arb.hijos) == 3:
			pointer.reiniciar()
			pointer = p.popTope()
			ejecutar(arb.hijos[2])
		else:
			pointer.reiniciar()
			pointer = p.popTope()
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion CONDICION
	#---------------------------------------------------------------------------
	elif arb.nombre == 'CONDICION': 				# Este es el nodo de la instruccion "on < condicion >"
		#---------------------------------------------------------------------------
		#  Comportamiento del comportamiento ACTIVATE
		#---------------------------------------------------------------------------
		if comportamiento == 'ACTIVATE':
			if datos.estado == 'activo':
				error_ejecucion(3,bot)
			
			datos.estado = 'activo'
		#---------------------------------------------------------------------------
		#  Comportamiento del comportamiento DEACTIVATE
		#---------------------------------------------------------------------------
		elif comportamiento == 'DEACTIVATE':
			if datos.estado == 'inactivo':
				error_ejecucion(4,bot,None,arb.hijos[0].linea)

			elif datos.estado in [None,'activacion','desactivacion']: 	# Se esta reusando datos.estado (activacion y
				error_ejecucion(5,bot,None,arb.hijos[0].linea)									# desactivacion son valores asignados en Tabla)

			datos.estado = 'inactivo'
		#---------------------------------------------------------------------------
		#  Comportamiento del comportamiento ADVANCE
		#---------------------------------------------------------------------------
		elif comportamiento == 'ADVANCE':
			if datos.estado == 'inactivo':
				error_ejecucion(5,bot,None,arb.hijos[0].linea)

			elif datos.estado in [None,'activacion','desactivacion']:
				error_ejecucion(8,bot,None,arb.hijos[0].linea)

		comp = datos.comportamientos 	# datos.comportamientos es un nodo, no un string como 'ACTIVACION'
		encontrado = False 				# Es true si se consigue el comportamiento que se desea ejecutar en el execute
		#---------------------------------------------------------------------------
		#  Busca el comportamiento en la lista de comportamientos del bot
		#---------------------------------------------------------------------------		
		while not encontrado:   		# del robot en la lista de comportamientos (busca el comportamiento q se quiere ej)
			if comp.hijos[0].nombre == 'ACTIVACION' and comportamiento == 'ACTIVATE': 
				encontrado = True

			elif comp.hijos[0].nombre == 'DESACTIVACION' and comportamiento == 'DEACTIVATE':
				encontrado = True

			elif (comp.hijos[0].nombre == 'ON_EXPRESION' and comportamiento == 'ADVANCE' and
															evaluar(comp.hijos[0].hijos[0])):
				encontrado = True
			elif comp.hijos[0].nombre == 'DEFAULT' and comportamiento == 'ADVANCE':
				encontrado = True

			else:
				if len(comp.hijos) == 4:
					comp = comp.hijos[3]
				else: 					# Si llega al ultimo nodo de comportamientos y no encontro el comportamiento buscado
					encontrado = False
					break
		
		if not encontrado:
			if comportamiento == 'ADVANCE':
				error_ejecucion(10,bot,None,arb.hijos[0].linea)

		else: 							# Si lo encontro, lo ejecuta
			ejecutar(comp.hijos[1])
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion STORE
	#---------------------------------------------------------------------------
	elif arb.nombre == 'STORE':
		if arb.hijos[0].nombre == 'CARACTER':
			resultado = evaluar(arb.hijos[0])
		else:
			resultado = evaluar(arb.hijos[0].hijos[0])
		if ((type(resultado) == bool and datos.tipo == 'bool') or 
			(type(resultado) == int and datos.tipo == 'int') or
			(type(resultado) == str and datos.tipo == 'char')):
			datos.tabla.tabla['me'].valor = resultado
		else:
			error_ejecucion(12,bot)

		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1])
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion COLLECT
	#---------------------------------------------------------------------------
	elif arb.nombre == 'COLLECT':
		objeto = None
		if datos.posicion in matriz:
			objeto = matriz[datos.posicion]
		else:
			print('~',arb.hijos[0].linea,'~')
			error_ejecucion(11,None,datos)

		if not ((type(objeto) == bool and datos.tipo == 'bool') or 
			(type(objeto) == int and datos.tipo == 'int') or
			(type(objeto) == str and datos.tipo == 'char')):
			error_ejecucion(13,bot)

		if len(arb.hijos) == 0:
			datos.tabla.tabla['me'].valor = objeto
		elif len(arb.hijos) == 1:
			if arb.hijos[0].nombre == 'COLLECT_AS':
				datos.tabla.tabla[arb.hijos[0].hijos[0].hijos[0]].valor = objeto
			else:
				datos.tabla.tabla['me'].valor = objeto
				ejecutar(arb.hijos[0])
		else:
			datos.tabla.tabla[arb.hijos[0].hijos[0].hijos[0]].valor = objeto
			ejecutar(arb.hijos[1])
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion DROP
	#---------------------------------------------------------------------------	
	elif arb.nombre == 'DROP':
		if arb.hijos[0].nombre == 'CARACTER':
			matriz[datos.posicion] = arb.hijos[0].hijos[0]
		else:
			resultado = evaluar(arb.hijos[0].hijos[0])
			matriz[datos.posicion] = resultado
		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1])
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion READ
	#---------------------------------------------------------------------------
	elif arb.nombre == 'READ':
		while True:
			entrada = input('>')
			try:
				if datos.tipo == 'int':
					entrada = int(entrada)
				elif datos.tipo == 'char':
					pass 					# No se cambia el tipo, ya que por defecto es string
				
				elif datos.tipo == 'bool':
					if entrada in ['True','TRUE','true']:
						entrada = True
					elif entrada in ['False','FALSE','false']:
						entrada = False
				
				if not((type(entrada) == bool and datos.tipo == 'bool') or
					(type(entrada) == int and datos.tipo == 'int') or
					(type(entrada) == str and datos.tipo == 'char')):
					error_conflicto(1)
				else:
					break
			except:
				error_conflicto(1)

		if len(arb.hijos[0].hijos) == 1:
			datos.tabla.tabla[arb.hijos[0].hijos[0].hijos[0]].valor = entrada
		else:
			datos.tabla.tabla['me'].valor = entrada
		
		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1]) 
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion SEND
	#---------------------------------------------------------------------------
	elif arb.nombre == 'SEND':
		send(datos.tabla.tabla['me'].valor)

		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1]) 
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion DIRECCION
	#---------------------------------------------------------------------------	
	elif arb.nombre == 'DIRECCION':
		(x,y) = datos.posicion
		if len(arb.hijos) == 1:
			datos.posicion = mover_en_direccion(arb,datos,x,y)
		elif len(arb.hijos) == 2:
			if arb.hijos[1].nombre == 'INST_ROBOT':
				datos.posicion = mover_en_direccion(arb,datos,x,y)
				ejecutar(arb.hijos[1])
			else:
				resultado = evaluar(arb.hijos[1])
				if type(resultado) == int:
					if resultado >= 0:
						datos.posicion = mover_en_direccion(arb,datos,x,y)
					else:
						error_ejecucion(14,bot)
				else:
					error_ejecucion(7,bot)
		else:
			resultado = evaluar(arb.hijos[1])
			if type(resultado) == int:
				if resultado >= 0:
					datos.posicion = mover_en_direccion(arb,datos,x,y)
				else:
					error_ejecucion(14,bot)
			else:
				error_ejecucion(14,bot)
			ejecutar(arb.hijos[2])
	#---------------------------------------------------------------------------
	#  Comportamiento de la instruccion ON_EXPRESION
	#---------------------------------------------------------------------------
	elif arb.nombre == 'ON_EXPRESION':
		condicion = evaluar(arb.hijos[0],robot) # Se le pasa el nombre del robot para que evalue el comportamiento 
		if type(condicion) == bool:				# del robot correcto y no de cualquier robot con el mismo comportamiento
			if condicion:
				pass
		else:
			error_ejecucion(6)

#---------------------------------------------------------------------------
# evaluar()
#
# Dado un arbol, evalua las expresiones que contiene
#---------------------------------------------------------------------------
def evaluar(arb):
	global bot,execute
	#---------------------------------------------------------------------------
	#  Evalua operadores booleanos
	#---------------------------------------------------------------------------
	if arb.nombre == 'CONJUNCION':
		return evaluar(arb.hijos[0]) and evaluar(arb.hijos[1])
	elif arb.nombre == 'DISYUNCION':
		return evaluar(arb.hijos[0]) or evaluar(arb.hijos[1])
	
	#---------------------------------------------------------------------------
	#  Evalua operadores relacionales
	#---------------------------------------------------------------------------	
	elif arb.nombre == 'IGUALDAD':
		return evaluar(arb.hijos[0]) == evaluar(arb.hijos[1])
	elif arb.nombre == 'DISTINTO':
		return evaluar(arb.hijos[0]) != evaluar(arb.hijos[1])
	elif arb.nombre == 'MENOR_QUE':
		return evaluar(arb.hijos[0]) < evaluar(arb.hijos[1])
	elif arb.nombre == 'MENOR_IGUAL':
		return evaluar(arb.hijos[0]) <= evaluar(arb.hijos[1])
	elif arb.nombre == 'MAYOR':
		return evaluar(arb.hijos[0]) > evaluar(arb.hijos[1])
	elif arb.nombre == 'MENOR_IGUAL':
		return evaluar(arb.hijos[0]) >= evaluar(arb.hijos[1])
	
	#---------------------------------------------------------------------------
	#  Evalua operadores aritmeticos
	#---------------------------------------------------------------------------	
	elif arb.nombre == 'SUMA':
		return evaluar(arb.hijos[0]) + evaluar(arb.hijos[1])
	elif arb.nombre == 'RESTA':
		return evaluar(arb.hijos[0]) - evaluar(arb.hijos[1])
	elif arb.nombre == 'MULTIPLICACION':
		print('~',arb.hijos[0].linea,'~')
		return evaluar(arb.hijos[0]) * evaluar(arb.hijos[1])
	elif arb.nombre == 'DIVISION':
		a = evaluar(arb.hijos[0])
		b = evaluar(arb.hijos[1])
		if b!=0:
			return evaluar(arb.hijos[0]) / evaluar(arb.hijos[1])
		else:
			error_conflicto(2)
	elif arb.nombre == 'MODULO':
		a = evaluar(arb.hijos[0])
		b = evaluar(arb.hijos[1])
		if b!=0:
			return evaluar(arb.hijos[0]) % evaluar(arb.hijos[1])
		else:
			error_conflicto(3)
			
	elif arb.nombre == 'PARENTESIS':
		return evaluar(arb.hijos[0])
	#---------------------------------------------------------------------------
	#  Evalua operadores unarios
	#---------------------------------------------------------------------------
	elif arb.nombre == 'NEGACION':
		return not evaluar(arb.hijos[0])
	
	elif arb.nombre == 'NEGATIVO':
		return - evaluar(arb.hijos[0])
	#---------------------------------------------------------------------------
	#  Evalua literales enteros
	#---------------------------------------------------------------------------		
	elif arb.nombre == 'ENTERO': # Los enteros ya vienen casteados del Lexer
		return arb.hijos[0]
	#---------------------------------------------------------------------------
	#  Evalua literales para caracteres
	#---------------------------------------------------------------------------		
	elif arb.nombre == 'CARACTER':
		return arb.hijos[0]
	#---------------------------------------------------------------------------
	#  Evalua literales boleanos
	#---------------------------------------------------------------------------	
	elif arb.nombre == 'BOOLEANO':
		if arb.hijos[0].hijos[0] == 'true':
			return True
		elif arb.hijos[0].hijos[0] == 'false':
			return False

	#---------------------------------------------------------------------------
	#  Evalua las variables
	#---------------------------------------------------------------------------	
	elif arb.nombre == 'VAR':
		datos = pointer.fetch(arb.hijos[0],bot,execute)
		if execute:
			val = datos.tabla.tabla['me'].valor
			if val != None:
				return val  # tabla.tabla la primera tabla es una clase tabla, la segunda
							# es un atributo de la clase tabla (un diccionario)
			else: 			# Si el robot no tenia un valor (no estaba inicializado) se da error
				error_ejecucion(9,bot)
		else:
			val = datos.valor
			if val != None:
				return val
			else: 			# Si la variable no tenia un valor (no estaba inicializada) se da error
				error_conflicto(4,arb)
