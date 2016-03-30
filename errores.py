#-------------------------------------------------------------------------------
#                               MANEJADOR DE ERRORES                            
#-------------------------------------------------------------------------------
import sys
from Arbol import *
from Tabla import *


#---------------------------------------------------------------------------
# error_linea()
#
# Imprime errores relacionados con comportamientos
#---------------------------------------------------------------------------
def error_linea(id,arbol):
    print("Error en la linea %d:" % (arbol.linea))
    
    if id == 1:
        print("Un robot no puede tener dos comportamientos de activacion.")
    elif id == 2:
        print("Un comportamiento \"activation\" no puede estar precedido por \
                                un \"deactivation\" .")
    elif id == 3:
        print("Un comportamiento \"activation\" no puede estar precedido por \
                                un \"default\" .")
    elif id ==4:
        print("El comportamiento \"deactivation\" debe estar precedido por\
                                        un activacion.")
    elif id == 5:
        print("Un robot no puede tener dos comportamientos de desactivacion.")
    elif id == 6:
        print("Un robot no puede tener dos comportamientos default.")
    elif id == 7:
        print("El comportamiento debe estar precedido por un \"activation\".")
    elif id == 8:
        print("El comportamiento no puede estar precedido por un \"deactivation\".")
    elif id == 9:
        print("El comportamiento debe estar precedido por un \"activation\".")
    elif id == 10:
        print("El comportamiento no puede estar precedido por un \"deactivation\".")
    elif id == 11:
        print("El comportamiento no puede estar precedido por un \"default\".")
    sys.exit()

#---------------------------------------------------------------------------
# error_tipo()
#
# Imprime errores relacionados con problemas de tipo en los robots y las 
# varibales
#---------------------------------------------------------------------------
def error_tipo(id,rama):
    print("Error de tipos en la linea %d:" % (rama.linea))
    
    if id in [1,2,3]:
        print("No es posible operar elementos del tipo \"%s\""%\
            (rama.hijos[0].tipo),end=" ")
    
    if id == 1:
        print("con un operador booleano.")
    elif id ==2:
        print("con otro de tipo \"%s\"."% (rama.hijos[1].tipo))
    elif id == 3:
        print("con un operador aritmetico.")
    
    elif id == 4:
        print("Se esperaba una expresion de tipo booleano,",end=' ')
    elif id == 5:
        print("Se esperaba una expresion de tipo entero,",end=' ')

    if id in [4,5]:
        print("pero fue dada una de tipo \"%s\"." % (rama.hijos[0].tipo))
    sys.exit()

#---------------------------------------------------------------------------
# error_otros()
#
# Imprime errores relacionados con variables y condiciones
#---------------------------------------------------------------------------
def error_otros(id, rama = None):
    if id == 1:
        print("Error en la linea %d: La variable \"me\" no puede ser . \
                                utilizada en la seccion de ejecucion")
    elif id == 2:
        print("Error en la linea %d: La variable \"%s\" no ha sido declarada." \
                            % (rama.linea, rama.hijos[0]))
    elif id == 3:
        print("Error en la linea %d: La condicion del robot debe evaluar en un booleano.")
    sys.exit()

#---------------------------------------------------------------------------
# error_ejecucion()
#
# Imprime errores que pueden surgir durante la ejecucion del programa
#---------------------------------------------------------------------------
def error_ejecucion(id,bot = None,datos = None,linea = 0):

    print ('Error en la linea %d: '%(linea),end='')

    if id == 1:
        print("La condicion del \"if\" debe ser de tipo booleano.")
    elif id == 2:
        print("La guardia del ciclo debe ser de tipo booleano.")
    elif id == 3:
        print("El robot \"%s\" ya fue activado."%(bot))
    elif id == 4:
        print("El robot \"%s\" ya ha sido desactivado."%(bot))
    elif id == 5:
        print("El robot \"%s\" esta inactivo."%(bot))
    elif id == 6:
        print("La condicion del comportamiento debe ser de tipo booleano.")
    elif id == 7:
        print("El numero de espacios debe ser un entero para mover a %s."%(bot))
    elif id == 8:
        print("El robot \"%s\" no ha sido activado."%(bot))
    elif id == 9:    
        print("El robot \"%s\" no ha sido inicializado."%(bot))
    elif id == 10:
        print("El robot \"%s\" no posee un comportamiento que permita avanzarlo."%(bot))
    elif id == 11:
        print("No existen elementos en la posicion [%s,%s] de la matriz."%(datos.posicion[0],datos.posicion[1]))
    elif id == 12:
        print("El tipo de la expresion evaluada es distinto al tipo de \"%s\"."%(bot))
    elif id == 13:
        print("El tipo del elemento recolectado es distinto al tipo de \"%s\"."%(bot))
    elif id == 14:
        print("No se puede mover el robot %s un numero negativo de espacios."%(bot))
    
    sys.exit()

#---------------------------------------------------------------------------
# error_conflicto()
#
# Imprime errores relacionados con conflictos que no hacen halt del programa
#---------------------------------------------------------------------------
def error_conflicto(id,arb = None):
    if id == 1:
        print("Error: Conflicto entre el tipo del robot y el valor ingresado.")
        print()
    if id == 2:
        print("Error: No es posible dividir por cero.")
        print()
    if id == 3:
        print("Error: No es posible obtener el modulo por cero.")
        print()
    elif id == 4:
        print("Error: La variable %s no ha sido inicializada."%(arb.hijos[0]))



