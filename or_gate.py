import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Time period for the signals
time = np.linspace(0, 10, 1000)

# Defining the input signals A and B as square waves for illustration
A = np.where((np.sin(2 * np.pi * 0.5 * time) > 0), 1, 0)  # Signal A (low frequency)
B = np.where((np.sin(2 * np.pi * 1.5 * time) > 0), 1, 0)  # Signal B (higher frequency)

# OR gate output (Z)
Z_or = A | B  # Logical OR operation

# Create a table (truth table style) for time, A, B, and Z (OR gate)
data = {
    'Time': time,
    'A': A,
    'B': B,
    'Z (A OR B)': Z_or
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display the first few rows of the table
print(df.head(10))

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

# Plot Z (output of OR gate)
plt.subplot(3, 1, 3)
plt.plot(time, Z_or, label='Z (A OR B)', color='green')
plt.ylim(-0.5, 1.5)
plt.title('Output Z (A OR B)')
plt.grid(True)

plt.tight_layout()
plt.show()