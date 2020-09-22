import numpy as np
import matplotlib.pyplot as plt


# First exercce of the lab: plot the wave in time, magnitud and phase
def ex1(freqFrame, N, time, frameIn, winL):
    f = np.arange(-len(freqFrame)+1, len(freqFrame))
    magnitud = np.concatenate([np.delete(np.flip(np.abs(freqFrame)), N-1), np.abs(freqFrame)])
    phase = np.concatenate([np.delete((np.flip(np.angle(freqFrame))*-1), N-1), np.angle(freqFrame)])

    plt.plot(time, frameIn)
    plt.title('x[n] en una finestra de '+str(winL)+'mostres')
    plt.xlabel('Segons')
    plt.ylabel('Amplitud')
    plt.show()

    fig1, (jX, zX) = plt.subplots(2, 1)
    fig1.subplots_adjust(hspace=0.5, wspace=0)
    
    jX.plot(f, magnitud)
    jX.set_title('Magnitude')
    jX.set_ylabel('Magnitud', fontsize=10)

    zX.plot(f, phase)
    zX.set_title('Phase')
    zX.set_xlabel('Freqüencia', fontsize=10)
    plt.show()
