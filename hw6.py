"""
COMP 614
Homework 6: DFS + PageRank
Ross Roberts
"""

import comp614_module6


def bfs_dfs(graph, start_node, rac_class):
    """
    Performs a breadth-first search on graph starting at the given node.
    Returns a two-element tuple containing a dictionary mapping each visited
    node to its distance from the start node and a dictionary mapping each
    visited node to its parent node.
    """
    # Initialize all data structures
    rac = rac_class()

    dist = {}
    parent = {}

    # Initialize distances and parents; no nodes have been visited yet
    for node in graph.nodes():
        dist[node] = float("inf")
        parent[node] = None

    # Initialize start node's distance to 0
    dist[start_node] = 0
    rac.push(start_node)

    # Continue as long as there are new reachable nodes
    while rac:
        node = rac.pop()
        nbrs = graph.get_neighbors(node)

        for nbr in nbrs:
            # Only update neighbors that have not been seen before
            if dist[nbr] == float('inf'):
                dist[nbr] = dist[node] + 1
                parent[nbr] = node
                rac.push(nbr)

    return parent


def recursive_dfs(graph, start_node, parent):
    """
    Given a graph, a start node from which to search, and a mapping of nodes to
    their parents, performs a recursive depth-first search on graph from the 
    given start node, populating the parents mapping as it goes.
    """
    neighbors = graph.get_neighbors(start_node)
    
    for neighbor in neighbors:
        if neighbor not in parent:
            parent[neighbor] = start_node
            recursive_dfs(graph, neighbor, parent)

# graphy = comp614_module6.file_to_graph('test5.txt')
# print(bfs_dfs(graphy, 'C', comp614_module6.Stack()))
# recursive_dfs(graphy, 'C', {'C' : None})

def get_inbound_nbrs(graph):
    """
    Given a directed graph, returns a mapping of each node n in the graph to
    the set of nodes that have edges into n.
    """
    inbound_nbrs = {}
    nodes = graph.nodes()

    for node in nodes:
        inbound_nbrs[node] = set([])

    for node in nodes:
        neighbors = graph.get_neighbors(node)
        for neighbor in neighbors:
            inbound_nbrs[neighbor].add(node)

    return inbound_nbrs


def remove_sink_nodes(graph):
    """
    Given a directed graph, returns a new copy of the graph where every node that
    was a sink node in the original graph now has an outbound edge linking it to 
    every other node in the graph (excluding itself).
    """
    new_graph = graph.copy()
    nodes1 = new_graph.nodes()

    for node1 in nodes1:
        neighbors = new_graph.get_neighbors(node1)
        if len(neighbors) == 0:
            nodes2 = set(nodes1)
            for node2 in nodes2:
                if node1 != node2:
                    new_graph.add_edge(node1, node2)

    return new_graph


def page_rank(graph, damping):
    """
    Given a directed graph and a damping factor, implements the PageRank algorithm
    -- continuing until delta is less than 10^-8 -- and returns a dictionary that 
    maps each node in the graph to its page rank.
    """
    p_rank = {}
    new_graph = remove_sink_nodes(graph)
    nodes = new_graph.nodes()
    inbound_nbrs = get_inbound_nbrs(new_graph)
    delta_k = float('inf')

    for node in nodes:
        p_rank[node] = 1 / len(nodes)

    while delta_k > 10e-8:
        current_p_rank = dict(p_rank)
        delta_k = 0

        for node in dict(current_p_rank):
            inbound_sum = 0

            for inbound_nbr in inbound_nbrs[node]:
                out_degree = len(new_graph.get_neighbors(inbound_nbr))
                inbound_sum += (p_rank[inbound_nbr] / out_degree)

            current_p_rank[node] = ((1 - damping) / len(nodes)) + (damping * inbound_sum)
            delta_k += abs(current_p_rank[node] - p_rank[node])

        p_rank = current_p_rank

    return p_rank

# def sort_func(item):
#     return item[1]

# graphy2 = comp614_module6.file_to_graph('wikipedia_articles_streamlined.txt')
# rank_dict = page_rank(graphy2, 0.85)
# rank_list = list(rank_dict.items())
# rank_list.sort(reverse = True, key = sort_func)
# print(rank_list[:10])