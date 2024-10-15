import matplotlib.pyplot as plt
import numpy as np

# Function to generate a clock signal starting in the low state
def generate_clock_signal(periods, steps_per_period, duty_cycle=0.5):
    clock = []
    low_steps = int(steps_per_period * (1 - duty_cycle))  # Low part comes first
    high_steps = steps_per_period - low_steps  # Remaining part is high
    for _ in range(periods):
        clock.extend([0] * low_steps + [1] * high_steps)  # Low state first, then high
    return clock

# Function to create a timing diagram for the given signals
def plot_timing_diagram(clock, signals, signal_names):
    t = np.arange(len(clock))  # Time steps
    num_signals = len(signals)

    fig, axs = plt.subplots(num_signals + 1, 1, figsize=(10, 2 * (num_signals + 1)), sharex=True)

    # Plot clock signal
    axs[0].step(t, clock, where='mid', label='Clock', color='blue')
    axs[0].set_ylim([-0.5, 1.5])
    axs[0].set_yticks([0, 1])
    axs[0].set_ylabel("Clock")
    axs[0].grid(True)

    # Plot each output signal
    for i, signal in enumerate(signals):
        axs[i + 1].step(t, signal, where='mid', label=signal_names[i], color='green')
        axs[i + 1].set_ylim([-0.5, 1.5])
        axs[i + 1].set_yticks([0, 1])
        axs[i + 1].set_ylabel(signal_names[i])
        axs[i + 1].grid(True)

    axs[-1].set_xlabel("Time")
    plt.tight_layout()
    plt.show()

# Function to get user inputs for clock parameters
def get_user_inputs():
    periods = int(input("Enter the number of clock periods to simulate: "))
    steps_per_period = int(input("Enter the resolution per period (higher = smoother): "))
    duty_cycle = float(input("Enter the clock duty cycle (e.g., 0.5 for 50%): "))
    
    return periods, steps_per_period, duty_cycle

# Get user inputs for the clock
periods, steps_per_period, duty_cycle = get_user_inputs()

# Generate the clock signal (starting in the low state)
clock = generate_clock_signal(periods, steps_per_period, duty_cycle)

# Define signals for Q0, Q1, Q2, Q3 (you can customize these based on your circuit's logic)
# Simulating simple sequential rising signals
Q0 = [0] * steps_per_period + [1] * steps_per_period * (periods - 1)
Q1 = [0] * steps_per_period * 2 + [1] * steps_per_period * (periods - 2)
Q2 = [0] * steps_per_period * 3 + [1] * steps_per_period * (periods - 3)
Q3 = [0] * steps_per_period * 4 + [1] * steps_per_period * (periods - 4)

# Signals list
signals = [Q0, Q1, Q2, Q3]
signal_names = ['Q0', 'Q1', 'Q2', 'Q3']

# Plot the timing diagram
plot_timing_diagram(clock, signals, signal_names)