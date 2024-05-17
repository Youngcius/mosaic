
import daqec
import cirq
import numpy as np

from cirq.contrib.qasm_import import circuit_from_qasm


qasm_file = './benchmarks/random/rand_8.qasm'

with open(qasm_file, 'r') as f:
    circ = circuit_from_qasm(f.read())

circ = circ[:10]

print(circ)


blocks = daqec.partition.seq_partition(circ, 3)

for blk in blocks:
    print()
    print('---')
    print(blk)
    print()
