# error correcting circuit for HW 8

qbits = 5
input = [1,1]0000

# begin with the encoder
{NOT; q1; q0}
{NOT; q2; q0}

# now for the error introduced into the system
{NOT; q0}

# now for the error detector
{NOT; q3; q0}
{NOT; q3; q1}
{NOT; q4; q1}
{NOT; q4; q2}

# now for the error corrector
{NOT; q1; q3 q4}
{NOT; q4}
{NOT; q0; q3 q4}
{NOT; q3 q4}
{NOT; q2; q3 q4}

# measure the states
prob n=3
prob 111xx
#measure 100