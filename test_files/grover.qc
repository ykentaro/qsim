# grover's search algorith
# 3 bit example, f(100) = f(x*) = 1

qbits = 4
input = 0001        # typical Grover input

function grover(["100","101"])

# step 1: Hadamard everything
{H; q0 q1 q2} {H; q3}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2}
{NOT; q0 q1 q2}
{PAULIz; q2; q0 q1}
{NOT; q0 q1 q2}
{H; q0 q1 q2}

# measure results
prob n=3