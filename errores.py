import sys
from Arbol import *
from Tabla import *

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

def error_ejecucion(id,bot = None,datos = None):

    if not (id in [8,9,10]):
        print ('Error: ',end='')

    if id in [3,4,6]:
        print(' El robot \"%s\" '%(bot),end='')

    # if id in [8,9,10]:
    #     print('no posee un comportamiento ',end='')

    if id in [11,13]:
        print('El tipo de',end='')
        
    if id == 0:
        print('Null')

    if id == 1:
        print("La condicion del \"if\" debe ser de tipo booleano.")
    elif id == 2:
        print("La guardia del ciclo debe ser de tipo booleano.")
    
    elif id == 3:
        print("ya fue activado.")
    elif id == 4:
        print("ya ha sido desactivado.")
    elif id == 5:
        print("esta inactivo.")

    elif id == 6:
        print("La condicion del comportamiento debe ser de tipo booleano.")
    elif id == 7:
        print("El numero de espacios debe ser un entero para mover a %s."%(bot))

    # elif id == 8:
    #     print("\"activation\" en su lista para poder ser activado.")
    # elif id == 9:
    #     print("\"deactivation\" en su lista para poder ser desactivado.")
    # elif id == 10:
    #     print("que permita avanzarlo.")
    
    elif id == 12:
        print("No existen elementos en la posicion [%s,%s] de la matriz."%(datos.posicion[0],datos.posicion[1]))

    elif id == 11:
        print(" la expresion evaluada es distinto al tipo de \"%s\"."%(bot))
    elif id == 13:
        print("l elemento recolectado es distinto al tipo de \"%s\"."%(bot))

    elif id == 14:
        print("No se puede mover el robot %s un numero negativo de espacios."%(bot))
    
    
    if not (id in [8,9,10]):
        sys.exit()


def error_conflicto(id):
    if id == 1:
        print("Error: Conflicto entre el tipo del robot y el valor ingresado.")
        print()