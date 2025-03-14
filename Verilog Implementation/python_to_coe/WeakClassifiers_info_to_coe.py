import numpy as np

# Define the values
# [threshold, left node, right node]
# stage 1 weak classifiers
wclassifier1_info = np.array([2, 9, -10])
wclassifier2_info = np.array([5, 3, -2])
wclassifier3_info = np.array([6, 7, -8])

# stage 2 weak_classifiers
wclassifier_1_info = np.array([2, 11, -10])
wclassifier_2_info = np.array([5, 8, -2])
wclassifier_3_info = np.array([6, 2, -8])
wclassifier_4_info = np.array([4, 6, -3])
wclassifier_5_info = np.array([9,12,-11])

#stage 3 weak classifiers
wclassifier__1_info = np.array([3, 7, -5])
wclassifier__2_info = np.array([8, 2, -16])

# Combine the classifiers into an array for easy processing
classifiers_info = np.array([wclassifier1_info, wclassifier2_info, wclassifier3_info,wclassifier_1_info,wclassifier_2_info,wclassifier_3_info,wclassifier_4_info,wclassifier_5_info,wclassifier__1_info,wclassifier__2_info])

def to_twos_complement(value, bit_width):
    """Convert a signed integer to its two's complement binary representation with bit_width bits."""
    if value < 0:
        value = (1 << bit_width) + value  # Compute two's complement for negative numbers
    return f'{value:0{bit_width}b}'

def write_classifiers_to_coe(classifiers_info, filename, bit_width=16):
    # Open the .coe file for writing
    with open(filename, 'w') as f:
        # Write the header
        f.write("memory_initialization_radix=2;\n")
        f.write("memory_initialization_vector=\n")
        
        # Convert each weak classifier's info to binary and write as one line
        for classifier in classifiers_info:
            bin_values = ''.join(to_twos_complement(value, bit_width) for value in classifier)
            f.write(bin_values + ',\n')
        
        # Replace the last comma with a semicolon
        f.seek(f.tell() - 2, 0)
        f.write(';\n')

# Write the weak classifier info to a .coe file
write_classifiers_to_coe(classifiers_info, 'weak_classifiers.coe')
