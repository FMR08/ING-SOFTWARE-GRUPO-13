#verifica un run. Recibe un string con solamente los digitos (sin puntos ni guion)
def run_valido(run):
    if len(run)!=9:
        return False
    for c in run:
        if not c.isdigit():
            return False

    suma = 0
    multiplicadores = [3, 2, 7, 6, 5, 4, 3, 2]
    for i in range(8):
        suma += int(run[i]) * multiplicadores[i]
    verificador_esperado = 11 - (suma % 11)

    if verificador_esperado == 11:
        verificador_esperado = '0'
    elif verificador_esperado == 10:
        verificador_esperado = 'K'
    else:
        verificador_esperado = str(verificador_esperado)
    return verificador_esperado == run[8].upper()