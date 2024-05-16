import sys
sys.path.append('..')

import cirq
import networkx as nx

circ = cirq.Circuit()

qubits = cirq.LineQubit.range(3)
circ.append(cirq.X.on(qubits[0]))
circ.append(cirq.X.on(qubits[2]))
circ.append(cirq.CNOT(*qubits[:2]))
circ.append(cirq.CNOT(*qubits[1:]))

print(circ)
print(isinstance(list(circ.all_operations())[0], cirq.GateOperation))

from daqec.circuits import circuit_to_dag
from daqec.partition import contract_1q_gates_on_dag, contract_1q_gates_on_dag_old

dag = circuit_to_dag(circ)

# for src, dst in dag.edges():
#     print(src, '-->', dst)

print(dag.edge_list())

print(circ.__hash__())

blocks = contract_1q_gates_on_dag_old(dag)

for blk in blocks:
    print(blk)

# print(cirq.Circuit(nx.topological_sort(dag)))
