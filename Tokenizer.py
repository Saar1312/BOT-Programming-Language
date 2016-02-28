#-------------------------------------------------------------------------------
#							    TOKENIZER
#-------------------------------------------------------------------------------

import ply.lex as lex
import sys

#------------------------------------------------------------------------------- 
# 	La libreria ply.lex utiliza los siguientes criterios para el reconocimiento
# de expresiones:	
# 	La definicion de los tokens se realiza de la siguiente forma:
#	- En las listas con los nombres de los tokens, primero se colocan aquellos 
#   que utilizan una funcion para su reconocimiento. 
#	- Los que poseen funciones van en el mismo orden tanto en la lista como en 
#   las definiciones.
#	- Los tokens deben estar ordenados en forma decreciente según el tamaño de 
#   la ER.
#-------------------------------------------------------------------------------

class Tokenizer:

	def __init__(self):
		self.tokenList = []		# Almacena los tokens para imprimirlos al final
		self.Lexer     = None	# Variable con la herramienta para el analisis 
								# lexicografico
		self.file      = None   # Variable para el archivo
		self.data      = None   # Variable para el contenido del archivo
		self.error     = False  # Booleano que almacena si ha sido hallado un
								# string desconocido para saber si imprimir o no
								# los tokens

	# Tokens que no son palabras reservadas del lenguaje BOT
	tk = [
		'TkCommentC','TkCommentL','TkCaracter','TkIdent','TkNum','TkMenorIgual',
		'TkMayorIgual','TkConjuncion','TkDisyuncion','TkDistinto','TkComa',
		'TkPunto','TkDosPuntos','TkParAbre','TkParCierra',
		'TkSuma','TkResta','TkMult','TkDiv','TkMod','TkMenor','TkMayor',
		'TkIgual','TkNegacion'
		]

	# Tokens de palabras reservadas del lenguaje BOT
	reservadas = {
		'deactivation':'TkDeactivation','deactivate':'TkDeactivate',  
		'activation':'TkActivation', 'activate':'TkActivate', 
		'execute':'TkExecute', 'recieve':'TkRecieve', 'advance':'TkAdvance', 
		'default':'TkDefault', 'collect':'TkCollect', 'create':'TkCreate',
		'while' :'TkWhile', 'right':'TkRight', 'store' :'TkStore',
		'false':'TkFalse', 'true':'TkTrue', 'left':'TkLeft', 'down':'TkDown', 
		'read':'TkRead', 'bool':'TkBool', 'drop':'TkDrop', 'send':'TkSend', 
		'bot':'TkBot', 'int':'TkInt', 'end':'TkEnd', 'on':'TkOn', 'if':'TkIf',
		'as':'TkAs', 'up':'TkUp', 'me':'TkMe', 'char': 'TkChar', 'else': 'TkElse',
		}

	tokens = tk + list(reservadas.values())

	# Expresiones regulares de los simbolos que conforman el lenguaje BOT
	t_TkMenorIgual = r'<='
	t_TkMayorIgual = r'>='
	t_TkConjuncion = r'/\\'
	t_TkDisyuncion = r'\\/'
	t_TkDistinto   = r'/=' 
	t_TkComa       = r','
	t_TkPunto      = r'\.'
	t_TkDosPuntos  = r'\:'
	t_TkParAbre    = r'\('
	t_TkParCierra  = r'\)'
	t_TkSuma  	   = r'\+'
	t_TkResta 	   = r'\-'
	t_TkMult       = r'\*'
	t_TkDiv        = r'/'
	t_TkMod        = r'%'
	t_TkMenor      = r'<'
	t_TkMayor      = r'>'
	t_TkIgual      = r'='
	t_TkNegacion   = r'\~'
	t_ignore       = ' \t'

	#---------------------------------------------------------------------------
	# t_TkCommentL()
	#
	# Utiliza la expresion regular \$\-([^-]|[\n]|(\-+([^\-\$]|[\n])))*\-+\$
	# para identificar los comentarios largos del lenguaje BOT (aquellos que 
	# comienzan por $- y terminan en $-), descartando su contenido. Ademas suma 
	# al contador de lineas el numero de saltos de linea que contenga el 
	# comentario.
	#---------------------------------------------------------------------------
	def t_TkCommentL(self, t):
		r'\$\-([^-]|[\n]|(\-+([^\-\$]|[\n])))*\-+\$'
		for char in t.value:
			if char == '\n':
				self.Lexer.lineno += 1
		pass

	#---------------------------------------------------------------------------
	# t_TkCommentC()
	#
	# Con la ER \$\$.*\n busca los comentarios cortos (aquellos que comienzan por 
	# $$ y terminan con el salto de linea)y los descarta.
	#---------------------------------------------------------------------------
	def t_TkCommentC(self, t): 
		r'\$\$.*\n'
		for char in t.value:
			if char == '\n':
				self.Lexer.lineno += 1
		pass

	#---------------------------------------------------------------------------
	# t_TkCaracter()
	#
	# Reconoce el tipo caracter del lenguaje BOT por medio de la expresion 
	# regular \'[^\0\n\t]\'. Descarta los caracteres "\0" "\n" "\t" y obliga 
	# a que la expresion dentro de las comillas simples sea un caracter simple
	# no vacio. De lo contrario la expresion no sera un reconocida como un 
	# caracter. Ademas elimina las comillas del caracter
	#---------------------------------------------------------------------------
	def t_TkCaracter(self, t):
		r'\'[^\0]\''
		t.value = t.value[1]
		return t

	#---------------------------------------------------------------------------
	# t_TkIdent()
	#
	# Utiliza la ER [a-zA-Z][a-zA-Z0-9_]* para reconocer los identificadores
	# en el lenguaje BOT, es decir, busca strings que comiencen por un caracter
	# del alfabeto, que luego contenga 0 o mas underscores o caracteres 
	# alfanumericos. El lexer no toma a las palabras reservadas como 
	# identificadores por el orden en que estan definidos los tokens
	#---------------------------------------------------------------------------
	def t_TkIdent(self, t):
		r'[a-zA-Z][a-zA-Z0-9_]*'
		t.type = self.reservadas.get(t.value,'TkIdent')
		return t

	#---------------------------------------------------------------------------
	# t_TkNum()
	#
	# Con la \d+ busca una o mas caracteres numericos. Ademas cambia el tipo
	# de la expresion encontrada a int.
	#---------------------------------------------------------------------------
	def t_TkNum(self, t):
		r'\d+'
		t.value = int(t.value)
		return t


	#---------------------------------------------------------------------------
	# t_error()
	#
	# Se ejecuta cuando un token no ha sido reconocido como parte del lenguaje
	# BOT, es decir, cuando ninguna de las definiciones dadas anteriormente
	# identifican el patron. Emite un mensaje de error y omite el token 
	# encontrado. Tambien modifica el valor de la variable "error" para evitar
	# que se impriman los resultados del analisis lexico.
	#---------------------------------------------------------------------------
	def t_error(self, t):
	    print("Error: Caracter inesperado \"%s\" en la fila %d, columna %d"\
	    		 % (t.value[0],t.lineno,self.lexColumna(self.data,t.lexpos)))
	    self.error = True
	    t.lexer.skip(1)

	#---------------------------------------------------------------------------
	# t_nuevaLinea()
	#
	# Aunmenta en uno el numero de lineas cuando un salto de linea es encontrado
	#---------------------------------------------------------------------------
	def t_nuevaLinea(self, t):
	    r'\n+'
	    t.lexer.lineno += len(t.value)

	#---------------------------------------------------------------------------
	# lexColumna()
	#
	# -data: contenido del archivo
	# -lexpos: posicion actual del analizador
	# -inicioLinea: posicion del ultimo salto de linea antes de lexpos
	# -numTabs: numero de \t en la linea actual antes de lexpos
	# -columna: posicion logica del lexer en la linea actual.
	#
	# Determina la columna actual restandole a la posicion actual del analizador
	# la posicion en la variable data (archivo) del ultimo salto de linea. Luego 
	# le suma el numero de espacios correspondientes a las posibles tabulaciones
	# en la linea.
	#---------------------------------------------------------------------------
	def lexColumna(self, data, lexpos):
		inicioLinea = data.rfind('\n',0,lexpos) + 1 # rfind: retorna la posicion del
												    # ultimo \n en el string 
												    # data[0:lexpos] 												    												   
		adicionales = self.contarAdicionales(lexpos,inicioLinea,data)
		columna = lexpos - inicioLinea + adicionales + 1
		return columna 										   
	
	#---------------------------------------------------------------------------
	# contarAdicionales()
	#
	# Cuenta el numero de caracteres adicionales que generan las tabulaciones.
	# Ejemplo:
	# 
	# a\taa\taaa\tx   
	# se veria como
	# a   aa  aaa x
	# Las tabulaciones ocupan 6 espacios adicionales antes de x	
	# Se tomaran las tabulaciones como de tamano 4													
	def contarAdicionales(self,lexpos,inicio,data):
		posicion = 0
		adicionales = 0
		tabLen = 0
		linea = data[inicio:lexpos]
		for char in linea:
			if char == '\t':
				tabLen = 3 - (posicion % 4)
				adicionales += tabLen
				posicion += tabLen + 1
				tabLen = 0
			else:
				posicion += 1
		return adicionales
	
	#---------------------------------------------------------------------------
	# build()
	#
	# Permite a la herramienta generadora de analizadores lexicograficos
	# funcione dentro de la clase Tokenizer.
	#---------------------------------------------------------------------------
	def build(self, **kwargs):
		self.Lexer = lex.lex(object=self,**kwargs)

	#---------------------------------------------------------------------------
	# cargarArchivo()
	#
	# Abre el archivo dado como argumento y retorna su contenido. Si no es 
	# posible abrir el archivo retorna un mensaje de error.
	#---------------------------------------------------------------------------
	def cargarArchivo(self, path):
		try:
			self.file = open(path,'r')
		except IOError:
			print("\nNo se ha podido leer el archivo %s\n"%(path))
			sys.exit()
		with self.file:
			data = self.file.read()
			self.file.close()
			return data

	#---------------------------------------------------------------------------
	# imprimirToken()
	#
	# Imprime los tokens encotrados en el formato propuesto.
	#---------------------------------------------------------------------------
	def imprimirToken(self,data,tk):
		if tk.type == 'TkIdent':
			print("TkIdent(\"%s\") %d %d" % (tk.value,tk.lineno,\
					      self.lexColumna(data,tk.lexpos)),end='')
		elif tk.type == 'TkNum':
			print("TkNum(%d) %d %d" % (tk.value,tk.lineno,\
					self.lexColumna(data,tk.lexpos)),end='')
		elif tk.type == 'TkCaracter':
			print("TkCaracter(\'%s\') %d %d" % (tk.value,tk.lineno,\
							  self.lexColumna(data,tk.lexpos)),end='')
		else:
			print(tk.type,tk.lineno,self.lexColumna(data,tk.lexpos),end='')