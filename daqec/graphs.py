"""
Universal graph operation utilities, especially for "rustworkx" backend
"""
import cirq
import networkx as nx
import rustworkx as rx
import pydot
import matplotlib.pyplot as plt
from typing import Callable, List, Any, Union
from IPython.display import Image


def rx_to_nx_graph(graph):
    """Convert a rustworkx PyGraph or PyDiGraph to a networkx graph."""
    edge_list = [(graph[x[0]], graph[x[1]], x[2]) for x in graph.weighted_edge_list()]

    if isinstance(graph, rx.PyGraph):
        if graph.multigraph:
            return nx.MultiGraph(edge_list)
        else:
            return nx.Graph(edge_list)
    else:
        if graph.multigraph:
            return nx.MultiDiGraph(edge_list)
        else:
            return nx.DiGraph(edge_list)


def nx_to_rx_graph(graph):
    """Convert a networkx graph to a rustworkx PyGraph."""
    return rx.networkx_converter(graph)


def draw_circ_dag_mpl(dag: Union[nx.DiGraph, rx.PyDiGraph], fname=None, figsize=None, fix_layout=False):
    from .circuits import repr_circuit
    from networkx.drawing.nx_pydot import graphviz_layout

    if isinstance(dag, rx.PyDiGraph):
        dag = rx_to_nx_graph(dag)

    colors = {1: 'white', 2: 'lightblue', 3: 'lightgreen', 4: 'lightpink',
              5: 'lightyellow', 6: 'lightgray', 7: 'lightcyan', 8: 'lightcoral'}
    node_colors = [colors[len(g.qubits)] if isinstance(g, cirq.GateOperation) else colors[len(g.all_qubits())] for g in
                   dag.nodes]
    if fix_layout:
        pos = graphviz_layout(dag, prog='dot')
    else:
        pos = None

    if figsize:
        plt.figure(figsize=figsize)

    nx.draw(dag, pos, with_labels=True,
            labels={node: (str(node) if isinstance(node, cirq.GateOperation) else repr_circuit(node)) for node in
                    dag.nodes}, node_color=node_colors,
            edgecolors='k',
            node_size=800, font_size=6, font_weight='bold')
    if fname:
        plt.savefig(fname)


def draw_circ_dag_graphviz(dag: Union[nx.DiGraph, rx.PyDiGraph], fname: str = None) -> Image:
    from .circuits import repr_circuit
    
    if isinstance(dag, rx.PyDiGraph):
        dag = rx_to_nx_graph(dag)

    dot = pydot.Dot(graph_type='digraph')
    gate_to_node = {}
    colors = {1: 'white', 2: 'lightblue', 3: 'lightgreen', 4: 'lightpink',
              5: 'lightyellow', 6: 'lightgray', 7: 'lightcyan', 8: 'lightcoral'}
    for g in dag.nodes:
        node = pydot.Node(hash(g), label=str(g) if isinstance(g, cirq.GateOperation) else repr_circuit(g),
                          fillcolor=colors[len(g.qubits)] if isinstance(g, cirq.GateOperation) else colors[
                              len(g.all_qubits())],
                          style='filled')
        gate_to_node[g] = node
        dot.add_node(node)
    for edge in dag.edges:
        dot.add_edge(pydot.Edge(gate_to_node[edge[0]], gate_to_node[edge[1]]))
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
    return next(idx for idx in graph.node_indices() if graph[idx] == node)
