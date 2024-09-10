import matplotlib.pyplot as plt
import numpy as np

# Time period for the signals
time = np.linspace(0, 10, 1000)

# Defining the input signals A and B as square waves for illustration
A = np.where((np.sin(2 * np.pi * 0.5 * time) > 0), 1, 0)  # Signal A (low frequency)
B = np.where((np.sin(2 * np.pi * 1.5 * time) > 0), 1, 0)  # Signal B (higher frequency)

# AND gate output (Z)
Z = A & B  # Logical AND operation

# Plotting the signals
plt.figure(figsize=(10, 6))

# Plot A
plt.subplot(3, 1, 1)
plt.plot(time, A, label='A', color='blue')
plt.ylim(-0.5, 1.5)
plt.title('Signal A')
plt.grid(True)

# Plot B
plt.subplot(3, 1, 2)
plt.plot(time, B, label='B', color='orange')
plt.ylim(-0.5, 1.5)
plt.title('Signal B')
plt.grid(True)

# Plot Z (output of AND gate)
plt.subplot(3, 1, 3)
plt.plot(time, Z, label='Z (A AND B)', color='green')
plt.ylim(-0.5, 1.5)
plt.title('Output Z (A AND B)')
plt.grid(True)

plt.tight_layout()
plt.show()