import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# 1. Création d'un signal de référence
def create_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t)
    return signal

# 1.c. Quantifier ce signal en utilisant différentes résolutions
def quantize_signal(signal, bits):
    levels = 2 ** bits
    quantized_signal = np.round(signal * (levels // 2 - 1)).astype(np.int8)
    return quantized_signal

# 2. Simuler la latence d'un réseau fonctionnant en mode paquet
def simulate_network_latency(signal, sample_rate, packet_size, latencies):
    packets = [signal[i:i + packet_size] for i in range(0, len(signal), packet_size)]
    delayed_signal = np.zeros_like(signal)
    for i, packet in enumerate(packets):
        start_index = i * packet_size
        delay = latencies[i % len(latencies)]
        delayed_signal[start_index:start_index + packet_size] = np.roll(packet, delay)
    return delayed_signal

# 3. Simuler la perte de paquets
def simulate_packet_loss(signal, sample_rate, packet_size, loss_probability):
    packets = [signal[i:i + packet_size] for i in range(0, len(signal), packet_size)]
    lost_signal = np.zeros_like(signal)
    for i, packet in enumerate(packets):
        if np.random.rand() > loss_probability:
            start_index = i * packet_size
            lost_signal[start_index:start_index + packet_size] = packet
    return lost_signal

# Main function to execute the steps
def main():
    # 1.a. Créer une tonalité sinusoïdale de fréquence 2kHz, de 3 sec de durée
    frequency = 2000  # 2kHz
    duration = 3  # 3 seconds
    sample_rate = frequency * 10  # 10 samples per period
    signal = create_sine_wave(frequency, duration, sample_rate)

    # Reproduire cette tonalité sur les haut-parleurs de votre ordinateur
    sd.play(signal, sample_rate)
    sd.wait()

    # 1.b. Quantifier ce signal en (int) à 8 bits/éch
    quantized_signal_8bit = np.round(signal * 127).astype(np.int8)

    # Quantifier ce signal en utilisant différentes résolutions
    quantized_signal_6bit = quantize_signal(signal, 6)
    quantized_signal_4bit = quantize_signal(signal, 4)
    quantized_signal_3bit = quantize_signal(signal, 3)
    quantized_signal_2bit = quantize_signal(signal, 2)
    quantized_signal_1bit = quantize_signal(signal, 1)

    # Simuler la latence d'un réseau fonctionnant en mode paquet
    latencies = [0, 1, 2, 3, 4]  # Different transmission delays
    packet_size = 2  # 2 samples per packet
    delayed_signal = simulate_network_latency(quantized_signal_8bit, sample_rate, packet_size, latencies)

    # Simuler la perte de paquets
    loss_probability_1 = 10**-3
    loss_probability_2 = 10**-2
    lost_signal_1 = simulate_packet_loss(quantized_signal_8bit, sample_rate, packet_size, loss_probability_1)
    lost_signal_2 = simulate_packet_loss(quantized_signal_8bit, sample_rate, packet_size, loss_probability_2)

    slice_length = 200

    # Plotting the signals for visualization
    plt.figure(figsize=(15, 18))

    plt.subplot(8, 1, 1)
    plt.plot(signal[:slice_length], label='Original Signal')
    plt.legend()

    plt.subplot(8, 1, 2)
    plt.plot(quantized_signal_6bit[:slice_length], label='Quantized Signal (6-bit)')
    plt.legend()

    plt.subplot(8, 1, 3)
    plt.plot(quantized_signal_4bit[:slice_length], label='Quantized Signal (4-bit)')
    plt.legend()

    plt.subplot(8, 1, 4)
    plt.plot(quantized_signal_3bit[:slice_length], label='Quantized Signal (3-bit)')
    plt.legend()

    plt.subplot(8, 1, 5)
    plt.plot(quantized_signal_2bit[:slice_length], label='Quantized Signal (2-bit)')
    plt.legend()

    plt.subplot(8, 1, 6)
    plt.plot(quantized_signal_1bit[:slice_length], label='Quantized Signal (1-bit)')
    plt.legend()

    plt.subplot(8, 1, 7)
    plt.plot(delayed_signal[:slice_length], label='Delayed Signal')
    plt.legend()

    plt.subplot(8, 1, 8)
    plt.plot(lost_signal_1[:slice_length], label='Lost Signal (p=10^-3)')
    plt.plot(lost_signal_2[:slice_length], label='Lost Signal (p=10^-2)')
    plt.legend()

    plt.show()

if __name__ == "__main__":
    main()