#!/usr/bin/env python3

"""
File containing testing for functionality.
"""

from qoperator import operator
from qstate import qstate
from f import *

# H1 = operator("H", N)
# H = H1**10
# print(H.shape)


# test large Hadamard matrix operating on state
# q = qstate("0", N)
# print(len(q))
# H10 = operator("H", N)
# print(H10.shape)
# psi = H10 * q
# print(len(psi))
# print(psi.state)
# print(qstate.normalized(psi.state))
# print(psi.joint_prob("1"))

# test out the control operators
# print(operator.Control(operator.NOT(), 4, [0, 3], [1, 2]))

# test for HW 8
# e1 = operator.Control(operator("NOT"), 3, 1, [0])
# e2 = operator.Control(operator("NOT"), 3, 2, [0])
# encoder = e1 * e2

# I2 = operator("NOT").tensor(operator("I"))
# error = operator("NOT").tensor(I2)

# beginning = operator.tensor( error*encoder, operator("I", 2) )

# d1 = operator.Control(operator("NOT"), 5, 3, [0])
# d2 = operator.Control(operator("NOT"), 5, 3, [1])
# d3 = operator.Control(operator("NOT"), 5, 4, [1])
# d4 = operator.Control(operator("NOT"), 5, 4, [2])
# decoder = d4 * d3 * d2 * d1

# c1 = operator.Control(operator("NOT"), 5, 1, [3, 4])
# c2 = operator.tensor( operator("I", 4), operator("NOT") )
# c3 = operator.Control(operator("NOT"), 5, 0, [3, 4])
# c4 = operator.tensor( operator("I", 3), operator("NOT"), operator("NOT") )
# c5 = operator.Control(operator("NOT"), 5, 2, [3, 4])
# correcter = c5 * c4 * c3 * c2 * c1

# circuit = correcter * decoder * beginning

# psi = qstate("[1,5]0000")
# phi = circuit * psi

# print(phi)

# test graph stuff
