from Tabla import Tabla,tabla,datos
from Arbol import *
from Pila import *

pointer = tabla
p = pila()
robot = None # Variable "global" que guarda el robot actual al que se le esta aplicando
				 # una activacion, desactivacion, etc.

def ejecutar(arb,comportamiento=None): # comportamiento es el tipo de comportamiento que se quiere ejecutar
	global pointer,p,robot
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
		datos = pointer.buscarEnTodos(robot,'getDatos') # desactivado o avanzado
		ejecutar(datos.comportamientos,arb.nombre) # Pasa por parametro el tipo de comportamiento
		
		if len(arb.hijos) >= 2:					# para saber cual ejecutar de la lista de comport.
			if arb.hijos[1].nombre == 'LISTA':
				seguir = True
				robot = arb.hijos[1] # Recorre la lista de robots para ir activando cada uno
				while seguir:
					datos = pointer.buscarEnTodos(robot.hijos[0].hijos[0],'getDatos') # Busca el simbolo del ident de la lista
					ejecutar(datos.comportamientos,arb.nombre) # datos.comportamientos es el nodo raiz de los 
															   # comportamientos del del robot que esta siendo
															   # desactivado/activado/avanzado
															   # arb.nombre es el nombre del comportamiento 
															   # que se va a ejecutar de ese arbol de comportamientos
					if len(robot.hijos) == 2:
						robot = robot.hijos[1]
					else:
						seguir = False
			else:
				ejecutar(arb.hijos[1])
			
			if len(arb.hijos) == 3:
				ejecutar(arb.hijos[2])

	elif arb.nombre == 'CONDICIONAL':
		condicion = evaluar(arb.hijos[0])
		if type(condicion) == bool: # Verificar si en la entrega anterior se contemplo que la guardia fuera un booleano. Si no se hizo, evaluar() podria retornar un entero y esta linea explota
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

	elif arb.nombre == 'INST_CONT': 
		ejecutar(arb.hijos[0])

	elif arb.nombre == 'INC_ALCANCE':
		p.addTope(pointer)
		pointer = arb.tabla
		ejecutar(arb.hijos[0])
		if len(arb.hijos) == 3:
			ejecutar(arb.hijos[2])

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
