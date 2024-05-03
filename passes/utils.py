import numpy as np
import networkx as nx
import cirq


def max_gate_weight(circ: cirq.Circuit) -> int:
    """Obtain the maximum gate weight of a circuit"""
    return max([len(g.qubits) for g in circ.all_operations()])


def circuit_to_dag(circ: cirq.Circuit) -> nx.DiGraph:
    """Convert a circuit to a DAG"""
    all_gates = list(circ.all_operations())
    dag = nx.DiGraph()
    dag.add_nodes_from(all_gates)
    while all_gates:
        g = all_gates.pop(0)
        qubits = set(g.qubits)
        for g_opt in all_gates:  # traverse the subsequent optional gates
            qubits_opt = set(g_opt.qubits)
            if qubits_opt & qubits:
                dag.add_edge(g, g_opt)
                qubits -= qubits_opt
            if not qubits:
                break
    return dag


def dag_to_circuit(dag: nx.DiGraph) -> cirq.Circuit:
    """Convert a DAG to a circuit"""
    return cirq.Circuit(nx.topological_sort(dag))
