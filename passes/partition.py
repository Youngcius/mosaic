"""
Sequential partitioning algorithm
"""

import cirq
import numpy as np
import networkx as nx
from typing import List
from . import utils


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


def contract_1q_gates_on_dag(dag: nx.DiGraph) -> nx.DiGraph:
    """
    Aggregate all 1Q gates into neighboring 2Q gates
    After this pass, each node in DAG is a 2Q block (Circuit instance), including only one 2Q gate
    """
    dag = dag.copy()
    nodes_2q_gate = [node for node in dag.nodes if isinstance(node, cirq.GateOperation) and len(node.qubits) == 2]
    for g in nodes_2q_gate:
        block = cirq.Circuit([g])
        print('current block:')
        print(block)
        dag = nx.relabel_nodes(dag, {g: block})
        while True:
            predecessors_1q_gate = [g_nb for g_nb in list(dag.predecessors(block)) if
                                    isinstance(g_nb, cirq.GateOperation) and len(g_nb.qubits) == 1]
            successors_1q_gate = [g_nb for g_nb in list(dag.successors(block)) if
                                  isinstance(g_nb, cirq.GateOperation) and len(g_nb.qubits) == 1]
            if not predecessors_1q_gate and not successors_1q_gate:  # there is no 1Q gate in the neighborhood
                break
            for g_pred in predecessors_1q_gate:
                block.insert(0, g_pred)
                dag = nx.contracted_nodes(dag, block, g_pred, self_loops=False)
            for g_succ in successors_1q_gate:
                block.append(g_succ)
                dag = nx.contracted_nodes(dag, block, g_succ, self_loops=False)
    return dag


