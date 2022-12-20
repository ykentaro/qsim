# stress test to see how efficient the program is

qbits = 10

{H; q0}

{NOT; q1; q0}

{H; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

{H; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

{H; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

{H; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

{H; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

{H; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

{H; q0 q1 q2 q3 q4 q5 q6 q7 q8 q9}

prob n=3

measure 10