import numpy as np

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