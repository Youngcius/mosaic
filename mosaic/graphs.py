"""
Universal graph operation utilities, especially for "rustworkx" backend
"""
import cirq
import rustworkx as rx
import pydot
import matplotlib.pyplot as plt
from typing import Callable, List, Any
from IPython.display import Image


def draw_circ_dag_mpl(dag: rx.PyDiGraph, fname=None, figsize=None):
    from .circuits import repr_circuit
    from rustworkx.visualization import mpl_draw

    colors = {1: 'white', 2: 'lightblue', 3: 'lightgreen', 4: 'lightpink',
              5: 'lightyellow', 6: 'lightgray', 7: 'lightcyan', 8: 'lightcoral'}
    node_colors = [colors[cirq.num_qubits(g)] for g in dag.nodes()]

    if figsize:
        plt.figure(figsize=figsize)

    mpl_draw(dag, with_labels=True,
            labels=str if isinstance(next(iter(dag.nodes())), cirq.GateOperation) else repr_circuit, 
            node_color=node_colors,
            edgecolors='grey',
            node_size=450, font_size=6, font_weight='bold')
    if fname:
        plt.savefig(fname)


def draw_circ_dag_graphviz(dag: rx.PyDiGraph, fname: str = None) -> Image:
    from .circuits import repr_circuit

    dot = pydot.Dot(graph_type='digraph')
    gate_to_node = {}
    colors = {1: 'white', 2: 'lightblue', 3: 'lightgreen', 4: 'lightpink',
              5: 'lightyellow', 6: 'lightgray', 7: 'lightcyan', 8: 'lightcoral'}
    for idx in dag.node_indices():
        node = pydot.Node(idx, label=str(dag[idx]) if isinstance(dag[idx], cirq.GateOperation) else repr_circuit(dag[idx]),
                          fillcolor=colors[cirq.num_qubits(dag[idx])], style='filled')
        gate_to_node[idx] = node
        dot.add_node(node)
    for src, dst in dag.edge_list():
        dot.add_edge(pydot.Edge(gate_to_node[src], gate_to_node[dst]))
    dot.set_rankdir('LR')
    if fname:
        dot.write_png(fname)
    return Image(dot.create_png())


def find_successors_by_node(dag: rx.PyDiGraph, idx: int, predicate: Callable) -> List[Any]:
    """
    Return a filtered list of successors data such that each node matches the filter.

    Args:
        dag: The DAG to search
        idx: The index of the node to get the successors for
        predicate: The filter function to use for matching each of its successor nodes

    Returns:
        A list of the node data for all the successors who match the filter
    """
    return [node for node in dag.successors(idx) if predicate(node)]


def find_successor_indices_by_node(dag: rx.PyDiGraph, idx: int, predicate: Callable) -> List[int]:
    """Similar to find_successors_by_node but returns the indices of the successor nodes instead of the data."""
    successors = find_successors_by_node(dag, idx, predicate)
    return [node_index(dag, node) for node in successors]


def find_predecessors_by_node(dag: rx.PyDiGraph, idx: int, predicate: Callable) -> List[Any]:
    """
    Return a filtered list of predecessors data such that each node has at least one edge data which matches the filter.

    Args:
        dag: The DAG to search
        idx: The index of the node to get the predecessors for
        predicate: The filter function to use for matching each of its predecessor nodes

    Returns:
        A list of the node data for all the predecessors who match the filter
    """
    return [node for node in dag.predecessors(idx) if predicate(node)]


def find_predecessor_indices_by_node(dag: rx.PyDiGraph, idx: int, predicate: Callable) -> List[int]:
    """Similar to find_predecessors_by_node but returns the indices of the predecessor nodes instead of the data."""
    predecessors = find_predecessors_by_node(dag, idx, predicate)
    return [node_index(dag, node) for node in predecessors]


def filter_nodes(dag: rx.PyDiGraph, predicate: Callable) -> List[Any]:
    """Return a list of node indices for all nodes in the DAG which match the filter."""
    # return [idx for idx, node in enumerate(dag.nodes()) if predicate(node)]
    return [dag[idx] for idx in dag.node_indices() if predicate(dag[idx])]


def node_index(graph: rx.PyDiGraph, node: Any) -> int:
    """Return the index of the node in the graph."""
    return next(idx for idx in graph.node_indices() if id(graph[idx]) == id(node))
