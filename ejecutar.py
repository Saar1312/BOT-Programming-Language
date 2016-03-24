from Tabla import Tabla,tabla,datos
from Arbol import *
from Pila import *
import sys
pointer = tabla
p = pila()
bot = None # Variable "global" que guarda el robot actual al que se le esta aplicando
				 # una activacion, desactivacion, etc.
datos = None # Almacena los datos del robot actual

def ejecutar(arb,comportamiento=None): # comportamiento es el tipo de comportamiento que se quiere ejecutar
	global pointer,p,bot,datos
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
		robot = arb.hijos[0].hijos[0] # Actualiza la variable global robot con el robot que esta siendo activado
		bot = robot
		datos = pointer.buscarEnTodos(robot,'getDatos') # desactivado o avanzado
		datos.estado = None
		ejecutar(datos.comportamientos,arb.nombre) # Pasa por parametro el tipo de comportamiento
		
		if len(arb.hijos) >= 2:					# para saber cual ejecutar de la lista de comport.
			if arb.hijos[1].nombre == 'LISTA':
				seguir = True
				robot = arb.hijos[1] # Recorre la lista de robots para ir activando cada uno
				bot = robot.hijos[0]
				while seguir:
					datos = pointer.buscarEnTodos(robot.hijos[0].hijos[0],'getDatos') # Busca el simbolo del ident de la lista
					datos.estado = None
					ejecutar(datos.comportamientos,arb.nombre) # datos.comportamientos es el nodo raiz de los 
															   # comportamientos del del robot que esta siendo
															   # desactivado/activado/avanzado
															   # arb.nombre es el nombre del comportamiento 
															   # que se va a ejecutar de ese arbol de comportamientos
					if len(robot.hijos) == 2:
						robot = robot.hijos[1]
						bot = robot.hijos[0]
					else:
						seguir = False
			else:
				ejecutar(arb.hijos[1])
			
			if len(arb.hijos) == 3:
				ejecutar(arb.hijos[2])

	elif arb.nombre == 'CONDICIONAL':
		condicion = evaluar(arb.hijos[0])
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
		condicion = evaluar(arb.hijos[0])
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
			ejecutar(arb.hijos[2])

	elif arb.nombre == 'CONDICION':
		if comportamiento == 'ACTIVATE':
			if datos.estado == 'activo': # PREGUNTAR: un robot puede activarse dos veces seguidas?
				print("Error: El robot \"%s\" ya fue activado."%(bot))
			elif datos.estado == 'inactivo': # PREGUNTAR: un robot puede volverse a activar luego de ser desactivado?
				print("Error: El robot \"%s\" ya fue desactivado."%(bot))
			datos.estado = 'activo'
		elif comportamiento == 'DEACTIVATE':
			if datos.estado == 'inactivo':
				print("Error: el robot \"%s\" ya ha sido desactivado."%(bot))
			elif datos.estado == None:
				print("Error: el robot \"%s\" no ha sido activado."%(bot))
			datos.estado = 'inactivo'
		elif comportamiento == 'ADVANCE':
			if datos.estado == 'inactivo':
				print("Error: el robot \"%s\" esta inactivo."%(bot))
			elif estado == None:
				print("Error: el robot \"%s\" no ha sido activado."%(bot))

		comp = datos.comportamientos # datos.comportamientos es un nodo, no un string como 'ACTIVACION'
		encontrado = False # Es true si se consigue el comportamiento que se desea ejecutar en el execute
		while not encontrado:   # del robot en la lista de comportamientos
			if comp.hijos[0].nombre == 'ACTIVACION' and comportamiento == 'ACTIVATE':
				encontrado = True
				ejecutar(comp.hijos[1]) # no hace falta pasarle el robot porque ya los datos son una var global?
			elif comp.hijos[0].nombre == 'DESACTIVACION' and comportamiento == 'DEACTIVATE':
				encontrado = True
				ejecutar(comp.hijos[1])
			elif (comp.hijos[0].nombre == 'ON_EXPRESION' and comportamiento == 'ADVANCE' and
					evaluar(comp.hijos[0].hijos[0])):
				encontrado = True
				ejecutar(comp.hijos[1])
			elif comp.hijos[0].nombre == 'DEFAULT' and comportamiento == 'ADVANCE':
				encontrado = True
				ejecutar(comp.hijos[1])
			else:
				if len(comp.hijos) == 4:
					comp = comp.hijos[3]
		if not encontrado:
			if comportamiento == 'ACTIVACION':
				print("Error: el robot \"%s\" no posee el comportamiento \"activation\"\
										 en su lista."%(robot.hijos[0].hijos[0]))
			elif comportamiento == 'DESACTIVACION':
				print("Error: el robot \"%s\" no posee el comportamiento \"deactivation\"\
										 en su lista."%(robot.hijos[0].hijos[0]))
			elif comportamiento == 'DEFAULT':
				print("Error: el robot \"%s\" no posee el comportamiento \"default\"\
										 en su lista."%(robot.hijos[0].hijos[0]))
			elif comportamiento == 'ON_EXPRESION':
				print("Error: el robot \"%s\" no posee el comportamiento \"on expresion\"\
										 en su lista."%(robot.hijos[0].hijos[0]))
	#elif arb.nombre == 'ACTIVACION':
	#	pass
	#elif arb.nombre == 'DESACTIVACION':
	#	pass
	#elif arb.nombre == 'DEFAULT':
	#	pass
	elif arb.nombre == 'ON_EXPRESION':
		condicion = evaluar(arb.hijos[0],robot) # Se le pasa el nombre del robot para que evalue el comportamiento 
		if type(condicion) == bool:				# del robot correcto y no de cualquier robot con el mismo comportamiento
			if condicion:
				pass
		else:
			print("Error: La condicion del comportamiento debe ser de tipo booleano.")
			sys.exit()

def evaluar(arb,robot=None): # Tabla es la tabla de simbolos global donde se sacaran valores de variables
	if arb.nombre == 'CONJUNCION':
		return arb.hijos[0].evaluar() and arb.hijos[1].evaluar()
	
	elif arb.nombre == 'DISYUNCION':
		return arb.hijos[0].evaluar() or arb.hijos[1].evaluar()
	
	elif arb.nombre == 'IGUALDAD':
		return arb.hijos[0].evaluar() == arb.hijos[1].evaluar()
	
	elif arb.nombre == 'DISTINTO':
		return arb.hijos[0].evaluar() != arb.hijos[1].evaluar()
	
	elif arb.nombre == 'MENOR_QUE':
		return arb.hijos[0].evaluar() < arb.hijos[1].evaluar()
	
	elif arb.nombre == 'MENOR_IGUAL':
		return arb.hijos[0].evaluar() <= arb.hijos[1].evaluar()
	
	elif arb.nombre == 'MAYOR':
		return arb.hijos[0].evaluar() > arb.hijos[1].evaluar()
	
	elif arb.nombre == 'MENOR_IGUAL':
		return arb.hijos[0].evaluar() >= arb.hijos[1].evaluar()
	
	elif arb.nombre == 'SUMA':
		return arb.hijos[0].evaluar() + arb.hijos[1].evaluar()
	
	elif arb.nombre == 'RESTA':
		return arb.hijos[0].evaluar() - arb.hijos[1].evaluar()
	
	elif arb.nombre == 'MULTIPLICACION':
		return arb.hijos[0].evaluar() * arb.hijos[1].evaluar()
	
	elif arb.nombre == 'DIVISION':
		return arb.hijos[0].evaluar() / arb.hijos[1].evaluar()
	
	elif arb.nombre == 'MODULO':
		return arb.hijos[0].evaluar() % arb.hijos[1].evaluar()
	
	elif arb.nombre == 'NEGACION':
		return not arb.hijos[0].evaluar()
	
	elif arb.nombre == 'NEGATIVO':
		return - arb.hijos[0].evaluar()
	
	elif arb.nombre == 'ENTERO': # Los enteros ya vienen casteados del Lexer
		return arb.hijos[0]
	
	elif arb.nombre == 'CARACTER':
		return arb.hijos[0]
	
	elif arb.nombre == 'BOOLEANO':
		if arb.hijos[0] == 'true':
			return True
		elif arb.hijos[0] == 'false':
			return False

	elif arb.nombre == 'VAR':
		return pointer.fetch(arb.hijos[0],robot)
