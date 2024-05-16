import cirq
import rustworkx as rx
from .graphs import node_index


def max_gate_weight(circ: cirq.Circuit) -> int:
    """Obtain the maximum gate weight of a circuit"""
    return max([len(g.qubits) for g in circ.all_operations()])


def circuit_to_dag(self) -> rx.PyDiGraph:
    """
    Convert a circuit into a Directed Acyclic Graph (DAG) according to dependency of each gate's qubits.
    """
    all_gates = self.gates
    dag = rx.PyDiGraph(multigraph=False)
    dag.add_nodes_from(all_gates)
    while all_gates:
        g = all_gates.pop(0)
        qregs = set(g.qregs)
        for g_opt in all_gates:  # traverse the subsequent optional gates
            qregs_opt = set(g_opt.qregs)
            if dependent_qubits := qregs_opt & qregs:
                dag.add_edge(node_index(dag, g), node_index(dag, g_opt), {'qubits': list(dependent_qubits)})
                qregs -= qregs_opt
            if not qregs:
                break
    return dag



def dag_to_circuit(dag: rx.PyDiGraph) -> cirq.Circuit:
    """Convert a DAG to a Circuit"""
    node_is_block = isinstance(next(iter(dag.nodes())), cirq.Circuit)
    if isinstance(dag, rx.PyDiGraph):
        if node_is_block:
            return Circuit(reduce(add, [dag[idx].gates for idx in rx.topological_sort(dag)]))
        return Circuit([dag[idx] for idx in rx.topological_sort(dag)])
    else:
        if node_is_block:
            return Circuit(reduce(add, list(nx.topological_sort(dag))))
        return Circuit(list(nx.topological_sort(dag)))



