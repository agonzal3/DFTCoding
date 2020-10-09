# Sub-band Coding based on FFT

## Description
The goal of this project is to simulate the coding that would have sended audio signal, also when we zip the files and other processes. Based in the DFT (Discrete Fourier Transform) to bands.
This was a project for the university where I had to pass Matlab code to a Python code. 
It is done in python and in Jupyter notebook.

## Installation
Once you have downloaded all the projects, you need to be sure to have python3 and all the packages required.

To install the packages:
````
pip install name_package
````
If you want to open the Main_Lab2.ipynb, here you have the link to install [Jupyter notebook](https://jupyter.org/install), but you also have to instal the other packages.

## Project
The project is divided in different steps:
- Initialization
- **Ex 1:** Transform Block
- **Ex 2 & 3:** Quantization bands with no overlapping
- **Ex 4:** Quantization bands with overlapping and a window
- **Ex 5:** Variable Quantization Bands

### Ex 1
There is the base of the transformation block, as the audio signal isn't constant, it will divide the signal in frames with a determined size. In every frame, it will do the FFT (Fast Fourier Transform) to be in frequency and reduce the data. 
At this point we will recover the signal. So it will increase the data and apply the IFFT (Inverse FFT). And join all the frames. In the following image we have a great representation of the process.

![Transform Block](/Images/TransformBlock.png)

This process is done in the **function** ``transform`` of the ``block_transform`` **class**.

### Ex 2 i 3
The program has been improved and now does the Quantization Process.

![Quantization Band](/Images/QuantizationBand.PNG)

With the following metrics for the bands:

![Quantization Bands](/Images/QuantizationBnads.PNG)

This process is done in the **function** ``quantization`` of the ``quantization`` **class**.

### Ex 4
Now the final result is more accurate because we overlap the frames with specific windows, in my case with the Hamming window.

![Overlaped Band](/Images/OverlapedBand.PNG)

### Ex 5
In this process instead of using so much data we reduce it, with the condition that if there isn't enough information it isn’t necessary to quantize.
````
Max(fft) > max_amplitude/energyThreshold
````

![Variable Quantization](/Images/VariableQuantization.PNG)


This process is done in the **function** ``variable_quantization`` of the ``quantization`` **class**.

## Usage
To run the project you just have to open your terminal, go to the project directory (DFTCoding), and write the following command:
````
python3 main.py
````
Once you have run it, you can listen to the generated *".wav"* files in the project folder.
If you want to edit it or analyze it deeper, you will only need an editor, in my case I’ve used **Atom** to create the files.

In the case that you want to open with **Jupyter notebook**, you just have to open the terminal and go to the *DFTCoding* folder. And once you are located in the folder write the next line in the terminal:
````
jupyter notebook
````
