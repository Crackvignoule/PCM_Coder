import numpy as np
import matplotlib.pyplot as plt

def create_sine_wave(frequency, duration, sample_rate):
    """ Create a sine wave with the given frequency, duration and sample rate """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t)
    return t, signal

def quantize_signal(signal, bits):
    """ Quantize the signal to the given number of bits """
    levels = 2 ** bits
    quantized_signal = np.round(signal * (levels // 2 - 1)).astype(np.int8)
    return quantized_signal

def encode_signal(signal, encoding_type="PCM"):
    """ Encode the signal using PCM or DPCM """
    if encoding_type.capitalize() == "DPCM":
        return np.diff(signal, prepend=signal[0])
    return signal

def decode_signal(encoded_signal, encoding_type="PCM"):
    """ Decode the signal using PCM or DPCM """
    if encoding_type.capitalize() == "DPCM":
        return np.cumsum(encoded_signal)
    return encoded_signal

def simulate_network_latency(signal, packet_size, latencies):
    """ Simulate network latency by delaying packets in the signal """
    packets = [signal[i:i + packet_size] for i in range(0, len(signal), packet_size)]
    delayed_signal = np.zeros_like(signal)
    for i, packet in enumerate(packets):
        start_index = i * packet_size
        delay = latencies[i % len(latencies)]
        delayed_signal[start_index:start_index + packet_size] = np.roll(packet, delay)
    return delayed_signal

def simulate_packet_loss(signal, packet_size, loss_probability):
    """ Simulate packet loss by dropping packets in the signal """
    packets = [signal[i:i + packet_size] for i in range(0, len(signal), packet_size)]
    lost_signal = np.zeros_like(signal)
    for i, packet in enumerate(packets):
        if np.random.rand() > loss_probability:
            start_index = i * packet_size
            lost_signal[start_index:start_index + packet_size] = packet
    return lost_signal

def plot_signal_subplot(position, t_slice, original_signal, quantized_signal, label, nrow=4, ncol=2, norm=True, show_error=True, tolerance=1e-3):
    plt.subplot(nrow, ncol, position)
    plt.plot(t_slice, original_signal, label='Original Signal')
    
    # Normalize quantized signal if norm is True and max value is not zero
    if norm and np.max(quantized_signal) != 0:
        quantized_signal = quantized_signal / np.max(quantized_signal)
    
    plt.plot(t_slice, quantized_signal, label=label, linestyle='--')
    
    if show_error:
        error_plotted = False
        for t_val, orig, quant in zip(t_slice, original_signal, quantized_signal):
            if abs(orig - quant) > tolerance:
                plt.plot(t_val, quant, 'ro', label='Error' if not error_plotted else "")  # Red dot at the quantized point
                plt.vlines(t_val, orig, quant, colors='r', linestyles='dotted')  # Vertical line
                error_plotted = True
    
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.legend()