import numpy as np
from quantimaxmin import quantimaxmin
from quanti import dequanti


# Quantization for bands
# Parameters:
#   - nBands: number of bands that the frame signal will be divided
# 	- freqFrame: fft reduced signal
#   - n_bits: number of bits to quantized sample
# Return:
#   - QfreqFrame: Recover amplitud of the frame
def quantization(nBands, freqFrame, n_bits):
    N = len(freqFrame)
    QfreqFrame = np.zeros(N, dtype=complex)
    QfreqFrame_real = np.zeros(N)
    QfreqFrame_img = np.zeros(N, dtype=complex)

    beginBand = 0

    for iBand in range(0, nBands):
        endBand = int(N/pow(2, nBands-iBand))

        max_amplitude = np.sqrt(N/pow(2, iBand))

        # Real part: real(fft)
        data = np.real(freqFrame[beginBand:endBand])
        q_value, _ = quantimaxmin(data, n_bits, max_amplitude, -max_amplitude)
        QfreqFrame_real[beginBand:endBand] = q_value

        # Imaginaty part: img(fft)
        data = np.imag(freqFrame[beginBand:endBand])
        q_value, _ = quantimaxmin(data, n_bits, max_amplitude, -max_amplitude)
        QfreqFrame_img[beginBand:endBand] = q_value*1j

        beginBand = endBand
    QfreqFrame = QfreqFrame_real+QfreqFrame_img
    return QfreqFrame


# Parameters:
#   - nBands: number of bands that the frame signal will be divided
# 	- freqFrame: fft reduced signal
#   - n_bits: number of bits to quantized sample
#   - numbits: Variable with the length of the bitstream coded
#   - energyThreshold: threshold to Quantize the bands with more info
# Return:
#   - QfreqFrame: Recover amplitud of the frame
#   - numbts: Variable with the length of the bitstream coded
def variable_quantization(nBands, freqFrame, n_bits, numbits, energyThreshold):
    N = len(freqFrame)
    QfreqFrame = np.zeros(N, dtype=complex)
    QfreqFrame_real = np.zeros(N)
    QfreqFrame_img = np.zeros(N, dtype=complex)
    beginBand = 0

    for iBand in range(0, nBands):
        endBand = int(N/pow(2, nBands-iBand))

        max_amplitude = np.sqrt(N/pow(2, iBand))

        # Coder
        if max(np.abs(freqFrame)) > (max_amplitude/energyThreshold):
            # Real part: real(fft)
            data_real = np.real(freqFrame[beginBand:endBand])
            _, Qlevel_real = quantimaxmin(data_real, n_bits, max_amplitude, -max_amplitude)
            numbits = numbits + n_bits*len(data_real)

            # Imaginary part: img(fft)
            data_img = np.imag(freqFrame[beginBand:endBand])
            _, Qlevel_img = quantimaxmin(data_img, n_bits, max_amplitude, -max_amplitude)
            numbits = numbits + n_bits*len(data_img)

            reciveBand = True
        else:
            numbits = numbits+1
            reciveBand = False

        # Decoder
        if(reciveBand):
            # Real part
            QAmp = dequanti(Qlevel_real, n_bits, max_amplitude, -max_amplitude)
            QfreqFrame_real[beginBand:endBand] = QAmp

            # Imaginaty part
            QAmp = dequanti(Qlevel_img, n_bits, max_amplitude, -max_amplitude)
            QfreqFrame_img[beginBand:endBand] = QAmp*1j

        beginBand = endBand

    QfreqFrame = QfreqFrame_real+QfreqFrame_img

    return QfreqFrame, numbits
