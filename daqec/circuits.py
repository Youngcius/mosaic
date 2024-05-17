import cirq
import rustworkx as rx
from functools import reduce
from typing import List
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


def dag_to_circuit(dag: rx.PyDiGraph) -> cirq.Circuit:
    """Convert a DAG to a Circuit"""
    node_is_block = isinstance(next(iter(dag.nodes())), cirq.Circuit)
    if node_is_block:
        return cirq.Circuit(reduce(add, [list(dag[idx].all_operations()) for idx in rx.topological_sort(dag)]))
    return cirq.Circuit([dag[idx] for idx in rx.topological_sort(dag)])


def remove_gate(circ: cirq.Circuit, gate: cirq.GateOperation, by_value: bool = False) -> cirq.Circuit:
    """Remove a gate from a circuit"""
    if by_value:
        cirq.Circuit([g for g in circ.all_operations() if g != gate])
    return cirq.Circuit([g for g in circ.all_operations() if id(g) != id(gate)])


def has_gate(circ: cirq.Circuit, gate: cirq.GateOperation, by_value: bool = False) -> bool:
    """Check if a circuit has a gate"""
    if by_value:
        return any([g == gate for g in circ.all_operations()])
    return any([id(g) == id(gate) for g in circ.all_operations()])


def num_gates(circ: cirq.Circuit) -> int:
    """Obtain the number of gates in a circuit"""
    return len(list(circ.all_operations()))


def num_nonlocal_gates(circ: cirq.Circuit) -> int:
    """Obtain the number of non-local gates in a circuit"""
    return len([g for g in circ.all_operations() if cirq.num_qubits(g) > 1])


def blocks_to_circuit(blocks: List[cirq.Circuit]) -> cirq.Circuit:
    """Unify a list of blocks into a circuit"""
    return cirq.Circuit(reduce(add, [list(blk.all_operations()) for blk in blocks]))
