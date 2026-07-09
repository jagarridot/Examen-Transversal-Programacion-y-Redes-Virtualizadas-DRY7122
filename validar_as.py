# Script que indica si un número de AS de BGP es público o privado

def validar_as(numero_as):
    numero_as = int(numero_as)
    if (64512 <= numero_as <= 65534) or (4200000000 <= numero_as <= 4294967294):
        return "privado"
    elif 1 <= numero_as <= 4294967295:
        return "público"
    else:
        return "no válido"

as_input = input("Ingrese el número de AS de BGP: ")

if as_input.isdigit():
    resultado = validar_as(as_input)
    if resultado == "no válido":
        print(f"El AS {as_input} no es un número de AS válido.")
    else:
        print(f"El AS {as_input} es un AS {resultado}.")
else:
    print("Por favor ingrese un número válido.")
