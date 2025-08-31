# Shor's Algorithm
This script is a simplified implementation of Shor's algorithm, designed to find the period of a modular exponentiation function, specifically $a^x\ (mod\ 15)$. The project demonstrates a fundamental application of quantum computing to a problem in number theory.

## Key Components
### 1. The Inverse Quantum Fourier Transform (IQFT)
The `qft_dagger(n)` function creates a quantum circuit for the inverse Quantum Fourier Transform. This operation is a critical step in Shor's algorithm as it converts the quantum phase, which encodes the period, into a measurable binary state.

### 2. The Controlled Modular Exponentiation Gate
The `c_amod15(a, power)` function builds a controlled modular exponentiation gate. This gate applies a unitary operation that computes $∣ψ⟩=∣ay(mod15)⟩$, but only when a control qubit is in the $∣1⟩$ state. The function is specifically designed to work with integers `a` that are coprime to 15 (i.e., 2, 4, 7, 8, 11, and 13).

### 3. The Main Execution Loop
This section of the code orchestrates the entire algorithm. It takes user input for the number of counting qubits and the base `a`. The circuit is built by:
- Initializing the counting qubits in a superposition with Hadamard gates.
- Applying a series of `c_amod15` gates to encode the period into the phase of the counting qubits.
- Executing the `qft_dagger` to convert the phase to a measurable binary string.
- Measuring the counting qubits and using the `Fraction` module to find the best rational approximation. The denominator of this fraction gives the likely period of the function.
