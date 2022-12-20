#!/usr/bin/env python3

"""
Defines the basic multi-bit quantum states.
"""

from math import sqrt, log
from numpy import array, ndarray, isclose, kron
from numpy.linalg import norm
from random import random
import re


class qstate:
    """
    Defines a basic quantum state composed of multiple q-bits.

    Repeats state "state" "n" times.

    ex)
      state="0"         -->  |0〉
      state="0", n=2    -->  |00〉
      state="010"       -->  |010〉
      state="010", n=2  -->  |010010〉
    """
    def __init__(self, state="0", n=1, norm=True):
        self.norm = norm        # optimization reasons, to normalize or not
        if isinstance(state, str) and n > 0:
            self.state = state * n
        else:
            self.state = state

    def __str__(self):
        pure_states = qstate.pure_states(self.bits)
        string = ""
        for i in range(len(pure_states)):
            if self.state[i]:
                string += "({:.3f})|{}〉+ ".format(self.state[i], pure_states[i])
        return string[:-2]

    def __add__(self, other):
        newvector = list()
        for i in range(len(self.state)):
            newvector.append(self.state[i] + other.state[i])
        return qstate(newvector)

    def __len__(self):
        return len(self.state)

    @staticmethod
    def normalized(vector, ret_val=False):
        """ verifies that the vector is normalized (can return norm if ret_val=True) """
        val = sqrt(sum(norm(x)**2 for x in vector))
        return isclose(val, 1.0) if not ret_val else isclose(val, 1.0), val

    @staticmethod
    def normalize(vector):
        """ will normalize a vector """
        norm, val = qstate.normalized(vector, True)
        if not norm:
            return [(1/val)*x for x in vector]
        return vector

    @staticmethod
    def pure_states(n):
        """ computes the pure states for n bits """
        if n <= 1:
            return ["0", "1"]
        else:
            zero = ["0"+x for x in qstate.pure_states(n-1)]
            one = ["1"+x for x in qstate.pure_states(n-1)]
            return zero + one

    @property
    def state(self):
        return self._statevector
  
    @property
    def prob(self):
        """ probabilities of pure states """
        return [norm(x)**2 for x in self.state]

    @property
    def bits(self):
        return int(log(len(self), 2))

    @property
    def shape(self):
        return self.state.shape

    @state.setter
    def state(self, newstate):
        """ sets the statevector of the qstate """
        # verify that the vector is of from 2^n and normalized
        if isinstance(newstate, list) or isinstance(newstate, ndarray):
            if log(len(newstate), 2).is_integer():
                if self.norm:
                    self._statevector = array(qstate.normalize(newstate))
                else:
                    self._statevector = array(newstate)

        # construct a vector from string of pure states tensored together
        elif isinstance(newstate, str):
            matches = re.findall(r"(\[[\d\., ]+\]|[01])", newstate)
            qbits = list()
            for m in matches:
                if m == "0":
                    qbits.append(qstate.ZERO())
                elif m == "1":
                    qbits.append(qstate.ONE())
                else:
                    alpha, beta = m[1:-1].split(',')
                    qbits.append( qstate([float(alpha.strip()), float(beta.strip())]) )
            if len(qbits) < 2:
                final = qbits[0]
            else:
                final = qstate.tensor(qbits[0], qbits[1], *qbits[2:])
            self._statevector = final.state

        else:
            self._statevector = array([1, 0])     # default to |0〉

    def tensor(qs1, qs2, *args):
        """
        Computes tensor product between two states.
        
        tensor(|0〉, |1〉) = |01〉
        """
        vec = kron(qs1.state, qs2.state)
        for qsn in args:
            vec = kron(vec, qsn.state)
        return qstate(vec, norm=False)

    def measure(self):
        """
        Collapses state down into pure basis.
        Returns classical measurement of final state.
        """
        # find list of probability partial sums
        prob = self.prob
        probs = [sum(prob[:i]) for i in range(1, len(prob)+1)]

        # get the uniform random variable
        x = random()

        # now find out which pure state this measurement corresponds to
        state = 0
        while probs[state] < x:
            state += 1
        statestr = self.pure_states(self.bits)[state]
        self.state = statestr               # collapse down to pure state

        return cstate(statestr)

    def joint_prob(self, pattern):
        """
        Finds the probability of a measurement resulting in a state
        which matches the pattern given.

        pattern: xx101  ->  matches any first 2 bits and 101 as last 3

        Returns the probability of a final pure state measurement which
        adheres to the pattern given.

        ex) first 4 bits (of 5) have q2=1 and q4=1 rest any
          pattern: x1x1x
        """
        probs = self.prob
        pure_states = self.pure_states(self.bits)
        total_prob = 0
        for i in range(len(probs)):
            state = pure_states[i]
            match = True
            for j in range(len(pattern)):
                if pattern[j] != 'x' and pattern[j] != state[j]:
                    match = False
                    break
            if match:
                total_prob += probs[i]
        return total_prob
            
    @staticmethod
    def ZERO():
        """
        Just the single qbit pure state |0〉
        """
        return ZERO

    @staticmethod
    def ONE():
        """
        Just the single qbit pure state |1〉
        """
        return ONE


ZERO = qstate([1, 0])
ONE = qstate([0, 1])


class cstate:
    """
    Classical pure state of bits.

    Results from collapsed qstate.
    """
    def __init__(self, state):
        self.state = state

    def __getitem__(self, index):
        return cstate(self.state[index])

    def __str__(self):
        return f"|{self.state}〉"


def measure(phi, m, r=3):
    """
    Auxillary function used to measure qstates with easy to
    write parameters.

    phi is the state to measure.

    m = ("prob", n)
      Measures probabilities for top n-bit pure states.

    m = ("prob", "all")
      Measures probabilities for pure states.

    m = ("prob", pattern)
      Measures probability for state which matches pattern.
      ex. pattern = "000xx" - top 3 bits 0, others are any
      More examples in README.

    m = ("measure", n)
      Prints results of n measurements of final state.

    m = ("graph")
      Shows a graph of the probabilities of the state.

    r is the number of digits to round.
    """
    if m[0] == "measure":
        print(f"Results of {m[1]} Measurements")
        res = {s:0 for s in qstate.pure_states(phi.bits)}
        for _ in range(m[1]):
            PHIprime = qstate(phi.state)    # sorry no cloning thm :(
            q = PHIprime.measure()
            res[q.state] += 1
        for qs in res.keys():
            if res[qs] > 0:
                print(f"  |{qs}〉--> {res[qs]}/{m[1]}")
    elif m[0] == "prob":
        if isinstance(m[1], int) or m[1] == "all":
            print("Probabilities of Pure State Measurements:")
            bits = phi.bits
            s = phi.pure_states(bits)
            p = phi.prob
            if isinstance(m[1], int):
                top = m[1]
                step = 2**(bits-top)
            else:
                top = bits
                step = 1
            for i in range(0, len(s), step):
                prob_list = p[i:i+step]
                print(f"  ({round(sum(prob_list), r)}) |{s[i][:top]}〉")
        else:
            #print(f"Probability of {m[1]} Measurement:")
            p = phi.joint_prob(m[1])
            s = ""
            s += m[1][1]
            s += m[1][3]
            s += m[1][5]
            s += m[1][7]
            s += m[1][9]

            print(f"  P[{s}] = {round(p, r)}")
    elif m[0] == "graph":
        import matplotlib.pyplot as plt
        print("Plotting probabilities of states")
        s = phi.pure_states(phi.bits)
        p = phi.prob
        plt.bar(s,p)
        plt.title("State probabilities")
        plt.xlabel("States")
        plt.ylabel("Probabilities")
        plt.ylim([0,1])
        plt.show()
            