#!/usr/bin/env python3

"""
Defines the basic qbit and cbit states.

Deprecated file, utility now mostly lives in qstate.py.

This is a proof of concept, not used in final qsim.
"""

from math import sqrt
from numpy.linalg import norm
from random import random

from qstate import qstate

class qbit(qstate):
    """
    Basic q-bit class implementing a single quantum bit.
    Must be normalized.
    Contains a superposition of the |0〉 and |1〉 states.
    """
    def __init__(self, state=0):
        super().__init__(state, n=1)

    def probstr(self):
        return "({:.3f})|0〉+ ({:.3f})|1〉".format(*self.prob)

    @qstate.state.setter
    def state(self, newstate):
        if isinstance(newstate, list) and len(newstate) == 2:
            self._statevector = qstate.normalize(newstate)
        else:
            self._statevector = [1, 0]      # default to |0〉

    def measure(self):
        """
        Collapses state down into |0〉 or |1〉 basis.
        Returns classical measurement of final state.
        """
        p0 = norm(self.state[0])**2
        if random() <= p0:
            self.state = [1, 0]
            return cbit(0)
        else:
            self.state = [0, 1]
            return cbit(1)


class cbit:
    """
    Basic implementation of a single classical bit.
    In state |0〉 or |1〉.
    """
    def __init__(self, state=0):
        self.state = state

    @property
    def state(self):
        return self._statevector[1]

    @state.setter
    def state(self, newstate):
        if newstate == 1:
            self._statevector = [0, 1]
        else:
            self._statevector = [1, 0]

    def __str__(self):
        return "|{}〉".format(self.state)


if __name__ == "__main__":
    # test that a valid q-bit can be stored and printed
    q1 = qbit([1/sqrt(2), 1j/sqrt(2)])
    print(q1, "->", q1.probstr())

    # test that an unnormalized q-bit reverts is normalized
    q2 = qbit([0.5, 0.5])
    print(q2, "->", q2.probstr())

    # test a full complex q-bit and normalization
    q3 = qbit([0, 5+4j])
    print(q3, "->", q3.probstr())

    # test that a cbit can be created
    c1 = cbit(1)
    c2 = cbit()
    print(c1, c2)

    # now test that a qbit can be measured to a cbit
    print("Before:", q1)
    c3 = q1.measure()
    print("Measured Value:", c3)
    print("After:", q1)

    # now make sure that the probability distributions are valid
    count = 0
    for _ in range(10000):
        q = qbit([1/sqrt(2), 1j/sqrt(2)])
        c = q.measure()
        if c.state == 0:
            count += 1
    print(count / 10000)