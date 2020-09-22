import numpy as np


# Cuantificador uniforme de b bits y fondo de escala xsc
# Parámetros:
# 	- x: Señal de entrada al cuantificador
# 	- b: nº de bits por muestra cuantificada
# 	- xsc: Valor de la tensión de sobrecarga
# Devuelve: Señal cuantificada, es decir, con amplitudes discretas
def quanti(x, b, xsc):

    delta = pow(2, (1-b))*xsc          # Se define el valor de la delta
    y = ((x != 0)*np.sign(x)*(np.fix(abs(x)/delta)+(0.5)))+((x == 0)*(0.5))

    # Cuantificacción por todos los valores de la señal
    ymax = pow(2, (b-1))-0.5
    y = ((abs(y) > ymax)*ymax*np.sign(y))+((abs(y) <= ymax)*y)

    return y


# Decuantificador que se utiliza en el caso de la cuantificacion variable
# Parámetros:
# 	- nivel: Nivel de Quantització
# 	- bits: nº de bits por muestra cuantificada
# 	- Amax: Amlitud Maxima
#   - Amin: Amplitud Minima
# Devuelve:
#   - Aq: Amplitud "original" de la señal
def dequanti(nivel, bits, Amax, Amin):

    # Hacer que la señal varíe entre un valor entre -xsc y xsc
    Amaxmed = 0.5*Amax
    Aminmed = 0.5*Amin

    # Pasar de nivel a valor quantificado
    Aq = nivel-(-0.5+2**(bits-1))

    xsc = Amaxmed-Aminmed
    Aq = Aq*xsc*(2**(1-bits))

    # Volver la señal a sus amplitudes originales
    Aq = Aq+(Amaxmed)+(Aminmed)

    return Aq
