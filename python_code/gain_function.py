import matplotlib.pyplot as plot
from math import *
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

resolution = 1024;
regularization_1 = 3.0  / 1024 * resolution      # Defines the speed of the control parameter to reach high compressions -> alpha
regularization_2 = 10.0 / 1024 * resolution     # Defines the maximum compression achieved, inversely -> beta

x_values = range(-resolution, resolution)
y_values = [0]*len(x_values);


control_parameter = 1024;  # Range: 0 - resolution



def process(input_sample, control_parameter):
    gain = (resolution + np.power(control_parameter, control_parameter / (resolution / 1.2)) * regularization_1 ) / (abs(input_sample) + np.power(control_parameter,  control_parameter / (resolution / 1.2)) * regularization_1 + regularization_2);

    return input_sample * gain



signal_length = 1000

input_signal = [0] * signal_length
output_signal_0 = [0] * signal_length
output_signal_1 = [0] * signal_length
output_signal_2 = [0] * signal_length
output_signal_3 = [0] * signal_length

for i in range(0, signal_length):
    input_signal[i] = sin(2 * np.pi * 1000 * i /48000) * 1024/2.0;
    output_signal_0[i] = process(input_signal[i], 0.0)
    output_signal_1[i] = process(input_signal[i], 600.0)
    output_signal_2[i] = process(input_signal[i], 800.0)
    output_signal_3[i] = process(input_signal[i], 1024.0)

fft_orig = 20*np.log(np.abs(np.fft.fft(np.divide(input_signal, 1024), signal_length)))
fft_0 = 20*np.log(np.abs(np.fft.fft(np.divide(output_signal_0, 1024), signal_length)))
fft_1 = 20*np.log(np.abs(np.fft.fft(np.divide(output_signal_1, 1024), signal_length)))
fft_2 = 20*np.log(np.abs(np.fft.fft(np.divide(output_signal_2, 1024), signal_length)))
fft_3 = 20*np.log(np.abs(np.fft.fft(np.divide(output_signal_3, 1024), signal_length)))

max_peak = np.max(fft_orig)
fft_orig = np.subtract(fft_orig, max_peak)
fft_0 = np.subtract(fft_0, max_peak)
fft_1 = np.subtract(fft_1, max_peak)
fft_2 = np.subtract(fft_2, max_peak)
fft_3 = np.subtract(fft_3, max_peak)

fft_orig = fft_orig[1:len(fft_orig)/2]
fft_0 = fft_0[1:len(fft_0)/2]
fft_1 = fft_1[1:len(fft_1)/2]
fft_2 = fft_2[1:len(fft_2)/2]
fft_3 = fft_3[1:len(fft_3)/2]

freq_axis = range(1, 48000, 48000/signal_length)
freq_axis = freq_axis[0:len(fft_orig)]

plot.ion()
plot.plot(freq_axis, fft_orig, linewidth=2)
plot.plot(freq_axis, fft_0)
plot.plot(freq_axis, fft_1)
plot.plot(freq_axis, fft_2)
plot.plot(freq_axis, fft_3)
plot.grid()
plot.xlim([0, 22000])
plot.ylim([-180, 50])
plot.xlabel('Frequency [Hz]')
plot.ylabel('Amplitude [dB]')
plot.title('Spectrum (module) produced from a 1 kHz input tone at -6 dBFS')
plot.legend(['Input signal', 'c = 0', 'c = 600', 'c = 800', 'c = 1024'], 'upper right')
plot.show()
pp = PdfPages('spectrums.pdf')
plot.savefig(pp, format='pdf')
pp.close()
plot.clf()

# Showing the waveforms
printed_length = 100
plot.ion()
plot.plot(input_signal[0 : printed_length])
plot.plot(output_signal_0[0 : printed_length])
plot.plot(output_signal_1[0 : printed_length])
plot.plot(output_signal_2[0 : printed_length])
plot.plot(output_signal_3[0 : printed_length])
plot.grid()
plot.xlabel('Time [samples]')
plot.ylabel('Amplitude [.]')
plot.ylim([-resolution, resolution])
plot.title('Waveforms produced from a 1 kHz input signal at -6 dBFS')
plot.legend(['Input signal', 'c = 0', 'c = 600', 'c = 800', 'c = 1024'])
plot.show()
pp = PdfPages('waveforms.pdf')
plot.savefig(pp, format='pdf')
pp.close()
plot.clf()

# This is for making a sweep of the control parameter and creating a plot
for control_parameter in [0, 150, 300, 450, 600, 750, 900, 1024]:
    for i in range(0, len(x_values)):
        gain = (resolution + np.power(control_parameter, control_parameter / (resolution / 1.2)) * regularization_1 ) / (abs(x_values[i]) + np.power(control_parameter,  control_parameter / (resolution / 1.2)) * regularization_1 + regularization_2);
        y_values[i] = x_values[i] * gain;
    
    plot.plot(x_values, y_values)

plot.ion()
plot.xlim([-resolution, resolution])
plot.ylim([-resolution, resolution])
plot.grid()
plot.xlabel('Input value - x[n]')
plot.ylabel('Output value - y[n]')
plot.legend(['c = 0', 'c = 150', 'c = 300', 'c = 450', 'c = 600', 'c = 750', 'c = 900', 'c = 1024'], 'upper left')
plot.title('Gain as a function of the control parameter')
plot.show()
pp = PdfPages('gain_function.pdf')
plot.savefig(pp, format='pdf')
pp.close()

quit()






# To generate an animated plot with the control parameter sweeping
plot.ion()
for control_parameter in range(resolution, 0, -resolution / 100):

    for i in range(0, len(x_values)):
        gain = (resolution + np.power(control_parameter, control_parameter / (resolution / 1.2)) * regularization_1 ) / (abs(x_values[i]) + np.power(control_parameter,  control_parameter / (resolution / 1.2)) * regularization_1 + regularization_2);
        y_values[i] = x_values[i] * gain;

    plot.plot(x_values, y_values)
    plot.xlim([-resolution, resolution])
    plot.ylim([-resolution, resolution])
    plot.grid()
    plot.title(str(control_parameter))
    plot.show()
    plot.pause(0.05)
    plot.clf()
