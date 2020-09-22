# Intro script of Adria Hermini Gonzalez 10/04/2020
# Pompeu Fabra University student
# This code it have been developed for a practice
# Subject: Audio Encoding Sistem
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import soundfile as sf
from block_transform import transform, transform_overlap
import sounddevice as sd
import math

# -------------------Inisialization------------------------------------------

# Read the auido file
audio, fsaudio = sf.read('wavs/es01_m44.wav')
# Create the time array corresponding with the aduio
time = np.linspace(0, (len(audio)-1)/fsaudio, num=len(audio-1))

# Play the sound
# sd.play(audio, fsaudio)
# status = sd.wait()  # Wait until file is done playing

# Plot of the audio
plt.plot(time, audio)
plt.title('Forma Audio')
plt.xlabel('Segons')
plt.ylabel('Amplitud')
plt.show()

winL = 1024
nBands = 5
n_bits = 8


# -------------------------Ex 1 ---------------------------------------------
# Plot a part of the signal in time, magnitud and phase
doQuantizationByBands = 0
waveOut = transform(audio, nBands, n_bits, winL, doQuantizationByBands, time)

# Compare plot of the original and final signal
fig1, (mX, nX) = plt.subplots(2, 1)
mX.plot(time, audio)
mX.set_title('Original')
nX.plot(time, waveOut, 'r')
nX.set_title('WaveOut')
plt.xlabel('Segons')
plt.show()

'''
sd.play(waveOut, fsaudio)
status = sd.wait()
'''
wavfile.write("waveOut.wav", fsaudio, waveOut)

# --------------------------Ex 2 i 3 ----------------------------------------
# Quantization bands with no overlapping and rectangular window
doQuantizationByBands = 1
waveOut = transform(audio, nBands, n_bits, winL, doQuantizationByBands, time)

# Compute Bitrate
bitrate = n_bits*fsaudio
print('BITRATE exercici 3:', bitrate/1000, ' Kbits/s')

# Compare plot of the original and final signal
fig2, (mX, nX) = plt.subplots(2, 1)
mX.plot(time, audio)
mX.set_title('Original')
nX.plot(time, waveOut, 'r')
nX.set_title('WaveOut Quantized')
plt.xlabel('Segons')
plt.show()

'''
sd.play(waveOut, fsaudio)
status = sd.wait()
'''
wavfile.write("waveOut_quantized.wav", fsaudio, waveOut)


# ------------------------ Ex 4 ----------------------------
# Quantization bands with oberlapping and a hamming window
window = np.hanning(winL)
overlap = 0.75
waveOut, _ = transform_overlap(audio, nBands, n_bits, winL, overlap, window, doQuantizationByBands, False)

# Compute bitrate
num_windows = math.ceil(len(audio)/(winL*(1-overlap))) - int(1/(1-overlap))
nbits_total = n_bits * winL * num_windows
bitrate2 = (nbits_total * fsaudio) / len(audio)
print('BITRATE exercici 4 (Overlap-Add):', '%.2f' % (bitrate2/1000), 'Kbits/s')

# Compare plot of the original and final signal
fig2, (mX, nX) = plt.subplots(2, 1)
mX.plot(time, audio)
mX.set_title('Original')
nX.plot(time, waveOut, 'r')
nX.set_title('WaveOut Overlapp')
plt.xlabel('Segons')
plt.show()

'''
sd.play(waveOut, fsaudio)
status = sd.wait()
'''
wavfile.write("waveOut_Overlap.wav", fsaudio, waveOut)


# ------------------------- Ex 5 ------------------------------
# Variable Quantization Bands
doQuantizationByBands = 5
window = np.hanning(winL)
overlap = 0.75
energyThreshold = 5

waveOut, nbits_total = transform_overlap(audio, nBands, n_bits, winL, overlap, window, doQuantizationByBands, energyThreshold)

# Compute Bitrate
bitrate3 = (nbits_total * fsaudio) / len(audio)
print('BITRATE exercici 5 (Variable):', '%.2f' % (bitrate3/1000), 'Kbits/s')

# Compare plot of the original and final signal
fig3, (mX, nX) = plt.subplots(2, 1)
mX.plot(time, audio)
mX.set_title('Original')
nX.plot(time, waveOut, 'r')
nX.set_title('WaveOut Variable bit allocation')
plt.xlabel('Segons')
plt.show()
sd.play(waveOut, fsaudio)
status = sd.wait()
wavfile.write("waveOut_variable.wav", fsaudio, waveOut)
