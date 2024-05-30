"""
Sequential partitioning algorithm by forward scanning on the circuit
"""

import cirq
import numpy as np
import rustworkx as rx
from typing import List, Set, Union
from rich.console import Console
from functools import reduce
from operator import add

from . import circuits, passes
from .graphs import node_index

console = Console()



def seq_partition(circ: cirq.Circuit, grain: int = 2) -> List[cirq.Circuit]:
    """
    Partition a list of circuits into groups of grain-qubit blocks (subcircuits) by one-round forward pass.
    ---
    Complexity: O(m*n), m is the number of 2Q gates, n is the number of qubits
    """
    if grain <= 1:
        raise ValueError("grain must be greater than 1.")
    if grain < circuits.max_gate_weight(circ):
        raise ValueError("grain must be no less than the maximum gate weight of the circuit.")

    circ_nl = circ.copy()
    blocks = []

    # peel all 1Q gates from the first layer
    first_1q_gates = []
    while first_layer_1q := [g for g in circ_nl[0] if cirq.num_qubits(g) == 1]:
        first_1q_gates.extend(first_layer_1q)
        circ_nl.batch_remove([(0, g) for g in first_layer_1q])
        circ_nl = cirq.Circuit(list(circ_nl.all_operations()))

    dag = circuits.circuit_to_dag(circ_nl)
    while circ_nl:  # for each epoch, select a block with the most nonlocal gates
        front_layer = passes.obtain_front_layer(dag)
        block_candidates = [cirq.Circuit([g]) for g in front_layer]
        for i, (g, block) in enumerate(zip(front_layer, block_candidates)):
            dag_peeled = dag.copy()
            dag_peeled.remove_node(node_index(dag, g))
            block_candidates[i] = _extend_block_over_dag(block, dag_peeled, grain)

        scores = [_block_score(block) for block in block_candidates]
        block = block_candidates[np.argmax(scores)]  # the selected extended block
        for g in block.all_operations():
            circ_nl = circuits.remove_gate(circ_nl, g)
            dag.remove_node(node_index(dag, g))
        blocks.append(block)

    # add 1Q gates from first_1q_gates back to corresponding blocks
    dag = circuits.circuit_to_dag(circ)
    for g in reversed(first_1q_gates):
        for blk in blocks:
            if circuits.has_gate(blk, list(dag.successors(node_index(dag, g)))[0]):
                blk.insert(0, g)
                break

    assert sum([circuits.num_gates(blk) for blk in blocks]) == circuits.num_gates(circ), "num_gates mismatch"
    # console.print('num_gates of all blocks: {}'.format(sum([circuits.num_gates(blk) for blk in blocks])))
    # console.print('num_gates: {}'.format(circuits.num_gates(circ)))

    # NOTE: in this algorithm we do not need to unify the blocks since they are already sorted
    return blocks


def _extend_block_over_dag(block: cirq.Circuit, dag: rx.PyDiGraph, max_weight: int) -> cirq.Circuit:
    """Search applicable gates from the neighbors of block among this DAG to add them to block"""
    block = block.copy()

    if not dag.num_nodes():
        return block

    while front_layer := passes.obtain_front_layer(dag):
        optional_gates = _sort_gates_on_ref_qubits(front_layer, block.all_qubits())
        if len(block.all_qubits() | set(optional_gates[0].qubits)) > max_weight:
            break
        for g in optional_gates:
            if len(block.all_qubits() | set(g.qubits)) <= max_weight:
                block.append(g)
                dag.remove_node(node_index(dag, g))
            else:
                break

    return block


def _sort_gates_on_ref_qubits(gates: List[cirq.GateOperation], ref_qubits: Union[List[int], Set[int]]) -> List[cirq.GateOperation]:
    """
    Sort the gates according to the number of qubits overlapped and additional overhead with the given set of qubits
    Sort by: 1) additional overhead (ascending); 2) number of qubits overlapped (descending)
    """
    return sorted(gates, key=lambda g: (len(set(g.qubits) - set(ref_qubits)),
                                        - len(set(g.qubits) & set(ref_qubits))))



def _block_score(block: Union[List[cirq.GateOperation], cirq.Circuit, List[cirq.Circuit]], init_score: float = 0) -> float:
    if isinstance(block, cirq.Circuit):
        circ = block
    elif isinstance(block, list) and isinstance(block[0], cirq.GateOperation):
        circ = cirq.Circuit(block)
    elif isinstance(block, list) and isinstance(block[0], cirq.Circuit):
        circ = reduce(add, block)
    else:
        raise ValueError('Invalid type of block.')

    # score_local = 0.1 * (circuits.num_gates(circ) - circuits.num_nonlocal_gates(circ))
    score_nl = circuits.num_nonlocal_gates(circ)  # the number of nonlocal gates contributes the most
    # return init_score + score_nl + 0.1 * score_local
    return score_nl
