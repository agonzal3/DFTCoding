import numpy as np
from scipy.fftpack import fft, ifft
from quantization import quantization, variable_quantization
from Ex1 import ex1


# Block Transform of the audio.
# Parameters:
#   - audio: original signal
#   - nBands: number of bands to quante the signal
#   - n_bits: number of bits to quatize the signal
#   - winL: size of the windows that will divide the signal
#   - doQuantizationByBands: Option to chose bewten no Quantization, and
#                            variable Quantization or Quantization
#   - time: array with the values of the seconds of the audio
# Return:
#   - waveOut: the new signal reconstructed

def transform(audio, nBands, n_bits, winL, doQuantizationByBands, time):
    waveOut = np.zeros(audio.shape)
    nFrames = int(len(audio)/winL)-1

    for iFrame in range(0, nFrames):
        beginFrame = int(iFrame*winL)
        endFrame = beginFrame+winL
        frameIn = audio[beginFrame:endFrame]

        # fft
        freqFrame = np.fft.fft(frameIn)
        freqFrame = freqFrame[0:int(winL/2)]

        # Quantization
        if doQuantizationByBands:
            QfreqFrame = quantization(nBands, freqFrame, n_bits)

        else:
            QfreqFrame = freqFrame
            if iFrame == 55:
                N = len(freqFrame)
                time_ex1 = time[beginFrame:endFrame]
                ex1(freqFrame, N, time_ex1, frameIn, winL)

        # ifft
        conj = np.conjugate(np.flip(QfreqFrame))
        QfreqFrame = np.concatenate([QfreqFrame, conj])
        frameOut = np.fft.irfft(QfreqFrame, n=winL)

        # Overlap-add
        frameOut_w = frameOut
        waveOut[beginFrame:endFrame] = frameOut_w

    return waveOut


# Parameters:
#   - ...
#   - overlap: values betwen [0, 1)
#   - window: rectangular, hanning or hamming window of the winL size
# Return:
#   - ...
#   - numbits: in variable Quantization case is the total number of bits that
#              has been used to quaitize the signal
def transform_overlap(audio, nBands, n_bits, winL, overlap, window, doQuantizationByBands, energyThreshold):
    waveOut = np.zeros(audio.shape)
    nFrames = int(len(audio)/(winL*(1-overlap)))-int(1/(1-overlap))
    numbits = 0

    for iFrame in range(0, nFrames):
        beginFrame = int(iFrame*winL*(1-overlap))
        endFrame = beginFrame+winL
        frameIn = audio[beginFrame:endFrame]

        # fft
        freqFrame = np.fft.fft(frameIn*window)
        freqFrame = freqFrame[0:int(winL/2)]

        # Quantization
        if doQuantizationByBands == 5:
            QfreqFrame, numbits = variable_quantization(nBands, freqFrame, n_bits, numbits, energyThreshold)
            numbits = numbits + 1
        elif doQuantizationByBands:
            QfreqFrame = quantization(nBands, freqFrame, n_bits)

        # ifft
        conj = np.conjugate(np.flip(QfreqFrame))
        QfreqFrame = np.concatenate([QfreqFrame, conj])
        frameOut = np.fft.irfft(QfreqFrame, n=winL)

        # Overlap-add
        frameOut_w = frameOut*window
        waveOut[beginFrame:endFrame] = waveOut[beginFrame:endFrame]+frameOut_w

    return waveOut, numbits
