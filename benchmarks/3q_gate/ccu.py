from qiskit import QuantumCircuit

qc = QuantumCircuit.from_qasm_file('ccu.qasm')
qc.draw('mpl', filename='ccu.png')