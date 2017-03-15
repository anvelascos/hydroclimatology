# # Primer mensaje como numero
# mi_mensaje = 5 + 4
# print(mi_mensaje)
# print(type(mi_mensaje))
#
# # # Concatenar textos
# # nombre = "  ANDRES"
# # apellido = "velasco   "
# #
# # nombre_completo = "-" + nombre.strip() + " " + apellido.rstrip() + "-"
# # print(nombre_completo)
#
# numero_decimal = 5. + 4.
# print(numero_decimal)
# print(type(numero_decimal))
#
# mi_mensaje_decimal = float(mi_mensaje)
# print(mi_mensaje_decimal)
# print(type(mi_mensaje_decimal))
#
# numero_entero = int(numero_decimal)
# print(numero_entero)
# print(type(numero_entero))
#
# """
# Simbolo operaciones matematicas en python
#
# suma: +
# resta: -
# multiplicacion: *
# division: /
# potencia: **
# """
#
# mi_division_entera = 9 / 2
# print(mi_division_entera)
# print(type(mi_division_entera))
#
mi_division_decimal = 9. / 2
print(mi_division_decimal)
print(type(mi_division_decimal))

# Trabajando con listas
mi_lista = ["texto", 9, 15., mi_division_decimal]
print(mi_lista[2])
print(type(mi_lista[2]))

for i in range(len(mi_lista)):
    print(mi_lista[i])
    print(type(mi_lista[i]))

def funcion_temporal(nombre):
    print('Tu nombre es: ' + nombre)


def funcion_matematica(x):
    y = x ** 2
    return y


lista_numeros = range(10)

for numero in lista_numeros:
    resultado = funcion_matematica(numero)
    print("El cuadrado de " + str(numero) + " es " + str(resultado))
