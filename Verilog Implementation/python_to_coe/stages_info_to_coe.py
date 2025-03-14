import numpy as np

# Define the values
# [#weak_classifiers, starting address]
stage1_info = np.array([3, 0])
stage2_info = np.array([5, 3])
stage3_info = np.array([2, 8])

# Combine the classifiers into an array for easy processing
stages_info = np.array([stage1_info, stage2_info, stage3_info])

def to_twos_complement(value, bit_width):
    """Convert a signed integer to its two's complement binary representation with bit_width bits."""
    if value < 0:
        value = (1 << bit_width) + value  # Compute two's complement for negative numbers
    return f'{value:0{bit_width}b}'

def write_stages_to_coe(stages_info, filename, bit_width=16):
    # Open the .coe file for writing
    with open(filename, 'w') as f:
        # Write the header
        f.write("memory_initialization_radix=2;\n")
        f.write("memory_initialization_vector=\n")
        
        # Convert each weak classifier's info to binary and write as one line
        lines = []
        for stage in stages_info:
            bin_values = ''.join(to_twos_complement(value, bit_width) for value in stage)
            lines.append(bin_values)
        
        # Join lines with commas, then add a semicolon at the end
        f.write(',\n'.join(lines) + ';\n')

# Write the weak classifier info to a .coe file
write_stages_to_coe(stages_info, 'stages_info.coe')
