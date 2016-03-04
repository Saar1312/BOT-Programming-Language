#-------------------------------------------------------------------------------
#							         PARSER
#-------------------------------------------------------------------------------

import ply.lex as lex
import ply.yacc as yacc
from Tokenizer import *
from Arbol import *
from Tabla import *
import sys

#-------------------------------------------------------------------------------
# Instrucciones y convenciones:
# * Los simbolos no terminales seran indicados con MAYUSCULAS
#
# * Las producciones de la gramatica son definidas dentro de funciones p_nombre(p)
# de la siguiente forma:
# 
# "S : a A b                            S -->  a A b
# 	| c               EQUIVALE A             | c
#	|                                        | lambda
# "
# donde no debe confundirse la definicion con los comentarios o strings en python.
#
# * En cada funcion que define a la gramatica se aplicara la nocion de gramaticas
# de atributos al utilizar un objeto "p" para almacenar los elementos de la 
# produccion en un arreglo , por lo que si una produccion tiene la forma:
#
# S : a B c
#   | d
#
# entonces "p" podra ser:
# p = [a,B,c] o p = [d]
# Para esto se define una estructura "p" del tipo arbol dada por:
# p[0] = arbolTipoX('TIPO',[hijo1,hijo2,...,hijon]) que genera de forma recursiva
# el arbol sintactico abstracto.

# * La "variable global" del lenguaje BOT no sera reconocida de forma distinta
# a un identificador.
#-------------------------------------------------------------------------------

# Definiendo la precedencia de operadores. La precedencia fue especificada con 
# mayor precedencia para los operadores al final de la lista y la misma para 
# aquellos en la misma línea.

# Declarando tabla de simbolos globalmente

# HACER QUE CUANDO SE CREE UN ARBOL PADRE, ASIGNARLE A LA TABLA PADRE EL HIJO QUE LA ESTA CREANDO
# QUE PASA SI SE DECLARA me COMO UN ROBOT?
# Hay que dar error cuando se use un robot sin que tenga un valor asociado? (dentro de las inst. 
# de robot debe haner un store de primero para poder usar el robot)
# Como saber de que robot es cada subtabla de simbolos de inst de robot?
# Hay que modificar el arbol para que sirva en la ultima entrega?
# Alfajores: 1 T harina trigo 2 Maizina 2 Huevos 1 Azucar 

#---- Igualdad de caracteres
#---- Verificar tipos del me Ej, me - 1
#---- Agregar token me 
#---- Un solo activate/deactivate
errorSint = True

precedence = (
	('left','TkDisyuncion'),
	('left','TkConjuncion'),
	('left','TkDistinto'),
	('left','TkIgual'),
	('left','TkMenorIgual'),
	('left','TkMayorIgual'),
	('left','TkMenor'),
	('left','TkMayor'),
	('right','TkNegacion'),
	('left', 'TkSuma', 'TkResta'),
	('left', 'TkMult', 'TkDiv','TkMod'),
	('right','TkNegativo'),
)

#-------------------------------------------------------------------------------
# Esta produccion pretende facilitar la comprension de la gramatica al indicar
# que un programa valido en BOT puede empezar por un conjunto de instrucciones de
# robot seguidas por instrucciones del controlador, o comenzar directamente por
# instrucciones del controlador.
#-------------------------------------------------------------------------------
def p_inicio(p):
	'''INICIO : CREATE
			  | EXECUTE
	'''
	p[0] = arbol('INICIO',[p[1]])

#-------------------------------------------------------------------------------
# Esta produccion genera la seccion de las instrucciones de robot, la cual esta
# delimitada por las palabras reservadas "create" y "execute". Puede tener mas
# de una instruccion de declaracion de robots:
#
# 					TYPE TkBot IDENT LISTA_IDENT   TkEnd
# 					bool bot   robot,robot1,robot2 end
#
# la cual a su vez puede contener el comportamiento de los robots declarados. 
# Este comportamiento es generado por el simbolo no terminal COMPORTAMIENTO.
# Finalmente la produccion CREATE contiene el simbolo no terminal DECLARE, ya que
# se podria realizar mas de una declaracion de robots; y al simbolo no terminal
# EXECUTE que obliga a la gramatica a generar la seccion de instrucciones del
# controlador.
#-------------------------------------------------------------------------------
def p_create(p):
	'CREATE : TkCreate TYPE TkBot IDENT LISTA_IDENT COMPORTAMIENTO TkEnd DECLARE EXECUTE'
	if p[8] != None: # Si la produccion DECLARE se volvio lambda, deberia haber
					 # almacenado
		p[0] = instContr('INSTRUCCIONES_ROBOT',\
			   [instContr('DECLARACION_ROBOT',[p[2],p[4],p[5],p[6],p[8],p[9]])])
	else:
		p[0] = instContr('INSTRUCCIONES_ROBOT',\
			   [instContr('DECLARACION_ROBOT',[p[2],p[4],p[5],p[6],p[9]])])
#-------------------------------------------------------------------------------
# Define las instrucciones de declaracion de robots. Notese que podria ser lambda
# ya que el simbolo no terminal DECLARE ha sido definido para general mas de
# una declaracion de robots. La primera ya habria sido llevada a cabo por la
# produccion CREATE
#-------------------------------------------------------------------------------
def p_declaracion(p):
	'''DECLARE : TYPE TkBot IDENT LISTA_IDENT COMPORTAMIENTO TkEnd DECLARE
			   |
	'''
	if len(p) > 1:
		if p[7] == None: # Si NO se fue otra vez a DECLARE
			p[0] = instContr('DECLARACION_ROBOT',[p[1],p[3],p[4],p[5]])
		else:			 # Si se fue otra vez a DECLARE
			p[0] = instContr('DECLARACION_ROBOT',[p[1],p[3],p[4],p[5],p[7]])

#-------------------------------------------------------------------------------
# Genera los posibles tipos de un robot en BOT.
#-------------------------------------------------------------------------------
def p_tipo(p):
	'''TYPE : TkInt
			| TkBool
			| TkChar
	'''
	if type(p[1]) == int:
		p[0] = defTipo('TIPO_ENTERO',[],'int')
	elif type(p[1]) == bool:
		p[0] = defTipo('TIPO_BOOL',[],'bool')
	elif type(p[1]) == str:
		p[0] = defTipo('TIPO_CHAR',[],'char')

#-------------------------------------------------------------------------------
# Permite generar una lista de identificadores.
#-------------------------------------------------------------------------------
def p_identificador(p):
	'''LISTA_IDENT : TkComa IDENT LISTA_IDENT
			 |
	'''
	if len(p) > 1:
		if p[3] != None: # Si no se volvio a encontrar otro identificador
			p[0] = instRobot('- lis_var: ',[p[2],p[3]])
		else:
			p[0] = instRobot('- lis_var: ',[p[2]])

#-------------------------------------------------------------------------------
# Permite generar identificadores (nombres de robots o variables)
#-------------------------------------------------------------------------------
def p_ident(p):
	'IDENT : TkIdent'
	p[0] = expresion('- var: ',[p[1]])

#-------------------------------------------------------------------------------
# COMPORTAMIENTO genera un comportamiento de un robot, delimitado por las palabras
# reservadas "on" y "end"
#-------------------------------------------------------------------------------
def p_comportamiento(p):
	'''COMPORTAMIENTO : TkOn CONDICION TkDosPuntos INST_ROBOT TkEnd COMPORTAMIENTO
					  |
	'''
	if len(p) > 1:
		if p[6] != None: # Si no se volvio a encontrar otro identificador
			p[0] = instRobot('CONDICION',[p[2],p[4],p[6]])
		else:
			p[0] = instRobot('CONDICION',[p[2],p[4]])

#-------------------------------------------------------------------------------
# Genera los distintos estados que puede tener un robot
#-------------------------------------------------------------------------------
def p_condicion(p):
	'''CONDICION : TkActivation
				 | TkDeactivation
				 | TkDefault
				 | EXP
	'''
	if p[1] == 'activation':
		p[0] = instContr('ACTIVACION',[])
	elif p[1] == 'deactivation':
		p[0] = instContr('DESACTIVACION',[])
	elif p[1] == 'default':
		p[0] = instContr('DEFAULT',[])
	else:
		p[0] = expresion('EXPRESION',[p[1]])

#-------------------------------------------------------------------------------
# EXP genera las expresiones aritmeticas, booleanas, identificadores y constantes
# bien parentizadas.
#-------------------------------------------------------------------------------
def p_exp(p):
	'''EXP : EXP TkConjuncion EXP
		   | EXP TkDisyuncion EXP
		   | EXP TkIgual EXP
		   | EXP TkDistinto EXP
		   | IDENT
		   | LITERAL_BOOL
		   | TkParAbre EXP TkParCierra
		   | TkNegacion EXP
		   | TkResta EXP %prec TkNegativo
		   | EXP TkMenor EXP
		   | EXP TkMenorIgual EXP
		   | EXP TkMayor EXP
		   | EXP TkMayorIgual EXP
		   | EXP TkSuma EXP
		   | EXP TkResta EXP
		   | EXP TkMult EXP
		   | EXP TkDiv EXP
		   | EXP TkMod EXP
		   | TkNum
	'''
	# len(p) == 4 indica que se leyo una operacion binaria (2 operandos, 1 
	# operador, p[0] = 4 elementos en el arreglo)

	if len(p) == 4:
		if p[1] != '(': # Si no es parentesis entonces se tienen expresiones binarias
			if p[2] == '/\\': # Ademas el tipo de los operandos debe corresponderse con el
				p[0] = expresion('CONJUNCION',[p[1],p[3]]) # del resultado de la operacion

			elif p[2] == '\/':
				p[0] = expresion('DISYUNCION',[p[1],p[3]])

			elif p[2] == '=':
				p[0] = expresion('IGUALDAD',[p[1],p[3]])

			elif p[2] == '/=':
				p[0] = expresion('DISTINTO',[p[1],p[3]])

			elif p[2] == '<':
				p[0] = expresion('MENOR_QUE',[p[1],p[3]])

			elif p[2] == '<=':
				p[0] = expresion('MENOR_IGUAL',[p[1],p[3]])

			elif p[2] == '>':
				p[0] = expresion('MAYOR',[p[1],p[3]])

			elif p[2] == '>=':
				p[0] = expresion('MAYOR_IGUAL',[p[1],p[3]])

			elif p[2] == '+':
				p[0] = expresion('SUMA',[p[1],p[3]])

			elif p[2] == '-':
				p[0] = expresion('RESTA',[p[1],p[3]])

			elif p[2] == '*':
				p[0] = expresion('MULTIPLICACION',[p[1],p[3]])

			elif p[2] == '/':
				p[0] = expresion('DIVISION',[p[1],p[3]])

			elif p[2] == '%':
				p[0] = expresion('MODULO',[p[1],p[3]])
		else:
			p[0] = expresion('PARENTESIS',[p[2]],p[2].tipo)

	elif len(p) == 3:
		if p[1] == '~':
			p[0] = expresion('NEGACION',[p[2]],'bool')
		elif p[1] == '-':
			p[0] = expresion('NEGATIVO',[p[2]],'int')
	elif len(p) == 2:
		if type(p[1]) == int:
			p[0] = expresion('ENTERO',[p[1]],'int')
		elif (p[1] == True) or (p[1] == False):
			p[0] = expresion('BOOLEANO',[p[1]],'bool')
		else:
			p[0] = expresion('- var: ',[p[1]])

#-------------------------------------------------------------------------------
# Genera los booleanos True y False
#-------------------------------------------------------------------------------
def p_literal_bool(p):
	'''LITERAL_BOOL : TkTrue
					| TkFalse
	'''
	if p[1] == 'true':
		p[0] = expresion('TRUE',[],'bool')
	elif p[1] == 'false':
		p[0] = expresion('FALSE',[],'bool')


#-------------------------------------------------------------------------------
# Genera las instrucciones del robot "store", "collect", "drop", "read", "send",
# "recieve", etc.
#-------------------------------------------------------------------------------
def p_inst_robot(p):
	'''INST_ROBOT : TkStore EXPRESION TkPunto INST_ROBOT_A
				  | TkCollect COLLECT TkPunto INST_ROBOT_A
				  | TkDrop EXPRESION TkPunto INST_ROBOT_A
				  | DIRECCION TkPunto INST_ROBOT_A
				  | DIRECCION EXP TkPunto INST_ROBOT_A
				  | READ TkPunto INST_ROBOT_A
				  | TkSend TkPunto INST_ROBOT_A
				  | TkRecieve TkPunto INST_ROBOT_A
	'''
	if p[1] == 'store':
		if p[4] == None:
			p[0] = instContr('STORE',[p[2]])
		else:
			p[0] = instContr('STORE',[p[2],p[4]])
	elif p[1] == 'collect':
		if (p[2] == None) and (p[4] == None):
			p[0] = instContr('COLLECT',[])
		elif (p[2] != None) and (p[4] == None):
			p[0] = instContr('COLLECT',[p[2]])
		elif (p[2] == None) and (p[4] != None):
			p[0] = instContr('COLLECT',[p[4]])
		elif (p[2] != None) and (p[4] != None):
			p[0] = instContr('COLLECT',[p[2],p[4]])
	elif p[1] == 'drop':
		if p[4] == None:
			p[0] = instContr('DROP',[p[2]])
		else:
			p[0] = instContr('DROP',[p[2],p[4]])
	elif p[1] == 'read':
		if p[3] == None:
			p[0] = instContr('READ',[p[1]])
		else:
			p[0] = instContr('READ',[p[1],p[3]])
	elif p[1] == 'send':
		if p[3] == None:
			p[0] = instContr('SEND',[p[1]])
		else:
			p[0] = instContr('SEND',[p[1],p[3]])
	elif p[1] == 'recieve':
		if p[3] == None:
			p[0] = instContr('RECIEVE',[p[1]])
		else:
			p[0] = instContr('RECIEVE',[p[1],p[3]])
	else: 
		if p[2] == '.':
			if p[3] == None:
				p[0] = instContr('DIRECCION',[p[1]])
			else:
				p[0] = instContr('DIRECCION',[p[1],p[3]])
		else:
			if p[4] == None:
				p[0] = instContr('DIRECCION',[p[1],p[2]])
			else:
				p[0] = instContr('DIRECCION',[p[1],p[2],p[4]])

#-------------------------------------------------------------------------------
# INST_ROBOT_A permite generar mas de una instruccion de robot seguida
#-------------------------------------------------------------------------------
def p_inst_robot_adicional(p):
	'''INST_ROBOT_A : INST_ROBOT
					|
	'''
	if len(p) > 1:
		p[0] = instContr('INST_ROBOT',[p[1]])


#-------------------------------------------------------------------------------
# Genera expresiones y caracteres
#-------------------------------------------------------------------------------
def p_expresion(p):
	'''EXPRESION : EXP
				 | TkCaracter
	'''
	if type(p[1]) == chr:
		p[0] = expresion('CARACTER',p[1],'char')
	else:
		p[0] = expresion('EXPRESION',[p[1]],p[1].tipo)

#-------------------------------------------------------------------------------
# Genera las direcciones a las que se puede mover un robot
#-------------------------------------------------------------------------------
def p_direccion(p):
	'''DIRECCION : TkLeft
				 | TkRight
				 | TkUp
				 | TkDown
	'''
	if p[1] == 'up':
		p[0] = instContr('UP',[])
	elif p[1] == 'down':
		p[0] = instContr('DOWN',[])
	elif p[1] == 'right':
		p[0] = instContr('RIGHT',[])
	elif p[1] == 'left':
		p[0] = instContr('LEFT',[])

#-------------------------------------------------------------------------------
# Permite generar el tipo de instruccion "collect" cuando se puede almacenar el 
# valor en una variable.
#-------------------------------------------------------------------------------
def p_collect(p):
	'''COLLECT : TkAs IDENT
			   |
	'''
	if len(p)>1:
		p[0] = instContr('COLLECT_AS',[p[2]])					# bloque de instrucciones de robot actual

#-------------------------------------------------------------------------------
# Permite generar el tipo de instruccion "read" cuando se puede almacenar el 
# valor en una variable.
#-------------------------------------------------------------------------------
def p_read(p):
	'''READ : TkRead
		    | TkRead TkAs IDENT
	'''
	if len(p)>2:
		p[0] = instContr('READ_AS',[p[3]])
	else:
		p[0] = instContr('READ_AS',[])

#-------------------------------------------------------------------------------
# Genera la seccion del controlador.
#-------------------------------------------------------------------------------
def p_execute(p):
	'''EXECUTE : TkExecute INST_CONTROLADOR TkEnd'''
	p[0] = instRobot('EXECUTE',[p[2]]) # p[2] es el arbol de INST_CONTROLADOR


#-------------------------------------------------------------------------------
# Permite generar las instrucciones de la seccion del controlador.
#-------------------------------------------------------------------------------
def p_inst_controlador(p): 
	'''INST_CONTROLADOR : TkActivate IDENT LISTA_IDENT TkPunto INST_CONTROLADOR_A
						| TkAdvance IDENT LISTA_IDENT TkPunto INST_CONTROLADOR_A
						| TkDeactivate IDENT LISTA_IDENT TkPunto INST_CONTROLADOR_A
						| TkIf EXP TkDosPuntos CONTENIDO TkEnd INST_CONTROLADOR_A
						| TkWhile EXP TkDosPuntos INST_CONTROLADOR TkEnd INST_CONTROLADOR_A 
						| INICIO
	'''
	if p[1] == 'activate':
		if p[3] == None:
			if p[5] == None:
				p[0] = instRobot('ACTIVATE',[p[2]])
			else:
				p[0] = instRobot('ACTIVATE',[p[2],p[5]])
		else:
			if p[5] == None:
				p[0] = instRobot('ACTIVATE',[p[2],p[3]])
			else:
				p[0] = instRobot('ACTIVATE',[p[2],p[3],p[5]])
	elif p[1] == 'advance':
		if p[3] == None:
			if p[5] == None:
				p[0] = instRobot('ADVANCE',[p[2]])
			else:
				p[0] = instRobot('ADVANCE',[p[2],p[5]])
		else:
			if p[5] == None:
				p[0] = instRobot('ADVANCE',[p[2],p[3]])
			else:
				p[0] = instRobot('ADVANCE',[p[2],p[3],p[5]])
	elif p[1] == 'deactivate':
		if p[3] == None:
			if p[5] == None:
				p[0] = instRobot('DEACTIVATE',[p[2]])
			else:
				p[0] = instRobot('DEACTIVATE',[p[2],p[5]])
		else:
			if p[5] == None:
				p[0] = instRobot('DEACTIVATE',[p[2],p[3]])
			else:
				p[0] = instRobot('DEACTIVATE',[p[2],p[3],p[5]])
	elif p[1] == 'if':
		if p[6] == None:
			p[0] = instRobot('CONDICIONAL',[p[2],p[4]])
		else:
			p[0] = instRobot('CONDICIONAL',[p[2],p[4],p[6]])
	elif p[1] == 'while':
		if p[6] == None:
			p[0] = instRobot('CICLO',[p[1],p[2],p[3],p[4],p[5]])
		else:
			p[0] = instRobot('CICLO',[p[1],p[2],p[3],p[4],p[5],p[6]])
	else:
		p[0] = arbol('INC_ALCANCE',[p[1]])


#-------------------------------------------------------------------------------
# Permite generar el contenido de un condicional, dependiendo de si este posee
# una condicion alterna (else)
#-------------------------------------------------------------------------------
def p_contenido(p):
	'''CONTENIDO : INST_CONTROLADOR
				 | INST_CONTROLADOR TkElse TkDosPuntos INST_CONTROLADOR
	'''
	if len(p)>2: # Si hay dos elementos en p[], entonces es la produccion de 
	 			 # abajo
		p[0] = instRobot('ELSE',[p[1],p[4]])
	else:
		p[0] = instRobot('INST_IF',[p[1]])

#-------------------------------------------------------------------------------
# Permite generar mas de una instruccion de controlador
#-------------------------------------------------------------------------------
def p_inst_controlador_a(p):
	'''INST_CONTROLADOR_A : INST_CONTROLADOR
						  | 
	'''
	if len(p)>1:
		p[0] = instRobot('INST_CONT',[p[1]])

#-------------------------------------------------------------------------------
# Regla para errores de sintaxis
#-------------------------------------------------------------------------------
def p_error(p):
	print(p.lineno)
	print("Error de sintaxis en la linea %d del archivo %s"%(p.lineno,sys.argv[1]))
	exit()

def errorTipos():
#def p_errorTipos(p):
	#if tipo == 'redeclaracion':
	#if tipo == 'no_declarado':
	#if tipo == 'error_tipos':
	#print("Error de tipos en la linea %d, columna %d" % (p.lineno,p.lexpos))
	print("Error TIPOS")
	exit()

