# large scale Grover's search algorith
# 9 bit example, f(001000101) = f(x*) = 1
# 2m54.563s runtime before optimization

qbits = 10
input = 0000000001        # typical Grover input

function grover(["001000101"])

# step 1: Hadamard everything
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8} {H; q9}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# step 2: hit with Uf (part 1 of Grover Iteration)
{Uf; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

# step 3: hit top 3 bits with W (part 2 of Grover Iteration)
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{PAULIz; q8; q0 q1 q2 q3 q4 q5 q6 q7}
{NOT; q0 q1 q2 q3 q4 q5 q6 q7 q8}
{H; q0 q1 q2 q3 q4 q5 q6 q7 q8}

# measure results
prob 001000101