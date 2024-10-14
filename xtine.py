import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# 1. Création d'un signal de référence (par exemple, une tonalité sinusoïdale)
def create_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t)
    return signal

frequency = 2000  # 2kHz
duration = 3  # 3 seconds
sample_rate = 44100  # Standard audio sample rate
signal = create_sine_wave(frequency, duration, sample_rate)

# 2. Quantifier le signal en utilisant une résolution de 8 bits/éch
quantized_signal_8bit = np.round(signal * 127).astype(np.int8)

# 3. Créer des paquets de 4 octets
packet_size = 4  # 4 bytes per packet
packets = [quantized_signal_8bit[i:i + packet_size] for i in range(0, len(quantized_signal_8bit), packet_size)]

# 4. Simuler la perte de paquets
def simulate_packet_loss(packets, loss_probability):
    lost_packets = []
    for packet in packets:
        if np.random.rand() > loss_probability:
            lost_packets.append(packet)
        else:
            lost_packets.append(np.zeros_like(packet))  # Simulate lost packet with zeros
    return np.concatenate(lost_packets)

loss_probability = 0.1  # 10% packet loss probability
lost_signal = simulate_packet_loss(packets, loss_probability)

# 5. Calculer le taux de pertes de blocs de 4 octets
total_packets = len(packets)
lost_packets_count = sum(1 for packet in packets if np.array_equal(packet, np.zeros_like(packet)))
loss_rate = lost_packets_count / total_packets

# Reproduire le signal perdu sur les haut-parleurs de votre ordinateur
sd.play(lost_signal, sample_rate)
sd.wait()

slice_length = 200

# Afficher les signaux pour visualisation
plt.figure(figsize=(15, 5))
plt.subplot(2, 1, 1)
plt.plot(quantized_signal_8bit[:slice_length], label='Quantized Signal (8-bit)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(lost_signal[:slice_length], label='Lost Signal (10% packet loss)')
plt.legend()

plt.show()

print(f"Taux de pertes de blocs de 4 octets : {loss_rate * 100:.2f}%")