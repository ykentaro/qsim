# qsim

Programming language for quantum computing simulation. Quantum circuits simulated using matrix operations. Circuits constructed in layers which act in parallel on a set of qbit states. Each layer acts sequentially on the states and produces a final output state. This final state can be measured to observe the outcome of the computation.

### Authors

Clay Bell

Kentaro Yasuda

### Project Information

Course: Computing and Quantum Computing

Professor: Malik Magdon-Ismail

## Circuit Construction

Circuits are constructed in a text (or .qc) file. This file contains lines which describe the circuit to the simulator. 

Each line specifies a layer of the circuit or gives some information such as the inputs bits, measurements, etc.

Example working circuit .qc files are found in the `test_files` directory and can be ran to see how the simulator works.

### Input

The number of input qbits must be specified for the circuit. This is done with the `qbits = ` keyword.

The following specifies a circuit with 5 input qbits. This means the layer operators will contain (32 x 32) elements.

`qbits = 5`

The qbits initial state can also be specified with the `input = ` keyword. For each qbit the state is specified either `0`, `1`, or `[a,b]` where `a` and `b` are the amplitudes of the `0` and `1` states of the qbit respectively.

`input = [1,1]1100`

This specifies a 5 qbit input state with the first bit having an equal superposition of `0` and `1`, the second two bits being in the pure state `1`, and the final two qbits being in the pure state `0`.

### Operators

The following operators are valid for specification and use in the circuit files:

 - `I`   - Identity: does not change the qbit state
 - `NOT` - Not Gate: flips the amplitudes of the qbit
 - `H`   - Hadamard Gate: puts a qbit into a superposition of `0` and `1` states
 - `Uf` - Unitary f(x): quantum implementation of a classical boolean function f(x)

### Controlled Gates

Each of the operators can be controlled by a set of qbits which are distinct from the inputs to the operator. This has the effect of applying the operator to the input only when the control qbits are in the `1` (true) state.

As of now `Uf` cannot be controlled.

### Unitary f(x) Operator

The unitary function operator `Uf` takes a classical boolean function `f(x)` which operates on a n-bit pure classical input x and produces a value `0` (false) or `1` (true).

This classical `f(x)` is used to construct a unitary quantum `Uf` operator which acts on the incoming qbits and produces a state consistent with the classical function.

When operating on pure states states the `Uf` outputs a state with each pure state in the input having its amplitude flipped if `f(x)` on this pure state is true.

The classical `f(x)` is specified in the file `f.py` and can be named whatever is desired. This function is then initialized as described in the circuit file using the `function =` keyword.

`function = func([inputs])`

This will be executed to initialize the classical `f` which will be used whenever `Uf` is needed. 

Note that for circuits without a `Uf` this can be ignored entirely.

### Layer

Each layer is specified by a group of quantum unitary operators which operate on a set of input qbits and are controlled by a set of qbits from the circuit.

Each layer can have multiple operators as long as they do not have the same input or control bits (they must operate on distinct qbits).

Any qbit which does not have an operator in a layer is hit with the identity and does not change state.

Operators are specified using curly braces with semicolons separating the operator, inputs, and control bits (in that order). Multiple bits are separated by spaces.

`{OPERATOR; input bits; control bits}`

Note that control bits can be omitted if not used, while the operator and input bits are neccessary to specify.

The following specifies a single operator layer which hits all of the input bits with the Hadamard gate:

`{H; q0 q1 q2 q3 q4}`

The following is a single operator layer which hits the first qbit with a NOT controlled by the second and third qbits (Toffoli gate).

`{NOT; q0; q1 q2}`

This layer contains two operators which act on distinct qbits in the layer. Hadamard is applied to the first bit while NOT is applied to the third.

`{H; q0} {NOT; q2}`

The following is a more compliated example, with Uf being applied to the first 3 bits and CNOT applied to the last controlled by the fourth.

`{f; q0 q1 q2} {NOT; q4; q3}`

Layers can contain as many operators as needed with whatever operators neccessary, however some layers may get split up during circuit construction for ease of computation or if they have overlapping control bits.

### Measurement

Measurement occurs at the end of computation. Specified measurements will be executed on the final statevector and the results will be printed to stdout. 

As many measurements as wanted can be specified. Possible measurement types currently include:

 - `prob` - gives the probability for measurement of each pure state
 - `prob 000xx` - gives the probability of measurement of the specific state which matches the pattern provided
 - `measure n` - collapses and measures the final state `n` times and returns the results
 - `graph` - prints a graph of the final probabilities of the state

Patterns for probability measurement can be specified to match particular groups of states.

 - `0` matches any state with a 0 for that qbit
 - `1` matches any state with a 1 for that qbit
 - `x` matches either a 0 or a 1 for that qbit

The pattern `00x11` matches any state with the first two qbits as `0` and the last two qbits as `1`. The middle qbit is free to be either.

### Comments

Comments can be added by prefacing the text with `#`. These will be ignored when constructing the circuit.

`# this is a comment`

## Running the Simulation

The simulation can be run by feeding a .qc file with a valid circuit into the `qsim.py` program. This will print to stdout the results of the computation specified by the measurement section of the circuit file.

`qsim.py circuit.qc`

Additional options include `debug` which prints debugging information to stdout as well as any results of the computation.

`qsim.py circuit.qc debug`

The output can be redirected to a file to save results for later analysis.

`qsim.py circuit.qc > results.txt`

## Simulation Specifics

This is not neccessary for using the simulator and is more of a documentation of the software.

### qsim.py

### qstate.py

### qoperator.py

### qparser.py

### f.py

This file specifies the classical f(x) boolean function in pure python. It is edited by the user to create their own `Uf`.

The function takes the form of a class with a `__init__` method and a `__call__` method. The init is used to specify any input needed for the function (done in the .qc file) and the call method is used when the function itself is called on a pure state input when constructing `Uf`.

The following is an example f(x) which dots the input vector with a given vector `a` specified at run time. The output is 0 if the product is even and 1 if it is odd.

```
class example_f:
  def __init__(self, a):
    self.a = a

  def __call__(self, x):
    pow = sum(a[i]*x[i] for i in range(len(x)))
    return 0 if pow % 2 == 0 else 1
```

### tests.py

## TODO:
 - clean up and make sure code looks good
 - document code
 - test everything thouroughly

 - make your own operator
 - allow arbitrary qbit names
 - verify that the circuits are valid
 - use only input= if wanted instead of qbits=

 POST GROVER:
 - specify your own operator (special operators)
 - name a group of layer for use later
 - repeat set of layers
