import pandas as pd
import itertools

# Define the number of inputs for the OR gate
num_inputs = 5

# Generate all possible combinations of 0 and 1 for 5 inputs
input_combinations = list(itertools.product([0, 1], repeat=num_inputs))

# Calculate the output for each combination using the OR operation
outputs = [int(any(combination)) for combination in input_combinations]

# Create a DataFrame to display the truth table
columns = [f"Input {i+1}" for i in range(num_inputs)] + ["Output"]
data = [list(combination) + [output] for combination, output in zip(input_combinations, outputs)]

# Create the DataFrame
truth_table = pd.DataFrame(data, columns=columns)

# Display the DataFrame
print(truth_table)

# Save the truth table to a CSV file
truth_table.to_csv('5_input_OR_gate_truth_table.csv', index=False)

print("Truth table saved as '5_input_OR_gate_truth_table.csv'.")