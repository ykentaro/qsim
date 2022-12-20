#!/usr/bin/env python3

"""
Used to parse quantum circuits.

The goal is to be able to input circuits layer by later, 
with each layer specifying the operators that will act 
on the given bits.

Basics:
  1. user specifies n input bits (n <= 10)
  2. user specifies l layers of quantum gates (l >= 0)
  3. at each layer user specifies what gates operate 
     on which qbits and which qbits control the operator
  4. f is also specified which is a function which should
     be used in Uf

This input will be specified in a .qc file and read by the
parser which will compute the probabilities when operating
on a given pure input state.
"""

import re
import sys


def parse_layer(match, debug=False):
    layer = list()
    if debug: 
        print("  layer:")

    for item in match:
        elements = item.split(';')

        # get the operator or function (only implement f for now)
        operator = elements[0].strip()
        if operator == "f":
            operator = "Uf"

        # now parse out the input qbits
        input_qbits = list(elements[1].strip().split())

        # finally get the control bits
        control_qbits = list(elements[2].strip().split()) if len(elements) == 3 else []

        layer.append([operator, input_qbits, control_qbits])
        
        if debug:
            print("    {}\n    {}\n    {}\n".format(operator, input_qbits, control_qbits))

    return layer


def parse(qc_file, debug=False):
    """
    Parses a .qc quantum circuit file.

    Obtains the following information:
      qbits - the number of qbits in the circuit (and maybe the names?)
      state - the initial state of the qbits of the circuit
      layers - the quantum gates forming each layer and what qbits they operate on
      function - the classical function and arguments to apply in Uf
      measurements - requests of measurement on the final state of the system
    
    Returns the qbits and layers of the circuit.
    """
    # program parameters
    num_qbits = 0
    state = None
    function = None
    layers = list()
    measurements = list()

    # read in the file for parsing
    with open(qc_file, 'r') as f:
        fstr = f.readlines()

    # parse the file line by line
    for line in fstr:
        # make sure that the line isn't a comment
        if re.match(r"^\s*#|^\s*$", line):
            continue
        elif debug:
            print(line)

        # first test for number of qbits specified
        # NOTE: change this to allow specification of bits order
        match = re.findall(r"^q?bits?[ ]*=?[ ]*(\d+)", line)
        if len(match):
            num_qbits = int(match[0])
            if debug: print(f"  {num_qbits} qbits\n")
            continue

        # next check for the input pure state of the system
        match = re.findall(r"^input?[ ]*=?[ ]*([\[\d\],\. ]+)", line)
        if len(match):
            state = match[0]
            if debug: print(f"  input state {state}\n")
            continue

        # now check for any classical function description
        match = re.findall(r"function *=?(.*)", line)
        if len(match):
            function = match[0]
            if debug: print(f"  function: {function}\n")
            continue

        # now parse out the heart of the program: the layers
        match = re.findall(r"{(.*?)}+", line)
        if len(match) > 0:
            layer = parse_layer(match, debug)
            layers.append(layer)
            continue

        # check for measurements of probabilities of the final state
        match = re.findall(r"prob *([n=]+\d+|[x01]*)", line)
        if len(match):
            query = match[0] if match[0] else "all"
            test = re.findall(r"[n=]+(\d+)", query)            # check for top n bits
            if len(test):
                query = int(test[0])
            measurements.append(("prob", query))
            if debug: print(f"  prob query: {query}\n")
            continue
        match = re.findall(r"measure *(\d+)", line)
        if len(match):
            measurements.append(("measure", int(match[0])))
            if debug: print(f" measure {match[0]} times\n")
            continue

        # check for a probability graph query
        match = re.findall(r"graph",line)
        if len(match):
            measurements.append(("graph"))
            if debug: print("  graph prob query")
            continue

        if debug:
            print("  no match for this line\n")

    if num_qbits == 0:
        print("ERROR: Number of qbits unspecified - Aborting.")
        return
    if not state:
        state = "0"*num_qbits       # default to all zero inputs
    if not function:
        function = "f()"            # default to no args f(x)
        
    # get the list of qbits {q0, q1, q2, ..., qn-1}
    qbits = {f"q{x}":x for x in range(num_qbits)}

    if debug:
        print(qbits, '\n')
        for layer in layers:
            print(layer)
        print()
        for query in measurements:
            print(query)
        print()

    return qbits, state, function, layers, measurements


if __name__ == "__main__":
    print(len(sys.argv), sys.argv)

    if len(sys.argv) < 2:
        print("Please specify an input file.")
        exit(1)
    
    filename = sys.argv[1]

    debug = False
    if len(sys.argv) == 3:
        if re.match(r"debug", sys.argv[2].lower()):
            debug = True

    circuit_info = parse(filename, debug)
    qbits = circuit_info[0]
    state = circuit_info[1]
    function = circuit_info[2]
    layers = circuit_info[3]
    measurements = circuit_info[4]

    print(f"qbits: {len(qbits)}\n  {qbits}\n")
    print(f"input state: {state}\n")
    print("layers:")
    for layer in layers:
        print(f"  {layer}")
    print()
    print(f"function: {function}\n")
    print(f"measuements:")
    for m in measurements:
        print(f"  {m}")
    print()
