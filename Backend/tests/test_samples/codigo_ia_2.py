"""
Binary Search Tree Implementation

This module implements a Binary Search Tree data structure with common operations
including insertion, deletion, searching, and various traversal methods.

Classes:
    TreeNode: Represents a node in the binary search tree.
    BinarySearchTree: Implements the binary search tree with various operations.

Example:
    >>> bst = BinarySearchTree()
    >>> bst.insert(5)
    >>> bst.insert(3)
    >>> bst.insert(7)
    >>> bst.search(3)
    True
"""

from typing import Optional, List


class TreeNode:
    """
    A node in a binary search tree.

    Attributes:
        value: The value stored in the node.
        left: Reference to the left child node.
        right: Reference to the right child node.
    """

    def __init__(self, value: int) -> None:
        """
        Initialize a new tree node.

        Args:
            value: The value to be stored in the node.
        """
        self.value: int = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BinarySearchTree:
    """
    A Binary Search Tree implementation.

    This class provides methods for inserting, deleting, and searching for values
    in a binary search tree, as well as various traversal methods.

    Attributes:
        root: The root node of the tree.
    """

    def __init__(self) -> None:
        """Initialize an empty binary search tree."""
        self.root: Optional[TreeNode] = None

    def insert(self, value: int) -> None:
        """
        Insert a new value into the binary search tree.

        Args:
            value: The value to be inserted.
        """
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: TreeNode, value: int) -> None:
        """
        Recursively insert a value into the tree.

        Args:
            node: The current node being examined.
            value: The value to be inserted.
        """
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value: int) -> bool:
        """
        Search for a value in the binary search tree.

        Args:
            value: The value to search for.

        Returns:
            True if the value is found, False otherwise.
        """
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node: Optional[TreeNode], value: int) -> bool:
        """
        Recursively search for a value in the tree.

        Args:
            node: The current node being examined.
            value: The value to search for.

        Returns:
            True if the value is found, False otherwise.
        """
        if node is None:
            return False

        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def inorder_traversal(self) -> List[int]:
        """
        Perform an inorder traversal of the tree.

        Returns:
            A list of values in inorder sequence.
        """
        result: List[int] = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: Optional[TreeNode], result: List[int]) -> None:
        """
        Recursively perform inorder traversal.

        Args:
            node: The current node being visited.
            result: The list to store the traversal result.
        """
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self) -> List[int]:
        """
        Perform a preorder traversal of the tree.

        Returns:
            A list of values in preorder sequence.
        """
        result: List[int] = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node: Optional[TreeNode], result: List[int]) -> None:
        """
        Recursively perform preorder traversal.

        Args:
            node: The current node being visited.
            result: The list to store the traversal result.
        """
        if node is not None:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self) -> List[int]:
        """
        Perform a postorder traversal of the tree.

        Returns:
            A list of values in postorder sequence.
        """
        result: List[int] = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node: Optional[TreeNode], result: List[int]) -> None:
        """
        Recursively perform postorder traversal.

        Args:
            node: The current node being visited.
            result: The list to store the traversal result.
        """
        if node is not None:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
