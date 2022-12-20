# circuit from homework 7

# 4 input bits of zero, one bit input 1, 5 total qbits
qbits = 5

# layer 1: Hadamard everything
{H; q0 q1 q2 q3 q4}

# layer 2: Uf
{Uf; q0 q1 q2 q3 q4}

# layer 3: Hadamard top 4 bits
{H; q0 q1 q2 q3}

# once cirucit is complete we specify the 'run' segment
input = 00001

# specify parameters of boolean function for setup
function vecf([1, 1, 1, 1], 3)

# specify measurement probabilities of particlar qbit states
# pick bit to be 0, 1, or x (either)
prob 0000x

# alternatively specify measurement of all probabilities
prob n=4

# measure the output a given # of times (100 here)
#measure 100