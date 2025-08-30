import numpy as np
from qiskit import QuantumCircuit,execute
from qiskit.providers.aer import AerSimulator
from fractions import Fraction


def qft_dagger(n):
    """n-qubit QFTdagger the first n qubits in circ"""
    qc = QuantumCircuit(n)
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc


def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2,4,7,8,11,13]:
        raise ValueError("'a' must be 2,4,7,8,11 or 13")
    U = QuantumCircuit(4)        
    for iteration in range(power):
        if a in [2,13]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a in [7,8]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [4, 11]:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = "%i^%i mod 15" % (a, power)
    c_U = U.control()
    return c_U

num = int(input())
for i in range(num):
    string = input().split()
    n1_count = int(string[0])
    a = int(string[1])

    qc = QuantumCircuit(n1_count +4, n1_count)
    for q in range(n1_count):
        qc.h(q)
        
    qc.x(n1_count)
    for q1 in range(n1_count):
        qc.append(c_amod15(a, 2**q1), 
                [q1] + [i+n1_count for i in range(4)])
    qc.barrier()
    # Do inverse-QFT
    qc.append(qft_dagger(n1_count), range(n1_count))
    qc.barrier()
    # Measure circuit
    qc.measure(range(n1_count),range(n1_count))


    sim = AerSimulator()
    job = execute(qc, backend=sim , shots=1000)
    result=job.result()
    counts=result.get_counts(qc)
    count = (sorted(counts.items()))
    frac = []
    for i in count:
        frac = Fraction(int(i[0], 2)/2**n1_count).limit_denominator(15)
        print(i[0], frac.denominator)