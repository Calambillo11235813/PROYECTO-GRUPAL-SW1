"""
Graph Data Structure Implementation

This module provides a comprehensive implementation of a graph data structure
with support for both directed and undirected graphs, including common graph
algorithms such as breadth-first search and depth-first search.

Classes:
    Graph: Represents a graph with vertices and edges.

Example:
    >>> graph = Graph(directed=False)
    >>> graph.add_edge(1, 2)
    >>> graph.add_edge(2, 3)
    >>> graph.bfs(1)
    [1, 2, 3]
"""

from typing import Dict, List, Set, Optional
from collections import deque, defaultdict


class Graph:
    """
    A graph data structure implementation.

    This class supports both directed and undirected graphs and provides
    methods for adding vertices and edges, as well as performing various
    graph traversal algorithms.

    Attributes:
        directed: Boolean indicating whether the graph is directed.
        adjacency_list: Dictionary mapping vertices to their adjacent vertices.
    """

    def __init__(self, directed: bool = False) -> None:
        """
        Initialize a new graph.

        Args:
            directed: If True, creates a directed graph; otherwise, creates
                     an undirected graph. Defaults to False.
        """
        self.directed: bool = directed
        self.adjacency_list: Dict[int, List[int]] = defaultdict(list)

    def add_vertex(self, vertex: int) -> None:
        """
        Add a vertex to the graph.

        Args:
            vertex: The vertex to be added.
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, source: int, destination: int) -> None:
        """
        Add an edge between two vertices.

        Args:
            source: The source vertex.
            destination: The destination vertex.
        """
        self.add_vertex(source)
        self.add_vertex(destination)
        self.adjacency_list[source].append(destination)

        if not self.directed:
            self.adjacency_list[destination].append(source)

    def remove_edge(self, source: int, destination: int) -> None:
        """
        Remove an edge between two vertices.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Raises:
            ValueError: If the edge does not exist.
        """
        if destination in self.adjacency_list[source]:
            self.adjacency_list[source].remove(destination)
        else:
            raise ValueError(f"Edge from {source} to {destination} does not exist")

        if not self.directed and source in self.adjacency_list[destination]:
            self.adjacency_list[destination].remove(source)

    def get_vertices(self) -> List[int]:
        """
        Get all vertices in the graph.

        Returns:
            A list of all vertices.
        """
        return list(self.adjacency_list.keys())

    def get_edges(self) -> List[tuple]:
        """
        Get all edges in the graph.

        Returns:
            A list of tuples representing edges.
        """
        edges: List[tuple] = []
        for vertex in self.adjacency_list:
            for neighbor in self.adjacency_list[vertex]:
                if self.directed or vertex < neighbor:
                    edges.append((vertex, neighbor))
        return edges

    def bfs(self, start_vertex: int) -> List[int]:
        """
        Perform breadth-first search starting from a given vertex.

        Args:
            start_vertex: The vertex to start the search from.

        Returns:
            A list of vertices in the order they were visited.

        Raises:
            ValueError: If the start vertex is not in the graph.
        """
        if start_vertex not in self.adjacency_list:
            raise ValueError(f"Vertex {start_vertex} not found in graph")

        visited: Set[int] = set()
        queue: deque = deque([start_vertex])
        result: List[int] = []

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                for neighbor in self.adjacency_list[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return result

    def dfs(self, start_vertex: int) -> List[int]:
        """
        Perform depth-first search starting from a given vertex.

        Args:
            start_vertex: The vertex to start the search from.

        Returns:
            A list of vertices in the order they were visited.

        Raises:
            ValueError: If the start vertex is not in the graph.
        """
        if start_vertex not in self.adjacency_list:
            raise ValueError(f"Vertex {start_vertex} not found in graph")

        visited: Set[int] = set()
        result: List[int] = []
        self._dfs_recursive(start_vertex, visited, result)
        return result

    def _dfs_recursive(self, vertex: int, visited: Set[int], result: List[int]) -> None:
        """
        Recursively perform depth-first search.

        Args:
            vertex: The current vertex being visited.
            visited: Set of already visited vertices.
            result: List to store the traversal order.
        """
        visited.add(vertex)
        result.append(vertex)

        for neighbor in self.adjacency_list[vertex]:
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, result)

    def has_path(self, source: int, destination: int) -> bool:
        """
        Check if there is a path between two vertices.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Returns:
            True if a path exists, False otherwise.
        """
        if source not in self.adjacency_list or destination not in self.adjacency_list:
            return False

        visited: Set[int] = set()
        return self._has_path_recursive(source, destination, visited)

    def _has_path_recursive(self, current: int, destination: int, visited: Set[int]) -> bool:
        """
        Recursively check for a path between vertices.

        Args:
            current: The current vertex.
            destination: The destination vertex.
            visited: Set of visited vertices.

        Returns:
            True if a path exists, False otherwise.
        """
        if current == destination:
            return True

        visited.add(current)

        for neighbor in self.adjacency_list[current]:
            if neighbor not in visited:
                if self._has_path_recursive(neighbor, destination, visited):
                    return True

        return False
