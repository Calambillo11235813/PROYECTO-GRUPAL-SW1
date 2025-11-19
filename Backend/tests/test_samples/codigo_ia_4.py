"""
Dynamic Programming Solutions Module

This module provides implementations of common dynamic programming algorithms
including Fibonacci sequence, longest common subsequence, and knapsack problem.

Functions:
    fibonacci_dp(n: int) -> int
    fibonacci_memoization(n: int, memo: dict) -> int
    longest_common_subsequence(text1: str, text2: str) -> int
    knapsack(weights: List[int], values: List[int], capacity: int) -> int
    coin_change(coins: List[int], amount: int) -> int

Example:
    >>> fibonacci_dp(10)
    55
    >>> longest_common_subsequence("abcde", "ace")
    3
"""

from typing import List, Dict, Optional


def fibonacci_dp(n: int) -> int:
    """
    Calculate the nth Fibonacci number using dynamic programming.

    This function uses a bottom-up approach to calculate the Fibonacci
    number, storing intermediate results in an array.

    Args:
        n: The position in the Fibonacci sequence to calculate.

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer")

    if n <= 1:
        return n

    dp: List[int] = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def fibonacci_memoization(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """
    Calculate the nth Fibonacci number using memoization.

    This function uses a top-down approach with memoization to calculate
    the Fibonacci number efficiently.

    Args:
        n: The position in the Fibonacci sequence to calculate.
        memo: Dictionary to store previously calculated values.

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer")

    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fibonacci_memoization(n - 1, memo) + fibonacci_memoization(n - 2, memo)
    return memo[n]


def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Find the length of the longest common subsequence between two strings.

    This function uses dynamic programming to find the longest subsequence
    that appears in both strings in the same relative order.

    Args:
        text1: The first string.
        text2: The second string.

    Returns:
        The length of the longest common subsequence.

    Time Complexity: O(m * n) where m and n are the lengths of the strings
    Space Complexity: O(m * n)
    """
    if not text1 or not text2:
        return 0

    m, n = len(text1), len(text2)
    dp: List[List[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Solve the 0/1 knapsack problem using dynamic programming.

    Given weights and values of n items, put these items in a knapsack of
    capacity to get the maximum total value in the knapsack.

    Args:
        weights: List of item weights.
        values: List of item values.
        capacity: Maximum capacity of the knapsack.

    Returns:
        The maximum value that can be obtained.

    Raises:
        ValueError: If weights and values have different lengths or if any
                   weight or value is negative.

    Time Complexity: O(n * capacity)
    Space Complexity: O(n * capacity)
    """
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same length")

    if any(w < 0 for w in weights) or any(v < 0 for v in values):
        raise ValueError("Weights and values must be non-negative")

    if capacity < 0:
        raise ValueError("Capacity must be non-negative")

    n = len(weights)
    dp: List[List[int]] = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


def coin_change(coins: List[int], amount: int) -> int:
    """
    Find the minimum number of coins needed to make up a given amount.

    This function uses dynamic programming to find the fewest number of coins
    that are needed to make up the amount. If the amount cannot be made up by
    any combination of the coins, return -1.

    Args:
        coins: List of coin denominations.
        amount: The target amount.

    Returns:
        The minimum number of coins needed, or -1 if impossible.

    Raises:
        ValueError: If amount is negative or if any coin value is non-positive.

    Time Complexity: O(amount * len(coins))
    Space Complexity: O(amount)
    """
    if amount < 0:
        raise ValueError("Amount must be non-negative")

    if any(c <= 0 for c in coins):
        raise ValueError("All coin values must be positive")

    dp: List[int] = [float("inf")] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1
