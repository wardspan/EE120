import matplotlib.pyplot as plt
import numpy as np


# Function to generate a clock signal, starting in user-defined state (high or low)
def generate_clock_signal(periods, steps_per_period, duty_cycle=0.5, start_high=False):
    clock = []
    if start_high:
        high_steps = int(steps_per_period * duty_cycle)
        low_steps = steps_per_period - high_steps
        for _ in range(periods):
            clock.extend([1] * high_steps + [0] * low_steps)  # High first, then low
    else:
        low_steps = int(steps_per_period * (1 - duty_cycle))  # Low part comes first
        high_steps = steps_per_period - low_steps  # Remaining part is high
        for _ in range(periods):
            clock.extend([0] * low_steps + [1] * high_steps)  # Low first, then high
    return clock


# Function to create the timing diagram for the shift register
def plot_timing_diagram(clock, signals, signal_names):
    t = np.arange(len(clock))  # Time steps
    num_signals = len(signals)

    fig, axs = plt.subplots(
        num_signals + 1, 1, figsize=(10, 2 * (num_signals + 1)), sharex=True
    )

    # Plot clock signal
    axs[0].step(t, clock, where="mid", label="Clock", color="blue")
    axs[0].set_ylim([-0.5, 1.5])
    axs[0].set_yticks([0, 1])
    axs[0].set_ylabel("Clock")
    axs[0].grid(True)

    # Plot each output signal (Q0, Q1, Q2, Q3)
    for i, signal in enumerate(signals):
        axs[i + 1].step(t, signal, where="mid", label=signal_names[i], color="green")
        axs[i + 1].set_ylim([-0.5, 1.5])
        axs[i + 1].set_yticks([0, 1])
        axs[i + 1].set_ylabel(signal_names[i])
        axs[i + 1].grid(True)

    axs[-1].set_xlabel("Time")
    plt.tight_layout()
    plt.show()


# Function to simulate a toggle flip-flop chain (binary counter shift register)
def simulate_toggle_register(clock, periods, steps_per_period):
    # Initialize Q0, Q1, Q2, Q3 as low (0)
    Q0 = [0] * len(clock)
    Q1 = [0] * len(clock)
    Q2 = [0] * len(clock)
    Q3 = [0] * len(clock)

    for i in range(1, len(clock)):
        if clock[i - 1] == 0 and clock[i] == 1:  # Rising edge detected
            # Toggle each flip-flop based on the complement of the previous flip-flop
            Q0[i:] = 1 - Q0[i - 1]  # Q0 toggles on every clock edge
            Q1[i:] = (
                1 - Q1[i - 1] if Q0[i] == 0 else Q1[i - 1]
            )  # Q1 toggles every time Q0 goes low
            Q2[i:] = (
                1 - Q2[i - 1] if Q1[i] == 0 else Q2[i - 1]
            )  # Q2 toggles every time Q1 goes low
            Q3[i:] = (
                1 - Q3[i - 1] if Q2[i] == 0 else Q3[i - 1]
            )  # Q3 toggles every time Q2 goes low

    return Q0, Q1, Q2, Q3


# Function to get user inputs for clock parameters
def get_user_inputs():
    periods = int(input("Enter the number of clock periods to simulate: "))
    steps_per_period = int(
        input("Enter the resolution per period (higher = smoother): ")
    )
    duty_cycle = float(input("Enter the clock duty cycle (e.g., 0.5 for 50%): "))

    # Get the initial clock state (high or low)
    clock_start = input("Should the clock start high? (y/n): ").lower() == "y"

    return periods, steps_per_period, duty_cycle, clock_start


# Get user inputs for the clock and register parameters
periods, steps_per_period, duty_cycle, clock_start = get_user_inputs()

# Generate the clock signal (starting in the user-defined state, high or low)
clock = generate_clock_signal(
    periods, steps_per_period, duty_cycle, start_high=clock_start
)

# Simulate the toggle register behavior (binary counter)
Q0, Q1, Q2, Q3 = simulate_toggle_register(clock, periods, steps_per_period)

# Signals list
signals = [Q0, Q1, Q2, Q3]
signal_names = ["Q0", "Q1", "Q2", "Q3"]

# Plot the timing diagram
plot_timing_diagram(clock, signals, signal_names)
