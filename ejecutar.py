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
matriz = None 
def ejecutar(arb,comportamiento=None): # comportamiento es el tipo de comportamiento que se quiere ejecutar
	global pointer,p,bot,datos,execute
	if arb.nombre in ['INICIO','INSTRUCCIONES_ROBOT']:
		ejecutar(arb.hijos[0])
	elif arb.nombre == 'DECLARACION_ROBOT': # Se va directo al execute (no le interesa la seccion declare)
		if len(arb.hijos) == 5:
			ejecutar(arb.hijos[4])
		elif len(arb.hijos) == 6:
			ejecutar(arb.hijos[5])
	
	elif arb.nombre == 'EXECUTE':
		ejecutar(arb.hijos[0])
	
	elif arb.nombre in ['ACTIVATE','DEACTIVATE','ADVANCE']:
		robot = arb.hijos[0].hijos[0] # Actualiza la variable global bot con el robot que esta siendo activado
		bot = robot
		#print("NOMBRE",arb.nombre)
		#print("ROBOT",bot)
		datos = pointer.buscarEnTodos(robot,'getDatos') # desactivado o avanzado
		ejecutar(datos.comportamientos,arb.nombre) # Pasa por parametro el tipo de comportamiento
		if len(arb.hijos) >= 2:					# para saber cual ejecutar de la lista de comport.
			if arb.hijos[1].nombre == 'LISTA':
				seguir = True
				robot = arb.hijos[1] # Recorre la lista de robots para ir activando cada uno
				bot = robot.hijos[0].hijos[0]
				#print("ROBOT",bot)
				while seguir:
					datos = pointer.buscarEnTodos(robot.hijos[0].hijos[0],'getDatos') # Busca el simbolo del ident de la lista
					datos.estado = None
					ejecutar(datos.comportamientos,arb.nombre) # - datos.comportamientos es el nodo raiz de los 
															   # comportamientos del robot que esta siendo
															   # desactivado/activado/avanzado
															   # - arb.nombre es el nombre del comportamiento 
															   # que se va a ejecutar de ese arbol de comportamientos
					if len(robot.hijos) == 2:
						robot = robot.hijos[1]
						bot = robot.hijos[0].hijos[0]
						#print("ROBOT",bot)
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
				ejecutar(arb.hijos[1])
				condicion = evaluar(arb.hijos[0])
		else:
			print("Error: La guardia del ciclo debe ser de tipo booleano.")
			sys.exit()
		if len(arb.hijos) == 3:
			ejecutar(arb.hijos[2])

	elif arb.nombre == 'INST_CONT': # No borrar
		ejecutar(arb.hijos[0])

	elif arb.nombre == 'INC_ALCANCE':
		p.addTope(pointer)
		pointer = arb.tabla
		ejecutar(arb.hijos[0])
		if len(arb.hijos) == 3:
			pointer = p.popTope()
			ejecutar(arb.hijos[2])
		else: # Quiza no hace falta porque si no hay mas instrucciones despues de una inc de alcance el programa termina
			pointer = p.popTope()

	elif arb.nombre == 'CONDICION': # Este es el nodo de la instruccion "on activation/deactivation..."
		if comportamiento == 'ACTIVATE':
			if datos.estado == 'activo': # PREGUNTAR: un robot puede activarse dos veces seguidas?
				print("Error: El robot \"%s\" ya fue activado."%(bot))
			elif datos.estado == 'inactivo': # PREGUNTAR: un robot puede volverse a activar luego de ser desactivado?
				print("Error: El robot \"%s\" ya fue desactivado."%(bot))
			datos.estado = 'activo'

		elif comportamiento == 'DEACTIVATE':
			if datos.estado == 'inactivo':
				print("Error: el robot \"%s\" ya ha sido desactivado."%(bot))
			elif datos.estado in [None,'activacion','desactivacion']: # Se esta reusando datos.estado (activacion y
				print("Error: el robot \"%s\" no ha sido activado."%(bot)) # desactivacion son valores asignados en Tabla
			datos.estado = 'inactivo'

		elif comportamiento == 'ADVANCE':
			if datos.estado == 'inactivo':
				print("Error: el robot \"%s\" esta inactivo."%(bot))
			elif datos.estado in [None,'activacion','desactivacion']:
				print("Error: el robot \"%s\" no ha sido activado."%(bot))

		comp = datos.comportamientos # datos.comportamientos es un nodo, no un string como 'ACTIVACION'
		print(comportamiento)
		encontrado = False # Es true si se consigue el comportamiento que se desea ejecutar en el execute
		while not encontrado:   # del robot en la lista de comportamientos (busca el comportamiento q se quiere ej)
			if (comp.hijos[0].nombre == 'ON_EXPRESION' and comportamiento == 'ADVANCE'):
				print(evaluar(comp.hijos[0].hijos[0]))

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
			if comportamiento == 'ACTIVATE':
				print("Error: el robot \"%s\" no posee un comportamiento \"activation\" en su lista para poder ser activado."%(bot))
			elif comportamiento == 'DEACTIVATE':
				print("Error: el robot \"%s\" no posee el comportamiento \"deactivation\" en su lista para poder ser desactivado."%(bot))
			elif comportamiento == 'ADVANCE':
				print("Error: el robot \"%s\" no posee un comportamiento que permita avanzarlo."%(bot))
		else: # Si lo encontro, lo ejecuta
			ejecutar(comp.hijos[1])

	elif arb.nombre == 'STORE':
		if arb.hijos[0].nombre == 'CARACTER':
			resultado = evaluar(arb.hijos[0].hijos[0])
		else:
			resultado = evaluar(arb.hijos[0].hijos[0])
		if ((type(resultado) == bool and datos.tipo == 'bool') or # Estos tipos podrian mejorarse cambiando el parser.py y Tabla.py
			(type(resultado) == int and datos.tipo == 'int') or
			(type(resultado) == str and datos.tipo == 'char')):
			datos.tabla.tabla['me'].valor = resultado
		else:
			print("Error: El tipo de la expresion evaluada es distinto al tipo del robot.")
			sys.exit()
		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1])
		print("POINTER_a",pointer.tabla['a'].tabla.tabla['me'].valor)
		print("POINTER_v",pointer.tabla['v'].tabla.tabla['me'].valor)
		print("POINTER_b",pointer.tabla['b'].tabla.tabla['me'].valor)

	elif arb.nombre == 'COLLECT':
		pass
		#ejecutar(arb.hijos[1]) # Acordarse de poner esto para seguir ejecutanto las siguientes instrucciones del robot
	
	elif arb.nombre == 'DROP':
		pass
		#ejecutar(arb.hijos[1]) # Acordarse de poner esto para seguir ejecutanto las siguientes instrucciones del robot
	
	elif arb.nombre == 'READ':
		entrada = input("Introduzca un valor: ")
		opcion = None
		while True:
			print()
			print("Por favor seleccione el tipo del valor que introdujo anteriormente:")
			opcion = input("1: Entero \n2: Caracter \n3: Booleano\n--> ")
			if opcion in ['1','2','3']:
				break
			else:
				print("Error: Por favor introduzca una opcion correcta")
		try:
			if opcion == '1':
				entrada = int(entrada)
			elif opcion == '2':
				pass # No se cambia el tipo, ya que por defecto es string
			elif opcion == '3':
				if entrada in ['True','TRUE','true']:
					entrada = True
				elif entrada in ['False','FALSE','false']:
					entrada = False
		except:
			print("Error: El tipo ingresado no se corresponde con el del valor dado.")
			sys.exit()
		if not((type(entrada) == bool and datos.tipo == 'bool') or # Estos tipos podrian mejorarse cambiando el parser.py y Tabla.py
			(type(entrada) == int and datos.tipo == 'int') or
			(type(entrada) == str and datos.tipo == 'char')):
			print("El valor introducido no coincide con el tipo del robot.")
			sys.exit()
		if len(arb.hijos[0].hijos) == 1:
			datos.tabla.tabla[arb.hijos[0].hijos[0].hijos[0]].valor = entrada
		else:
			datos.tabla.tabla['me'].valor = entrada
		
		print(pointer.tabla[bot].tabla.tabla['me'].valor)
		if len(arb.hijos) == 2:
			ejecutar(arb.hijos[1]) 
	elif arb.nombre == 'SEND':
		pass
		#ejecutar(arb.hijos[1]) # Acordarse de poner esto para seguir ejecutanto las siguientes instrucciones del robot
	
	elif arb.nombre == 'RECIEVE':
		pass
		#ejecutar(arb.hijos[1]) # Acordarse de poner esto para seguir ejecutanto las siguientes instrucciones del robot
	
	elif arb.nombre == 'DIRECCION':
		pass
		#ejecutar(arb.hijos[1]) # Acordarse de poner esto para seguir ejecutanto las siguientes instrucciones del robot

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
		return evaluar(arb.hijos[0]) / evaluar(arb.hijos[1])
	
	elif arb.nombre == 'MODULO':
		return evaluar(arb.hijos[0]) % evaluar(arb.hijos[1])
	
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
		#print("POINTER",pointer.tabla)
		#print("BOT",bot)
		#print(pointer[bot])
		datos = pointer.fetch(arb.hijos[0],bot,execute)
		if execute:
			return datos.tabla.tabla['me'].datos.valor  # tabla.tabla la primera tabla es una clase tabla, la segunda
														# es un atributo de la clase tabla (un diccionario)
		else:
			return datos.valor # Revisar