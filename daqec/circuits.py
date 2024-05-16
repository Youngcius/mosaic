import cirq
import rustworkx as rx
from functools import reduce
from operator import add
from .graphs import node_index


def repr_circuit(circ: cirq.Circuit) -> str:
    return 'Circuit(#Q={}, #G={})'.format(len(circ.all_qubits()), len(list(circ.all_operations())))


def max_gate_weight(circ: cirq.Circuit) -> int:
    """Obtain the maximum gate weight of a circuit"""
    return max([len(g.qubits) for g in circ.all_operations()])


def circuit_to_dag(circ: cirq.Circuit) -> rx.PyDiGraph:
    """
    Convert a circuit into a Directed Acyclic Graph (DAG) according to dependency of each gate's qubits.
    """
    all_gates = list(circ.all_operations())
    dag = rx.PyDiGraph(multigraph=False)
    dag.add_nodes_from(all_gates)
    while all_gates:
        g = all_gates.pop(0)
        qubits = set(g.qubits)
        for g_opt in all_gates:  # traverse the subsequent optional gates
            qregs_opt = set(g_opt.qubits)
            if dependent_qubits := qregs_opt & qubits:
                dag.add_edge(node_index(dag, g), node_index(dag, g_opt), {'qubits': list(dependent_qubits)})
                qubits -= qregs_opt
            if not qubits:
                break
    return dag


# def circuit_to_dag_old(circ: cirq.Circuit) -> nx.DiGraph:
#     """Convert a circuit to a DAG"""
#     all_gates = list(circ.all_operations())
#     dag = nx.DiGraph()
#     dag.add_nodes_from(all_gates)
#     while all_gates:
#         g = all_gates.pop(0)
#         qubits = set(g.qubits)
#         for g_opt in all_gates:  # traverse the subsequent optional gates
#             qubits_opt = set(g_opt.qubits)
#             if qubits_opt & qubits:
#                 dag.add_edge(g, g_opt)
#                 qubits -= qubits_opt
#             if not qubits:
#                 break
#     return dag
#

def dag_to_circuit(dag: rx.PyDiGraph) -> cirq.Circuit:
    """Convert a DAG to a Circuit"""
    node_is_block = isinstance(next(iter(dag.nodes())), cirq.Circuit)
    if node_is_block:
        return cirq.Circuit(reduce(add, [list(dag[idx].all_operations()) for idx in rx.topological_sort(dag)]))
    return cirq.Circuit([dag[idx] for idx in rx.topological_sort(dag)])
