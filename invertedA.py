import matplotlib.pyplot as plt
import numpy as np

# Define the time range for the signals
time = np.linspace(0, 10, 1000)

# Define the original signals A and B based on the waveform description
# Here, A and B are created as square waves with different frequencies
A = np.where((np.sin(2 * np.pi * 0.5 * time) > 0), 1, 0)  # Signal A (lower frequency)
B = np.where((np.sin(2 * np.pi * 1.5 * time) > 0), 1, 0)  # Signal B (higher frequency)

# Inverted A
A_inverted = 1 - A

# Output Z: Assuming AND gate operation with A and B
Z = A & B

# Z with Inverted A: AND operation between Inverted A and B
Z_inverted_A = A_inverted & B

# Plotting the signals
plt.figure(figsize=(12, 10))

# Plot A
plt.subplot(4, 1, 1)
plt.plot(time, A, label='A', color='blue')
plt.ylim(-0.5, 1.5)
plt.title('Signal A')
plt.grid(True)

# Plot B
plt.subplot(4, 1, 2)
plt.plot(time, B, label='B', color='orange')
plt.ylim(-0.5, 1.5)
plt.title('Signal B')
plt.grid(True)

# Plot Inverted A
plt.subplot(4, 1, 3)
plt.plot(time, A_inverted, label='Inverted A', color='red')
plt.ylim(-0.5, 1.5)
plt.title('Inverted A')
plt.grid(True)

# Plot Z and Z with Inverted A
plt.subplot(4, 1, 4)
plt.plot(time, Z, label='Z (A AND B)', color='green')
plt.plot(time, Z_inverted_A, label='Z with Inverted A (Inverted A AND B)', color='purple', linestyle='--')
plt.ylim(-0.5, 1.5)
plt.title('Output Z and Z with Inverted A')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()