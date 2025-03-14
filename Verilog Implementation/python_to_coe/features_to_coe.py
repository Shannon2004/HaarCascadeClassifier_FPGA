import numpy as np

# stage 1 feature values---------------------------------------------------------------------

A1 = 20
B1 = 15
C1 = 20
D1 = 10
w1 = -1

A11 = 40
B11 = 30
C11 = 50
D11 = 20
w11 = -1

A12 = 20
B12 = 25
C12 = 10
D12 = 10
w12 = -1

A2 = 30
B2 = 40
C2 = 60
D2 = 70
w2 = 2

A21 = 20
B21 = 30
C21 = 40
D21 = 50
w21 = 1

A22 = 20
B22 = 30
C22 = 70
D22 = 80
w22 = 3

A3 = 40
B3 = 20
C3 = 25
D3 = 10
w3 = 1

A31 = 20
B31 = 30
C31 = 10
D31 = 15
w31 = -1

A32 = 10
B32 = 12
C32 = 14
D32 = 20
w32 = 1

# stage 2 feature values---------------------------------------------------------------------

A_1 = 20
B_1 = 15
C_1 = 10
D_1 = 10
w_1 = 1

A_11 = 40
B_11 = 30
C_11 = 10
D_11 = 20
w_11 = 1

A_12 = 20
B_12 = 15
C_12 = 10
D_12 = 20
w_12 = 1

A_13 = 20
B_13 = 10
C_13 = 40
D_13 = 10
w_13 = -1

A_14 = 20
B_14 = 30
C_14 = 10
D_14 = 45
w_14 = 1

A_2 = 30
B_2 = 60
C_2 = 40
D_2 = 70
w_2 = -2

A_21 = 20
B_21 = 30
C_21 = 40
D_21 = 50
w_21 = -1

A_22 = 20
B_22 = 30
C_22 = 70
D_22 = 80
w_22 = 3

A_23 = 15
B_23 = 30
C_23 = 20
D_23 = 10
w_23 = -1

A_24 = 20
B_24 = 30
C_24 = 10
D_24 = 45
w_24 = 1

A_3 = 40
B_3 = 60
C_3 = 70
D_3 = 10
w_3 = -1

A_31 = 20
B_31 = 30
C_31 = 10
D_31 = 40
w_31 = 1

A_32 = 10
B_32 = 12
C_32 = 14
D_32 = 10
w_32 = -1

A_33 = 40
B_33 = 10
C_33 = 50
D_33 = 10
w_33 = -1

A_34 = 20
B_34 = 30
C_34 = 10
D_34 = 45
w_34 = 1

# stage 3 feature values---------------------------------------------------------------------

A__1 = 25
B__1 = 35
C__1 = 15
D__1 = 20
w__1 = -1

A__11 = 20
B__11 = 15
C__11 = 35
D__11 = 10
w__11 = -2

A__2 = 20
B__2 = 15
C__2 = 20
D__2 = 15
w__2 = 2

A__12 = 20
B__12 = 15
C__12 = 20
D__12 = 10
w__12 = -1

A__3 = 15
B__3 = 10
C__3 = 20
D__3 = 15
w__3 = 1

A__13 = 20
B__13 = 15
C__13 = 20
D__13 = 25
w__13 = 1

int_img1 = np.array([[A1,B1,C1,D1,w1],[A11,B11,C11,D11,w11],[A12,B12,C12,D12,w12],[A_1,B_1,C_1,D_1,w_1],[A_11,B_11,C_11,D_11,w_11],[A_12,B_12,C_12,D_12,w_12],[A_13,B_13,C_13,D_13,w_13],[A_14,B_14,C_14,D_14,w_14],[A__1,B__1,C__1,D__1,w__1],[A__11,B__11,C__11,D__11,w__11]])
int_img2 = np.array([[A2,B2,C2,D2,w2],[A21,B21,C21,D21,w21],[A22,B22,C22,D22,w22],[A_2,B_2,C_2,D_2,w_2],[A_21,B_21,C_21,D_21,w_21],[A_22,B_22,C_22,D_22,w_22],[A_23,B_23,C_23,D_23,w_23],[A_24,B_24,C_24,D_24,w_24],[A__2,B__2,C__2,D__2,w__2],[A__12,B__12,C__12,D__12,w__12]])
int_img3 = np.array([[A3,B3,C3,D3,w3],[A31,B31,C31,D31,w31],[A32,B32,C32,D32,w32],[A_3,B_3,C_3,D_3,w_3],[A_31,B_31,C_31,D_31,w_31],[A_32,B_32,C_32,D_32,w_32],[A_33,B_33,C_33,D_33,w_33],[A_34,B_34,C_34,D_34,w_34],[A__3,B__3,C__3,D__3,w__3],[A__13,B__13,C__13,D__13,w__13]])


def to_twos_complement(value, bit_width):
    """Convert a signed integer to its two's complement binary representation with bit_width bits."""
    if value < 0:
        value = (1 << bit_width) + value  # Compute two's complement for negative numbers
    return f'{value:0{bit_width}b}'

def write_int_img_to_coe(int_img, filename, bit_width=16):
    # Open the .coe file for writing
    with open(filename, 'w') as f:
        # Write the header
        f.write("memory_initialization_radix=2;\n")
        f.write("memory_initialization_vector=\n")
        
        # Convert each row in int_img to a line in the COE file
        for row in int_img:
            # Convert each element in the row to binary and join them as a single line
            bin_row = ''.join(to_twos_complement(value, bit_width) for value in row)
            f.write(bin_row + ',\n')
        
        # Replace the last comma with a semicolon
        f.seek(f.tell() - 2, 0)
        f.write(';\n')

# Write each integer image to its respective .coe file
write_int_img_to_coe(int_img1, 'int_img1.coe')
write_int_img_to_coe(int_img2, 'int_img2.coe')
write_int_img_to_coe(int_img3, 'int_img3.coe')
