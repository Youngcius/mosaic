import rustworkx as rx
import cirq

from .graphs import node_index, find_predecessors_by_node, find_successors_by_node


def contract_1q_gates_on_dag(dag: rx.PyDiGraph) -> rx.PyDiGraph:
    """
    Aggregate all 1Q gates into neighboring 2Q gates
    After this pass, each node in DAG is a 2Q block (Circuit instance), including only one 2Q gate
    """
    dag = dag.copy()
    nodes_2q_gate = [node for node in dag.nodes() if isinstance(node, cirq.GateOperation) and len(node.qubits) == 2]

    for g in nodes_2q_gate:
        block = cirq.Circuit([g])
        dag[node_index(dag, g)] = block
        while True:
            predecessors_1q = find_predecessors_by_node(dag, node_index(dag, block),
                                                        lambda node: isinstance(node, cirq.GateOperation) and len(node.qubits) == 1)
            successors_1q = find_successors_by_node(dag, node_index(dag, block),
                                                    lambda node: isinstance(node, cirq.GateOperation) and len(node.qubits) == 1)
            if not predecessors_1q and not successors_1q:  # there is no 1Q gate in the neighborhood
                break
            for g_pred in predecessors_1q:
                block.insert(0, g_pred)
                dag.contract_nodes([node_index(dag, block), node_index(dag, g_pred)], block)
            for g_succ in successors_1q:
                block.append(g_succ)
                dag.contract_nodes([node_index(dag, block), node_index(dag, g_succ)], block)

    return dag
