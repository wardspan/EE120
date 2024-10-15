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

    fig, axs = plt.subplots(num_signals + 1, 1, figsize=(10, 2 * (num_signals + 1)), sharex=True)

    # Plot clock signal
    axs[0].step(t, clock, where='mid', label='Clock', color='blue')
    axs[0].set_ylim([-0.5, 1.5])
    axs[0].set_yticks([0, 1])
    axs[0].set_ylabel("Clock")
    axs[0].grid(True)

    # Plot each output signal (Q0, Q1, Q2, Q3)
    for i, signal in enumerate(signals):
        axs[i + 1].step(t, signal, where='mid', label=signal_names[i], color='green')
        axs[i + 1].set_ylim([-0.5, 1.5])
        axs[i + 1].set_yticks([0, 1])
        axs[i + 1].set_ylabel(signal_names[i])
        axs[i + 1].grid(True)

    axs[-1].set_xlabel("Time")
    plt.tight_layout()
    plt.show()

# Function to simulate the behavior of the shift register based on its type
def simulate_shift_register(clock, periods, steps_per_period, register_type, use_complement):
    # Initialize Q0, Q1, Q2, Q3 as low (0)
    Q0 = [0] * len(clock)
    Q1 = [0] * len(clock)
    Q2 = [0] * len(clock)
    Q3 = [0] * len(clock)

    # Initial data input to Q0
    data_input = 1  # This is the data we are shifting through the register

    for i in range(1, len(clock)):
        if clock[i-1] == 0 and clock[i] == 1:  # Rising edge detected
            # Shift the values from Q0 to Q3 on the rising edge
            for j in range(i, len(clock)):  # Update from the current clock step to the end
                Q3[j] = Q2[i-1]  # Q3 takes the value of Q2
                Q2[j] = Q1[i-1]  # Q2 takes the value of Q1
                Q1[j] = Q0[i-1]  # Q1 takes the value of Q0
                Q0[j] = data_input  # Q0 takes the new data input (assumed to be 1 here)

    return Q0, Q1, Q2, Q3

# Function to get user inputs for clock parameters and register type, with added descriptions
def get_user_inputs():
    periods = int(input("Enter the number of clock periods to simulate: "))
    steps_per_period = int(input("Enter the resolution per period (higher = smoother): "))
    duty_cycle = float(input("Enter the clock duty cycle (e.g., 0.5 for 50%): "))
    
    # Get the initial clock state (high or low)
    clock_start = input("Should the clock start high? (y/n): ").lower() == 'y'
    
    # Define and show the register types with descriptions
    print("\nRegister Types:")
    print("1. SISO (Serial-In Serial-Out): Data is shifted in serially, and output is read serially.")
    print("2. SIPO (Serial-In Parallel-Out): Data is shifted in serially, but all outputs are updated in parallel.")
    print("3. PISO (Parallel-In Serial-Out): Data is loaded into the register in parallel but is output serially.")
    print("4. PIPO (Parallel-In Parallel-Out): Data is both loaded and read out in parallel.")
    
    # Get the type of register from the user
    register_type = input("Enter the type of shift register (SISO, SIPO, PISO, PIPO): ").upper()

    # Ask if complement output should be used
    use_complement = input("Use complement output (bar(Q))? (y/n): ").lower() == 'y'
    
    return periods, steps_per_period, duty_cycle, clock_start, register_type, use_complement

# Get user inputs for the clock and register parameters
periods, steps_per_period, duty_cycle, clock_start, register_type, use_complement = get_user_inputs()

# Generate the clock signal (starting in the user-defined state, high or low)
clock = generate_clock_signal(periods, steps_per_period, duty_cycle, start_high=clock_start)

# Simulate the shift register behavior based on the user-selected type
Q0, Q1, Q2, Q3 = simulate_shift_register(clock, periods, steps_per_period, register_type, use_complement)

# Signals list
signals = [Q0, Q1, Q2, Q3]
signal_names = ['Q0', 'Q1', 'Q2', 'Q3']

# Plot the timing diagram
plot_timing_diagram(clock, signals, signal_names)