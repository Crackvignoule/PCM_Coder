import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# 1. Création d'un signal de référence
def create_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t)
    return signal

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

# 1.c. Quantifier ce signal en utilisant différentes résolutions
def quantize_signal(signal, bits):
    levels = 2 ** bits
    quantized_signal = np.round(signal * (levels // 2 - 1)).astype(np.int8)
    return quantized_signal

quantized_signal_6bit = quantize_signal(signal, 6)
quantized_signal_4bit = quantize_signal(signal, 4)
quantized_signal_3bit = quantize_signal(signal, 3)
quantized_signal_2bit = quantize_signal(signal, 2)

# 1.d. Quantifier ce signal en utilisant une résolution de 1 bit/éch
quantized_signal_1bit = quantize_signal(signal, 1)

# 2. Simuler la latence d'un réseau fonctionnant en mode paquet
def simulate_network_latency(signal, sample_rate, packet_size, latencies):
    packets = [signal[i:i + packet_size] for i in range(0, len(signal), packet_size)]
    delayed_signal = np.zeros_like(signal)
    for i, packet in enumerate(packets):
        start_index = i * packet_size
        delay = latencies[i % len(latencies)]
        delayed_signal[start_index:start_index + packet_size] = np.roll(packet, delay)
    return delayed_signal

latencies = [0, 1, 2, 3, 4]  # Different transmission delays
packet_size = 2  # 2 samples per packet
delayed_signal = simulate_network_latency(quantized_signal_8bit, sample_rate, packet_size, latencies)

# 3. Simuler la perte de paquets
def simulate_packet_loss(signal, sample_rate, packet_size, loss_probability):
    packets = [signal[i:i + packet_size] for i in range(0, len(signal), packet_size)]
    lost_signal = np.zeros_like(signal)
    for i, packet in enumerate(packets):
        if np.random.rand() > loss_probability:
            start_index = i * packet_size
            lost_signal[start_index:start_index + packet_size] = packet
    return lost_signal

loss_probability_1 = 10**-3
loss_probability_2 = 10**-2
lost_signal_1 = simulate_packet_loss(quantized_signal_8bit, sample_rate, packet_size, loss_probability_1)
lost_signal_2 = simulate_packet_loss(quantized_signal_8bit, sample_rate, packet_size, loss_probability_2)

# Plotting the signals for visualization
plt.figure(figsize=(15, 10))
plt.subplot(3, 1, 1)
plt.plot(signal[:1000], label='Original Signal')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(delayed_signal[:1000], label='Delayed Signal')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(lost_signal_1[:1000], label='Lost Signal (p=10^-3)')
plt.plot(lost_signal_2[:1000], label='Lost Signal (p=10^-2)')
plt.legend()

plt.show()