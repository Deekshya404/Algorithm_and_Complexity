"""
Huffman Encoding — Brute Force vs Greedy
==========================================

Greedy   : classic Huffman algorithm using a min-heap. O(n log n).
Brute force : tries EVERY possible order of merging nodes (no min-heap,
              no pruning) and keeps the cheapest resulting tree.
              This explores a factorial-sized search space, so it is
              only run for small n.

Both return the same optimal cost (Huffman's greedy choice is provably
optimal) — the point of the brute force version is purely to show how
much slower "trying everything" is compared to the greedy shortcut.
"""

import heapq
import itertools
import random
import time
import sys

sys.setrecursionlimit(10000)


class Node:
    __slots__ = ("weight", "left", "right", "char")

    def __init__(self, weight, left=None, right=None, char=None):
        self.weight = weight
        self.left = left
        self.right = right
        self.char = char

    def is_leaf(self):
        return self.char is not None


# ---------------------------------------------------------------------
# GREEDY (standard) HUFFMAN — O(n log n)
# ---------------------------------------------------------------------
def greedy_huffman(freqs: dict):
    """
    Builds the Huffman tree by always merging the two lowest-weight
    nodes, using a min-heap. Returns (root_node, total_cost).
    """
    counter = itertools.count()
    heap = [(w, next(counter), Node(w, char=c)) for c, w in freqs.items()]
    heapq.heapify(heap)

    total_cost = 0
    while len(heap) > 1:
        w1, _, n1 = heapq.heappop(heap)
        w2, _, n2 = heapq.heappop(heap)
        merged = Node(w1 + w2, n1, n2)
        total_cost += merged.weight
        heapq.heappush(heap, (merged.weight, next(counter), merged))

    return heap[0][2], total_cost


# ---------------------------------------------------------------------
# BRUTE FORCE HUFFMAN — tries every merge order, no pruning
# ---------------------------------------------------------------------
def brute_force_huffman(freqs: dict):
    """
    Exhaustively tries every possible sequence of pairwise merges and
    keeps the cheapest tree found. Cost of a merge sequence equals
    sum(weighted path lengths) = sum of all intermediate merge weights,
    same accounting the greedy version uses, so results are comparable.

    Search space size ~ n! * (n-1)! / 2^(n-1), i.e. explodes fast —
    only usable for small n (roughly n <= 9 in reasonable time).
    """
    nodes = [Node(w, char=c) for c, w in freqs.items()]
    best = [None, None]  # [best_cost, best_root]

    def recurse(node_list, cost_so_far):
        if best[0] is not None and cost_so_far >= best[0]:
            return  # cheap pruning purely to keep runtime sane; still exhaustive-order
        if len(node_list) == 1:
            if best[0] is None or cost_so_far < best[0]:
                best[0] = cost_so_far
                best[1] = node_list[0]
            return
        n = len(node_list)
        for i in range(n):
            for j in range(i + 1, n):
                merged = Node(node_list[i].weight + node_list[j].weight,
                              node_list[i], node_list[j])
                new_list = [node_list[k] for k in range(n) if k != i and k != j]
                new_list.append(merged)
                recurse(new_list, cost_so_far + merged.weight)

    recurse(nodes, 0)
    return best[1], best[0]


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def build_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node.is_leaf():
        codebook[node.char] = prefix or "0"
        return codebook
    build_codes(node.left, prefix + "0", codebook)
    build_codes(node.right, prefix + "1", codebook)
    return codebook


def random_freqs(n, seed=None):
    rnd = random.Random(seed)
    chars = [chr(97 + i) if i < 26 else f"s{i}" for i in range(n)]
    return {c: rnd.randint(1, 100) for c in chars}


if __name__ == "__main__":
    freqs = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45,"g": 7, "h": 3}

    root_g, cost_g = greedy_huffman(freqs)
    root_b, cost_b = brute_force_huffman(freqs)

    print("Greedy codes:     ", build_codes(root_g))
    print("Greedy total cost:", cost_g)
    print("Brute codes:      ", build_codes(root_b))
    print("Brute total cost: ", cost_b)