import heapq
import matplotlib.pyplot as plt

# ---------------- Node Class ----------------
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# ---------------- Build Huffman Tree ----------------
def build_huffman_tree(characters, frequencies):
    heap = []

    for ch, freq in zip(characters, frequencies):
        heapq.heappush(heap, Node(ch, freq))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]


# ---------------- Assign Positions ----------------
def assign_positions(root):
    pos = {}
    leaf_x = [0]  # mutable counter

    def dfs(node, depth):
        if node is None:
            return

        # Leaf node
        if node.left is None and node.right is None:
            x = leaf_x[0]
            leaf_x[0] += 2          # spacing between leaves
            pos[node] = (x, -depth)
            return

        # Internal node
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

        lx = pos[node.left][0]
        rx = pos[node.right][0]
        pos[node] = ((lx + rx) / 2, -depth)

    dfs(root, 0)
    return pos


# ---------------- Draw Tree ----------------
def draw_tree(root):
    pos = assign_positions(root)

    fig, ax = plt.subplots(figsize=(14, 8))

    # Draw edges
    for node, (x, y) in pos.items():

        if node.left:
            x2, y2 = pos[node.left]
            ax.plot([x, x2], [y, y2], 'k-', lw=2)
            ax.text((x+x2)/2-0.15, (y+y2)/2, "0",
                    color="blue", fontsize=12)

        if node.right:
            x2, y2 = pos[node.right]
            ax.plot([x, x2], [y, y2], 'k-', lw=2)
            ax.text((x+x2)/2+0.15, (y+y2)/2, "1",
                    color="red", fontsize=12)

    # Draw nodes
    for node, (x, y) in pos.items():

        if node.char is None:
            label = f"{node.freq}"
            color = "lightgreen"
        else:
            label = f"{node.char}\n{node.freq}"
            color = "skyblue"

        circle = plt.Circle((x, y), 0.3,
                            facecolor=color,
                            edgecolor="black",
                            linewidth=2)

        ax.add_patch(circle)
        ax.text(x, y, label,
                ha='center',
                va='center',
                fontsize=11,
                weight='bold')

    # Automatically fit everything
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]

    ax.set_xlim(min(xs)-1, max(xs)+1)
    ax.set_ylim(min(ys)-1, max(ys)+1)

    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Huffman Tree", fontsize=18)
    plt.tight_layout()
    plt.show()

# ---------------- Main ----------------
characters = ['A', 'B', 'C', 'D', 'E', 'F','G','H']
frequencies = [5, 9, 12, 13, 16, 45, 7, 3]

root = build_huffman_tree(characters, frequencies)

draw_tree(root)