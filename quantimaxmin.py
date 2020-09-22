import numpy as np
from quanti import quanti


# Parámetros:
# 	- A: Señal de entrada al cuantificador
# 	- bits: nº de bits por muestra cuantificada
# 	- Amax: Amlitud Maxima
#   - Amin: Amplitud Minima
# Devuelve:
#   - ampQ: Amplitud del Cuantificador
#   - level: Nivel del Cuantificador
def quantimaxmin(A, bits, Amax, Amin):
    # Hace que la señal varie entre un valor -xsc y xsc
    Amaxmed = Amax*0.5
    Aminmed = Amin*0.5
    xsc = (Amaxmed-Aminmed)
    A2 = A - (Amaxmed + Aminmed)

    # Quantize
    ampQ = quanti(A2, bits, xsc)
    level = ampQ + (-0.5 + pow(2, (bits - 1)))
    level = np.round(level)

    ampQ = ampQ * xsc * pow(2, (1 - bits))
    # Hace volver la señal a sus amplitudes originales
    ampQ = ampQ + (Amaxmed + Aminmed)

    return ampQ, level
