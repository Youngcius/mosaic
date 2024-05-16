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

