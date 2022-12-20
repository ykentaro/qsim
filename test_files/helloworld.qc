# this is a comment

# first we specify the number of bits
qbits = 4

# next we specify the layers one by one
# this means that H operates on a, b, and c with d controlling
{H; q0 q1 q2; q3}

# this layer has multiple gates
# note it is assumed that any qbit without a gate on a layer is acted on by I
{NOT; q2 q3; q0}   # CNOT with a controlling NOT(c, d)

# we need at least one application of the function f
{f; q0 q1 q2 q3;}       # can keep trailing ; or leave out

# we can also have a layer with multiple gates
{I; q0 q1} {H; q2 q3}
