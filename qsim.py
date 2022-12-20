#!/usr/bin/env python3

"""
Quantum Circuit Simulator

Clay Bell, Kentaro Yasuda
12/8/2022
"""

import sys
import re
import cProfile, pstats

from qparser import parse
from qoperator import operator
from qstate import qstate, measure
from f import *


DEBUG = False
PROFILE = False


def construct_layer(layer, qbits, cf):
    """
    Create the matrix representation of the given layer.

    layer:
      [[operator1, [input qbits], [control bits]], [operator2, [...], [...]]]

    qbits:
      {'bit0':0, 'bit1':1, ..., 'bitn':n}
      # of qbits = len(qbits)
    
    cf:
      control function (classical binary function)
      used to construct Uf

    ASSUMPTIONS:
        1. layer with multiple gates contain no control bits
        2. Uf unitaries operate on adjacent qbit blocks
    """
    # list of operators on this layer (default to nothing)
    operators = ["I" for _ in range(len(qbits))]

    # first parse out any special cases: control or Uf
    if len(layer) == 1:
        element = layer[0]
        # unitary function: can now be controlled or part of layer
        # assumption: Uf is continuous block
        if element[0].upper() == "UF":
            bits = sorted([qbits[x] for x in element[1]])
            control = [qbits[x] for x in element[2]]
            Uf = operator.UnitaryF(len(bits), cf)
            # if controlled, ends up being whole layer
            if len(control):
                Uf = operator.Control(Uf, len(qbits), bits[0], control)
                return Uf
            # otherwise need to tensor w Is where Uf is not
            else:
                I1 = operator("I", bits[0])
                I2 = operator("I", len(qbits)-bits[-1]-1)
                return operator.tensor(I1, Uf, I2)

        # controlled gate: must be whole layer
        # one input for control gates only
        if len(element[2]) > 0:
            OP = operator(element[0])
            qinput = qbits[element[1][0]]               # 1 bit input
            control = [qbits[x] for x in element[2]]
            return operator.Control(OP, len(qbits), qinput, control)

    # run through each element and add to the operators
    for element in layer:
        qinput = element[1]
        for line in qinput:
            operators[qbits[line]] = element[0]

    # condense the operator list down to neccessary ones
    i = 0
    neccessary = list()
    while i < len(operators):
        name = operators[i]
        if name in ("I", "NOT", "H", "SWAP"):
            j = 1
            while i+j < len(operators) and operators[i+j] == name:
                j += 1
            neccessary.append((name, j))
            i += j
        else:
            neccessary.append((name, 1))
            i += 1
    
    # now construct the tensor product of the operators
    LAYER = operator("I", 0)
    for line in range(len(neccessary)):
        op = neccessary[line][0]
        n = neccessary[line][1]
        LAYER = LAYER.tensor( operator(op, n) )
    return LAYER


def construct_operator(circuit, qbits, cf):
    """
    Creates the quantum operator corresponding to a given quantum
    circuit specified with a set number of bits and (optionally)
    a classical boolean function f(x) implemented as operator Uf.

    NOTE: any layer w/ multiple controlled gates is constructed separately

    circuit:
        list of layers: [[operator, [bits], [control bits]], ... ]
    qbits:
        number of bits in the circuit input and output
    """
    if DEBUG:
        print("Circuit to Construct:")
        for l in circuit:
            print(f"  {l}")
        print(f"Qbits: {len(qbits)} {qbits}\n")

    # split any layers with multiple control or Uf circuits up
    i = 0
    while i < len(circuit):
        if not isinstance(circuit[i][0], str):     # multiple gates on layer
            # check if any are controlled or Uf
            UorCont = False
            for sublayer in circuit[i]:
                if sublayer[0].upper() == "UF" or len(sublayer[2]) > 0:
                    UorCont = True
                    break
            # if so split the layer up into its components
            if UorCont:
                layer = circuit.pop(i)
                for sublayer in reversed(layer):
                    circuit.insert(i, [sublayer])
        i += 1
    if DEBUG:
        print("Post Split Circuit:")
        for l in circuit:
            print(f"  {l}")

    # construct the layers one by one
    CIRCUIT = [construct_layer(l, qbits, cf) for l in circuit]
    
    if DEBUG:
        print(f"Final Circuit:")
        for c in CIRCUIT:
            print(c)

    return CIRCUIT


def main(filename):
    # 2. parse the .qc file and get the qbits and layers of the circuit
    # NOTE: need way to input arbitrary [alpha, beta] qbit state
    circuit_info = parse(filename)
    qbits = circuit_info[0]
    state = circuit_info[1]
    function = circuit_info[2]
    layers = circuit_info[3]
    measurements = circuit_info[4]
    if DEBUG:
        print(f"qbits:\n  {qbits}\n")
        print(f"input state: {state}\n")
        print("layers:")
        for layer in layers:
            print(f"  {layer}")
        print(f"function: {function}\n")
        print(f"measuements:")
        for m in measurements:
            print(f"  {m}")
        print()

    # 3. construct the circuits for each f(x)

    # initialize the function
    cf = eval(function)

    # construct the operator that represents the circuit
    OPs = construct_operator(layers, qbits, cf)

    # get the input quantum pure state
    PSI = qstate(state)

    # 4. apply the circuit to the input state to get the final state
    PHI = PSI
    for OP in OPs:
        PHI = OP * PHI

    # 5. take any measurements requested from the final state
    if len(measurements): print(f"Input State: {PSI}\n")
    for m in measurements:
        measure(PHI, m, 10)

if __name__ == "__main__":
    # 1. parse the program args and setup env variables
    if DEBUG:
        print(len(sys.argv), sys.argv)
    if len(sys.argv) < 2:
        print("Please specify an input quantum circuit file.")
        exit(1)
    filename = sys.argv[1]
    for i in range(2, len(sys.argv)):
        if re.match(r"debug", sys.argv[i].lower()):
            DEBUG = True
        if re.match(r"stats|profile", sys.argv[i].lower()):
            PROFILE = True
    
    # can run the simulation in profile mode or normally
    if PROFILE:
        with cProfile.Profile() as pf:
            main(filename)
        print()
        print("-"*20 + " Stats " + "-"*20)
        stats = pstats.Stats(pf).sort_stats('cumtime')
        stats.print_stats()
    else:
        main(filename)