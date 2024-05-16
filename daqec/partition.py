"""
Sequential partitioning algorithm
"""

import cirq
import numpy as np
import rustworkx as rx
from typing import List
from . import utils
from .graphs import node_index, find_predecessors_by_node, find_successors_by_node


def seq_partition(circ: cirq.Circuit, grain: int = 2) -> List[cirq.Circuit]:
    """
    Partition a list of circuits into groups of grain-qubit blocks (subcircuits) by one-round forward pass.
    ---
    Complexity: O(m*n), m is the number of 2Q gates, n is the number of qubits
    """
    if grain <= 1:
        raise ValueError("grain must be greater than 1.")
    if grain < utils.max_gate_weight(circ):
        raise ValueError("grain must be no less than the maximum gate weight of the circuit.")

    # blocks = []
    # return blocks
    raise NotImplementedError("Implement the sequential partitioning algorithm here.")





def contract_1q_gates_on_dag(dag: rx.PyDiGraph) -> rx.PyDiGraph:
    """
    Aggregate all 1Q gates into neighboring 2Q gates
    After this pass, each node in DAG is a 2Q block (Circuit instance), including only one 2Q gate
    """
    dag = dag.copy()
    nodes_2q_gate = [node for node in dag.nodes() if isinstance(node, Gate) and node.num_qregs == 2]

    # console.print('nodes_2q_gate:', nodes_2q_gate)
    # console.print('nodes_2q_gate (indices):', [node_index(dag, node) for node in nodes_2q_gate])

    for g in nodes_2q_gate:
        # console.print({idx: dag[idx] for idx in dag.node_indices()})
        # console.print('contracting {} with node index {}'.format(g, node_index(dag, g)), style='bold red')
        block = Circuit([g])
        # dag = nx.relabel_nodes(dag, {g: block})
        dag[node_index(dag, g)] = block
        while True:
            # predecessors_1q_gate = [g_nb for g_nb in list(dag.predecessors(block)) if
            #                         isinstance(g_nb, Gate) and g_nb.num_qregs == 1]
            # successors_1q_gate = [g_nb for g_nb in list(dag.successors(block)) if
            #                       isinstance(g_nb, Gate) and g_nb.num_qregs == 1]
            predecessors_1q = find_predecessors_by_node(dag, node_index(dag, block),
                                                        lambda node: isinstance(node, Gate) and node.num_qregs == 1)
            successors_1q = find_successors_by_node(dag, node_index(dag, block),
                                                    lambda node: isinstance(node, Gate) and node.num_qregs == 1)
            if not predecessors_1q and not successors_1q:  # there is no 1Q gate in the neighborhood
                break
            # console.print('predecessors_1q: {}'.format(predecessors_1q), style='blue')
            # console.print('successors_1q: {}'.format(successors_1q), style='blue')
            for g_pred in predecessors_1q:
                block.insert(0, g_pred)
                dag.contract_nodes([node_index(dag, block), node_index(dag, g_pred)], block)
            for g_succ in successors_1q:
                block.append(g_succ)
                dag.contract_nodes([node_index(dag, block), node_index(dag, g_succ)], block)
            # print(block.to_cirq())
    return dag


