import rustworkx as rx
import cirq
from typing import Union, List, Tuple

from .graphs import node_index, find_predecessors_by_node, find_successors_by_node


def obtain_front_layer(dag_or_circ: Union[cirq.Circuit, rx.PyDiGraph],
                       return_indices: bool = False) -> Union[
    List[Union[cirq.GateOperation, cirq.Circuit]], Tuple[List[Union[cirq.GateOperation, cirq.Circuit]], List[int]]]:
    """
    Obtain front layer (with in_degree == 0) of the DAG.
    Since the node of DAG might be Gate instance or Circuit instance, result is a list of Gate or Circuit.
    """
    if isinstance(dag_or_circ, cirq.Circuit):
        dag = dag_or_circ.to_dag()
    else:
        dag = dag_or_circ
    front_layer = []
    front_layer_indices = []
    for node_idx in dag.node_indices():
        if dag.in_degree(node_idx) == 0:
            front_layer.append(dag[node_idx])
            front_layer_indices.append(node_idx)
    if return_indices:
        return front_layer, front_layer_indices
    return front_layer


def contract_1q_gates_on_dag(dag: rx.PyDiGraph) -> rx.PyDiGraph:
    """
    Aggregate all 1Q gates into neighboring 2Q gates
    After this pass, each node in DAG is a 2Q block (Circuit instance), including only one 2Q gate
    """
    dag = dag.copy()
    nodes_2q_gate = [node for node in dag.nodes() if isinstance(node, cirq.GateOperation) and cirq.num_qubits(node) == 2]

    for g in nodes_2q_gate:
        block = cirq.Circuit([g])
        dag[node_index(dag, g)] = block
        while True:
            predecessors_1q = find_predecessors_by_node(dag, node_index(dag, block),
                                                        lambda node: isinstance(node, cirq.GateOperation) and cirq.num_qubits(node) == 1)
            successors_1q = find_successors_by_node(dag, node_index(dag, block),
                                                    lambda node: isinstance(node, cirq.GateOperation) and cirq.num_qubits(node) == 1)
            if not predecessors_1q and not successors_1q:  # there is no 1Q gate in the neighborhood
                break
            for g_pred in predecessors_1q:
                block.insert(0, g_pred)
                dag.contract_nodes([node_index(dag, block), node_index(dag, g_pred)], block)
            for g_succ in successors_1q:
                block.append(g_succ)
                dag.contract_nodes([node_index(dag, block), node_index(dag, g_succ)], block)

    return dag



