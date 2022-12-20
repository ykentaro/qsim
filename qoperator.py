#!/usr/bin/env python3

"""
Defines the basic multi-bit quantum states.

The operator class is used to store all quantum gates
used in the circuits constructed in qsim.
"""

from math import log
from numpy import array, ndarray, matrix, kron, matmul, eye, allclose, zeros, column_stack, zeros, flip

from qstate import qstate


class operator:
    """
    Basic unitary linear quantum operator.
    
    Matrix size (2^n x 2^n) for n bit input / output.
    """
    def __init__(self, mat="I", n=1):
        if isinstance(mat, str):
            if mat == "NOT":
                self.matrix = self.NOT(n).matrix
            elif mat == "H":
                self.matrix = self.Hadamard(n).matrix
            elif mat == "I":
                self.matrix = self.Identity(n).matrix
            elif mat == "PAULIz":
                self.matrix = self.PAULIz().matrix
            elif mat == "SWAP":
                self.matrix = self.SWAP().matrix
            elif mat == "S":
                self.matrix = [[0,1],[1,0]]
        else:
            self.matrix = mat

    def __str__(self):
        string = ""
        for i in range(self.matrix.shape[0]):
            string += "| "
            for j in range(self.matrix.shape[1]):
                string += "{:6.3f} ".format(self.matrix[i, j])
            string += "|\n"
        return string[:-1]

    def latex(self):
        """
        Useful if needing to print the operator matrix in LaTeX.
        """
        string = "\\begin{bmatrix}\n"
        for i in range(self.matrix.shape[0]):
            string += "  "
            for j in range(self.matrix.shape[1]):
                string += f"{int(self.matrix[i, j])} & "
            string = string[:-2] + "\\\\\n"
        return string + "\\end{bmatrix}"

    def __mul__(self, other):
        """
        Defines multiplication with:
         - another operator matrix      -> new operator matrix
         - a qstate vector or ndarray   -> new qstate vector
         - a scalar                     -> new operator matrix
        """
        if isinstance(other, (int, float)):
            return operator(other*self.matrix)
        elif isinstance(other, qstate):
            newmat = matmul(array(self.matrix), other.state)
            return qstate(newmat, norm=False)
        elif isinstance(other, ndarray):
            newmat = matmul(array(self.matrix), other)
            return qstate(newmat, norm=False)
        newmat = matmul(self.matrix, other.matrix)
        return operator(newmat)

    def __pow__(self, n):
        return operator(self.matrix**n)

    def tensor(op1, op2, *args):
        """
        Kronecker product between two operators.
        """
        newmat = kron(op1.matrix, op2.matrix)
        for op in args:
            newmat = kron(newmat, op.matrix)
        return operator(newmat)

    def valid(self):
        shape = self.matrix.shape[0] == self.matrix.shape[1]
        unitary = allclose(eye(self.matrix.shape[0]), self.matrix.H * self.matrix)
        return shape and unitary

    @property
    def matrix(self):
        return self._matrix

    @property
    def shape(self):
        return self.matrix.shape

    @property
    def bits(self):
        return int(log(self.shape[0], 2))

    @matrix.setter
    def matrix(self, newmatrix):
        """
        Used to initialize the underlying matrix correctly.
        """
        if isinstance(newmatrix, (list, ndarray)):
            newmatrix = matrix(newmatrix)
        if isinstance(newmatrix, matrix):
            if newmatrix.shape[0] == newmatrix.shape[1]:
                self._matrix = newmatrix
                return
        self._matrix = eye(2)       # default to I2

    @staticmethod
    def Control(gate, bits, target, control):
        """
        Computes a matrix operator for a layer with controlled gates.

        layer has 'bits' inputs and outputs
        'gate' is on bit 'target' and is controlled by all 'control' bits

        gate - an operator object
        bits, target - integers specifying # of bits and position of operator
        control - list of positions of controlling bits
        ** bits begin at 0, ends at bits-1 **

        NOTE: if multiple input bits, top bit specified

        Returns a matrix representing the whole layer.
        """
        # first we need a classical function representing controlled NOT
        def cf(x, cx, state, OP):
            """
            x is a n bit binary input
            returns OP(tx) if cx all true
            """
            if sum(int(x[i]) for i in cx) == len(cx):
                return (OP * state).state
            return state

        # construct the operator to be used conditionally
        I1 = operator("I", target)                  # first bits from [0, target)
        I2 = operator("I", bits-target-gate.bits)   # last bits (target, end]
        op = operator.tensor(I1, gate, I2)

        # now construct the matrix using this function on the basis vectors
        cols = list()
        ps = qstate.pure_states(bits)
        n = 2**bits
        for i in range(n):
            x = zeros(n)
            x[i] = 1
            c = cf(ps[i], control, x, op)
            cols.append( c )
        return operator(column_stack(cols))

    @staticmethod
    def UnitaryF(n, f):
        """
        n - number of bits
        f - classical boolean function on n bits.

        From f, will create Uf with dimensions 2^n x 2^n.

        Returns a matrix operator Uf which implements f in a 
        reversible unitary quantum operator.
        """
        purestates = qstate.pure_states(n-1)
        uf = zeros((2**n, 2**n))
        for i in range(len(purestates)):
            # state = [int(x) for x in purestates[i]]
            if f(purestates[i]) == 0:
                # Fill with I
                uf[2*i][2*i] = 1
                uf[2*i+1][2*i+1] = 1
            else:
                # Fill with NOT
                uf[2*i+1][2*i] = 1
                uf[2*i][2*i+1] = 1
        return operator(uf)

    @staticmethod
    def Identity(n=1):
        """
        n bit Identity gate
        """
        return operator(eye(2**n))

    @staticmethod
    def NOT(n=1):
        """
        n bit NOT gate
        """
        return operator(flip(eye(2**n), axis=1))

    @staticmethod
    def Hadamard(n=1):
        """
        n bit input / output Hadamard gate
        """
        if Qadamards[n]:
            return Qadamards[n] * 2**(-n/2)
        if not Qadamards[1]:
            Qadamards[1] = operator([[1, 1], [1, -1]])
        for i in range(2, n+1):
            if Qadamards[i]: continue
            Qadamards[i] = operator.tensor(Qadamards[i-1], Qadamards[1])
        return Qadamards[n] * 2**(-n/2)

    @staticmethod
    def CNOT():
        """
        Single bit controlling the one below. Basic CNOT.
        """
        return operator.Control(operator.NOT(), 2, 1, [0])

    @staticmethod
    def Toffoli():
        """
        Two bits controlling a third below. Basic Toffoli gate.
        """
        return operator.Control(operator.NOT(), 3, 2, [0, 1])

    @staticmethod
    def PAULIz():
        return operator([[1, 0], [0, -1]])

    @staticmethod
    def SWAP():
        """
        swaps two qbits which are adjacent (only)
        """
        op = [[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]
        return operator(op)

Qadamards = [None for _ in range(11)]
