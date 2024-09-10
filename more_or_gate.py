import matplotlib.pyplot as plt
import numpy as np

# Time period for the signals
time = np.linspace(0, 10, 1000)

# Defining the input signals A, B, and C as square waves with different frequencies
#A = np.where((np.sin(2 * np.pi * 0.5 * time) > 0), 1, 0)  # Signal A (medium frequency)

# Signal A shorted to ground (always 0)
#A = np.zeros_like(time, dtype=int)

# Signal A shorted to +5V (always 1)
A = np.ones_like(time, dtype=int)

B = np.where((np.sin(2 * np.pi * 1.5 * time) > 0), 1, 0)  # Signal B (higher frequency)
C = np.where((np.sin(2 * np.pi * 0.25 * time) > 0), 1, 0)  # Signal C (lower frequency)

# OR gate output (Z)
Z_or = A | B | C  # Logical OR operation of A, B, and C

# Plotting the signals
plt.figure(figsize=(12, 8))

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

# Plot C
plt.subplot(4, 1, 3)
plt.plot(time, C, label='C', color='red')
plt.ylim(-0.5, 1.5)
plt.title('Signal C')
plt.grid(True)

# Plot Z (output of OR gate)
plt.subplot(4, 1, 4)
plt.plot(time, Z_or, label='Z (A OR B OR C)', color='green')
plt.ylim(-0.5, 1.5)
plt.title('Output Z (A OR B OR C)')
plt.grid(True)

plt.tight_layout()
plt.show()
