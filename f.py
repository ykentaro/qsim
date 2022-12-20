#!/usr/bin/env python3

"""
This file contains the classical boolean f(x) which is used in
the quantum circuit simulation to generate Uf.

Function which are to be used for circuits can be specified here
and then noted in the .qc file. 

See the README for more information. A function template is provided
here for use.
"""

class f:
  def __init__(self, *args):
    pass

  def __call__(self, x):
    return bool(x)

class test:
  """ for uf.qc testing """
  def __init__(self):
    pass

  def __call__(self, x):
    return 0 if x == "1" else 1


class grover:
  """ for grover's search algorithm """
  def __init__(self, xstar):
    self.xstar = xstar

  def __call__(self, x):
    return 1 if x in self.xstar else 0


class vecf:
  """
  Function: f(x)
    boolean function

  Initialize the function with:
    a - vector of coefficients
    k - modulus of dot product of inputs and a
  """
  def __init__(self, a=[1, 2, 3, 4], k=2):
    self.a = a
    self.k = k

  def __call__(self, x):
    """
    Takes as input a vector with n binary entries.
    Outputs a binary value 0 or 1.
    """
    X = [int(i) for i in list(x)]
    ex1 = (X[0] + X[1] + X[2])
    return ((X[0]+X[1])**ex1 + (X[1]+X[2])**ex1)%2
    # exponent = sum(self.a[i]*X[i] for i in range(len(x))) % self.k
    # return int((1/2)*(1 + (-1)**exponent))