from Tabla import Tabla,tabla,datos
from Arbol import *
from Pila import *
import sys
pointer = tabla
p = pila()
bot = None # Variable "global" que guarda el robot actual al que se le esta aplicando
				 # una activacion, desactivacion, etc.
datos = None # Almacena los datos del robot actual
execute = False # Permite saber si una expresion esta en una seccion de execute o en un create
matriz = {}
ciclo = False
def ejecutar(arb,comportamiento=None): # comportamiento es el tipo de comportamiento que se quiere ejecutar
	global pointer,p,bot,datos,execute,ciclo
	if arb.nombre in ['INICIO','INSTRUCCIONES_ROBOT']:
		ejecutar(arb.hijos[0])

	elif arb.nombre == 'DECLARACION_ROBOT': # Se va directo al execute (no le interesa la seccion declare)
		if len(arb.hijos) == 5:
			ejecutar(arb.hijos[4])
		elif len(arb.hijos) == 6:
			ejecutar(arb.hijos[5])
		elif len(arb.hijos) == 4:
			ejecutar(arb.hijos[3])
	
	elif arb.nombre == 'EXECUTE':
		ejecutar(arb.hijos[0])
	
	elif arb.nombre in ['ACTIVATE','DEACTIVATE','ADVANCE']:
		robot = arb.hijos[0].hijos[0] # Actualiza la variable global bot con el robot que esta siendo activado
		bot = robot
		datos = pointer.buscarEnTodos(robot,'getDatos') # desactivado o avanzado
		ejecutar(datos.comportamientos,arb.nombre) # Pasa por parametro el tipo de comportamiento
		if len(arb.hijos) >= 2:					# para saber cual ejecutar de la lista de comport.
			if arb.hijos[1].nombre == 'LISTA':
				seguir = True
				robot = arb.hijos[1] # Recorre la lista de robots para ir activando cada uno
				bot = robot.hijos[0].hijos[0]
				while seguir:
					datos = pointer.buscarEnTodos(robot.hijos[0].hijos[0],'getDatos') # Busca el simbolo del ident de la lista
					ejecutar(datos.comportamientos,arb.nombre) # - datos.comportamientos es el nodo raiz de los 
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

	elif arb.nombre == 'CONDICIONAL':
		execute = True
		condicion = evaluar(arb.hijos[0])
		execute = False
		if type(condicion) == bool:
			if condicion: # Si se cumple la condicion del if
				ejecutar(arb.hijos[1].hijos[0])
			else: # Si no se cumple la condicion del if
				if arb.hijos[1].nombre == 'ELSE': # Si hay un else (si no hay, no se hace nada)
					ejecutar(arb.hijos[1].hijos[1])
			if len(arb.hijos) == 3: # Si hay mas instrucciones despues de terminar el if
				ejecutar(arb.hijos[2]) # Continua la ejecucion de las instrucciones despues del if	
		else:
			print("Error: La condicion del \"if\" debe ser de tipo booleano.")
			sys.exit()

	elif arb.nombre == 'INST_IF':
		ejecutar(arb.hijos[0])

	elif arb.nombre == 'ELSE':
		ejecutar(arb.hijos[0])

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
			print("Error: La guardia del ciclo debe ser de tipo booleano.")
			sys.exit()
		if len(arb.hijos) == 3:
			ejecutar(arb.hijos[2])


	elif arb.nombre == 'INST_CONT': # No borrar
		ejecutar(arb.hijos[0])

	elif arb.nombre == 'INC_ALCANCE':
		#if ciclo:
		#	pointer.reiniciar()
		p.addTope(pointer)
		pointer = arb.tabla
		ejecutar(arb.hijos[0])
		if len(arb.hijos) == 3:
			pointer.reiniciar()
			pointer = p.popTope()
			ejecutar(arb.hijos[2])
		else: # Quiza no hace falta porque si no hay mas instrucciones despues de una inc de alcance el programa termina
			pointer.reiniciar()
			pointer = p.popTope()

	elif arb.nombre == 'CONDICION': # Este es el nodo de la instruccion "on activation/deactivation..."
		if comportamiento == 'ACTIVATE':
			if datos.estado == 'activo': # PREGUNTAR: un robot puede activarse dos veces seguidas?
				print("Error: El robot \"%s\" ya fue activado."%(bot))
				sys.exit()
			#elif datos.estado == 'inactivo': # PREGUNTAR: un robot puede volverse a activar luego de ser desactivado?
			#	print("Error: El robot \"%s\" ya fue desactivado."%(bot))
			#	sys.exit()
			datos.estado = 'activo'

		elif comportamiento == 'DEACTIVATE':
			if datos.estado == 'inactivo':
				print("Error: el robot \"%s\" ya ha sido desactivado."%(bot))
				sys.exit()
			elif datos.estado in [None,'activacion','desactivacion']: # Se esta reusando datos.estado (activacion y
				print("Error: el robot \"%s\" no ha sido activado."%(bot)) # desactivacion son valores asignados en Tabla
				sys.exit()
			datos.estado = 'inactivo'

		elif comportamiento == 'ADVANCE':
			if datos.estado == 'inactivo':
				print("Error: el robot \"%s\" esta inactivo."%(bot))
				sys.exit()
			elif datos.estado in [None,'activacion','desactivacion']:
				print("Error: el robot \"%s\" no ha sido activado."%(bot))
				sys.exit()
		comp = datos.comportamientos # datos.comportamientos es un nodo, no un string como 'ACTIVACION'
		encontrado = False # Es true si se consigue el comportamiento que se desea ejecutar en el execute
		while not encontrado:   # del robot en la lista de comportamientos (busca el comportamiento q se quiere ej)
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
				else: # Si llega al ultimo nodo de comportamientos y no encontro el comportamiento buscado
					encontrado = False
					break
		if not encontrado:
			#if comportamiento == 'ACTIVATE':
			#	print("Error: el robot \"%s\" no posee un comportamiento \"activation\" en su lista para poder ser activado."%(bot))
			#	sys.exit()
			#elif comportamiento == 'DEACTIVATE':
			#	print("Error: el robot \"%s\" no posee el comportamiento \"deactivation\" en su lista para poder ser desactivado."%(bot))
			#	sys.exit()
			if comportamiento == 'ADVANCE': # era un elif
				print("Error: el robot \"%s\" no posee un comportamiento que permita avanzarlo."%(bot))
				sys.exit()
		else: # Si lo encontro, lo ejecuta
			ejecutar(comp.hijos[1])

	elif arb.nombre == 'STORE':
		if arb.hijos[0].nombre == 'CARACTER':
			resultado = evaluar(arb.hijos[0])
		else:
			resultado = evaluar(arb.hijos[0].hijos[0])
		if ((type(resultado) == bool and datos.tipo == 'bool') or # Estos tipos podrian mejorarse cambiando el parser.py y Tabla.py
			(type(resultado) == int and datos.tipo == 'int') or
			(type(resultado) == str and datos.tipo == 'char')):
			datos.tabla.tabla['me'].valor = resultado
		else:
			print("Error: El tipo de la expresion evaluada es distinto al tipo de \"%s\"."%(robot))
			sys.exit()
		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1])

	elif arb.nombre == 'COLLECT':
		objeto = None
		if datos.posicion in matriz:
			objeto = matriz[datos.posicion]
		else:
			print("Error: No existen elementos en la posicion [%s,%s] de la matriz."%(datos.posicion[0],datos.posicion[1]))
			sys.exit()
		if not ((type(objeto) == bool and datos.tipo == 'bool') or 
			(type(objeto) == int and datos.tipo == 'int') or
			(type(objeto) == str and datos.tipo == 'char')):
			print("Error: El tipo del elemento recolectado es distinto al tipo de \"%s\"."%(bot))
			sys.exit()
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
	
	elif arb.nombre == 'DROP':
		if arb.hijos[0].nombre == 'CARACTER':
			matriz[datos.posicion] = arb.hijos[0].hijos[0]
		else:
			resultado = evaluar(arb.hijos[0].hijos[0])
			matriz[datos.posicion] = resultado
		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1])

	elif arb.nombre == 'READ':
		while True:
			entrada = input("Introduzca un valor: ") # Esto se puede quitar, porque los lenguajes no ponen mensajes
													 # por defecto en los inputs
			try:
				if datos.tipo == 'int':
					entrada = int(entrada)
				elif datos.tipo == 'char':
					pass # No se cambia el tipo, ya que por defecto es string
				elif datos.tipo == 'bool':
					if entrada in ['True','TRUE','true']:
						entrada = True
					elif entrada in ['False','FALSE','false']:
						entrada = False
				if not((type(entrada) == bool and datos.tipo == 'bool') or # Estos tipos podrian mejorarse cambiando el parser.py y Tabla.py
					(type(entrada) == int and datos.tipo == 'int') or
					(type(entrada) == str and datos.tipo == 'char')):
					print("Error: Conflicto entre el tipo del robot y el valor ingresado.")
					print()
				else:
					break
			except:
				print("Error: Conflicto entre el tipo del robot y el valor ingresado.")
				print()
		if len(arb.hijos[0].hijos) == 1:
			datos.tabla.tabla[arb.hijos[0].hijos[0].hijos[0]].valor = entrada
		else:
			datos.tabla.tabla['me'].valor = entrada
		
		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1]) 

	elif arb.nombre == 'SEND':
		print(datos.tabla.tabla['me'].valor) # No borrar
		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1]) 
	
	elif arb.nombre == 'DIRECCION':
		(x,y) = datos.posicion
		if len(arb.hijos) == 1:
			if arb.hijos[0].nombre == 'UP':
				datos.posicion = (x,y+1)
			elif arb.hijos[0].nombre == 'DOWN':
				datos.posicion = (x,y-1)
			elif arb.hijos[0].nombre == 'RIGHT':
				datos.posicion = (x+1,y)
			elif arb.hijos[0].nombre == 'LEFT':
				datos.posicion = (x-1,y)
		elif len(arb.hijos) == 2:
			if arb.hijos[1].nombre == 'INST_ROBOT':
				if arb.hijos[0].nombre == 'UP':
					datos.posicion = (x,y+1)
				elif arb.hijos[0].nombre == 'DOWN':
					datos.posicion = (x,y-1)
				elif arb.hijos[0].nombre == 'RIGHT':
					datos.posicion = (x+1,y)
				elif arb.hijos[0].nombre == 'LEFT':
					datos.posicion = (x-1,y)
				ejecutar(arb.hijos[1])
			else:
				resultado = evaluar(arb.hijos[1])
				if type(resultado) == int:
					if resultado >= 0:
						if arb.hijos[0].nombre == 'UP':
							datos.posicion = (x,y+resultado)
						elif arb.hijos[0].nombre == 'DOWN':
							datos.posicion = (x,y-resultado)
						elif arb.hijos[0].nombre == 'RIGHT':
							datos.posicion = (x+resultado,y)
						elif arb.hijos[0].nombre == 'LEFT':
							datos.posicion = (x-resultado,y)
					else:
						print("Error: No se puede mover el robot %s un numero negativo de espacios."%(bot))
						sys.exit()
				else:
					print("Error: El numero de espacios debe ser un entero para mover a %s."%(bot))
					sys.exit()
		else:
			resultado = evaluar(arb.hijos[1])
			if type(resultado) == int:
				if resultado >= 0:
					if arb.hijos[0].nombre == 'UP':
						datos.posicion = (x,y+resultado)
					elif arb.hijos[0].nombre == 'DOWN':
						datos.posicion = (x,y-resultado)
					elif arb.hijos[0].nombre == 'RIGHT':
						datos.posicion = (x+resultado,y)
					elif arb.hijos[0].nombre == 'LEFT':
						datos.posicion = (x-resultado,y)
				else:
					print("Error: No se puede mover el robot %s un numero negativo de espacios."%(bot))
					sys.exit()
			else:
				print("Error: El numero de espacios debe ser un entero para mover a %s."%(bot))
				sys.exit()
			ejecutar(arb.hijos[2])

	elif arb.nombre == 'ON_EXPRESION':
		condicion = evaluar(arb.hijos[0],robot) # Se le pasa el nombre del robot para que evalue el comportamiento 
		if type(condicion) == bool:				# del robot correcto y no de cualquier robot con el mismo comportamiento
			if condicion:
				pass
		else:
			print("Error: La condicion del comportamiento debe ser de tipo booleano.")
			sys.exit()

	elif arb.nombre == 'INST_ROBOT': # Para seguir ejecutando el arbol cuando hay varias instrucciones de robot seguidas
		ejecutar(arb.hijos[0])

def evaluar(arb): # Tabla es la tabla de simbolos global donde se sacaran valores de variables
	global bot,execute
	if arb.nombre == 'CONJUNCION':
		return evaluar(arb.hijos[0]) and evaluar(arb.hijos[1])
	
	elif arb.nombre == 'DISYUNCION':
		return evaluar(arb.hijos[0]) or evaluar(arb.hijos[1])
	
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
	
	elif arb.nombre == 'SUMA':
		return evaluar(arb.hijos[0]) + evaluar(arb.hijos[1])
	
	elif arb.nombre == 'RESTA':
		return evaluar(arb.hijos[0]) - evaluar(arb.hijos[1])
	
	elif arb.nombre == 'MULTIPLICACION':
		return evaluar(arb.hijos[0]) * evaluar(arb.hijos[1])
	
	elif arb.nombre == 'DIVISION':
		a = evaluar(arb.hijos[0])
		b = evaluar(arb.hijos[1])
		if b!=0:
			return evaluar(arb.hijos[0]) / evaluar(arb.hijos[1])
		else:
			print("Error: No es posible dividir por cero.")

	elif arb.nombre == 'MODULO':
		a = evaluar(arb.hijos[0])
		b = evaluar(arb.hijos[1])
		if b!=0:
			return evaluar(arb.hijos[0]) % evaluar(arb.hijos[1])
		else:
			print("Error: No es posible obtener el modulo por cero.")
			
	elif arb.nombre == 'PARENTESIS':
		return evaluar(arb.hijos[0])

	elif arb.nombre == 'NEGACION':
		return not evaluar(arb.hijos[0])
	
	elif arb.nombre == 'NEGATIVO':
		return - evaluar(arb.hijos[0])
	
	elif arb.nombre == 'ENTERO': # Los enteros ya vienen casteados del Lexer
		return arb.hijos[0]
	
	elif arb.nombre == 'CARACTER':
		return arb.hijos[0]
	
	elif arb.nombre == 'BOOLEANO':
		if arb.hijos[0].hijos[0] == 'true':
			return True
		elif arb.hijos[0].hijos[0] == 'false':
			return False

	elif arb.nombre == 'VAR':
		datos = pointer.fetch(arb.hijos[0],bot,execute)
		if execute:
			val = datos.tabla.tabla['me'].valor
			if val != None:
				return val  # tabla.tabla la primera tabla es una clase tabla, la segunda
							# es un atributo de la clase tabla (un diccionario)
			else: # Si el robot no tenia un valor (no estaba inicializado) se da error
				print("Error: El robot %s no ha sido inicializado."%(bot))
				sys.exit()
		else:
			val = datos.valor
			if val != None:
				return val
			else: # Si la variable no tenia un valor (no estaba inicializada) se da error
				print("Error: La variable %s no ha sido inicializada."%(arb.hijos[0]))
				sys.exit()