from Tabla import *
from Arbol import *

def ejecutar(arb,comportamiento=None): # comportamiento es el tipo de comportamiento que se quiere ejecutar
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
		robot = arb.hijos[0].hijos[0]
		datos = tabla.fetchBot(robot)
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
		# !!!! AGREGE UNA CONDICION DE QUE NO SEA NONE MIENTRAS LA FUNCION ESTA VACIA !!!! #
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
		if datos != None:
			ejecutar(datos.comportamientos,arb.nombre) # Pasa por parametro el tipo de comportamiento
		
		if len(arb.hijos) >= 2:					# para saber cual ejecutar de la lista de comport.
			if arb.hijos[1].nombre == 'LISTA':
				seguir = True
				robot = arb.hijos[1] # Recorre la lista de robots para ir activando cada uno
				while seguir:
					datos = tabla.fetchBot(robot.hijos[0].hijos[0]) # Busca el simbolo del ident de la lista
					#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
					#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
					# !!!! AGREGE UNA CONDICION DE QUE NO SEA NONE MIENTRAS LA FUNCION ESTA VACIA !!!! #
					#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
					#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
					if datos != None:
						ejecutar(datos.comportamientos,arb.nombre)
					
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
		while evaluar(arb.hijos[0]):
			ejecutar(arb.hijos[1])
		if len(arb.hijos) == 3:
			ejecutar(arb.hijos[2])

	elif arb.nombre == 'INST_CONT': 
		ejecutar(arb.hijos[0])

	elif arb.nombre == 'INC_ALCANCE':
		ejecutar(arb.hijos[0])
		if len(arb.hijos) == 3:
			ejecutar(arb.hijos[2])

	elif arb.nombre == 'ON_EXPRESION': # No puede ir aqui porque se va a evaluar la exp sin que el robot haya sido avanzado
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
		# !!!!!!!!!!!!!!!!! AQUI LE PASAS UN PARAMETRO DE MAS A EVALUAR !!!!!!!!!!!!!!!!!! #
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
		if arb.evaluar(arb.hijos[0],robot): # Verificar que sea un booleano (retornar None si no lo es)
			pass # Ejecutar comportamiento
	

def evaluar(arb): # Tabla es la tabla de simbolos global donde se sacaran valores de variables
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
		return tabla.fetch(arb.hijos[0],robot)
