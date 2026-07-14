"""Data-structure builders for writing your own test cases.

These are *testing utilities*, not solutions. They convert between plain Python
lists (easy to type in an assert) and the ListNode / TreeNode objects LeetCode
hands your methods, using LeetCode's own conventions. Standard library only.

Typical use inside a solution file's ``__main__`` block::

    from helpers.structures import to_linked, from_linked, to_tree, from_tree

    head = to_linked([1, 2, 3])
    assert from_linked(Solution().your_method(head)) == [3, 2, 1]

    root = to_tree([1, 2, 3, None, None, 4, 5])
    assert from_tree(Solution().your_method(root)) == [1, 2, 3, None, None, 4, 5]
"""
from collections import deque


class ListNode:
    """Singly-linked list node, matching LeetCode's definition.

    Example::

        node = ListNode(1, ListNode(2))
        node.val   # 1
        node.next.val  # 2
    """

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return "ListNode({})".format(self.val)


class TreeNode:
    """Binary tree node, matching LeetCode's definition.

    Example::

        root = TreeNode(1, TreeNode(2), TreeNode(3))
        root.val, root.left.val, root.right.val  # (1, 2, 3)
    """

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return "TreeNode({})".format(self.val)


def to_linked(values):
    """Build a linked list from a list; return the head (or None if empty).

    Example::

        to_linked([1, 2, 3])  # 1 -> 2 -> 3
    """
    head = None
    for val in reversed(list(values)):
        head = ListNode(val, head)
    return head


def from_linked(node):
    """Flatten a linked list back into a plain list of values.

    Example::

        from_linked(to_linked([1, 2, 3]))  # [1, 2, 3]
    """
    out = []
    while node is not None:
        out.append(node.val)
        node = node.next
    return out


def to_tree(values):
    """Build a binary tree from a LeetCode level-order list with None gaps.

    Example::

        to_tree([1, 2, 3, None, None, 4, 5])
        #     1
        #    / \\
        #   2   3
        #      / \\
        #     4   5
    """
    values = list(values)
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    n = len(values)
    while queue and i < n:
        node = queue.popleft()
        if i < n:
            val = values[i]
            i += 1
            if val is not None:
                node.left = TreeNode(val)
                queue.append(node.left)
        if i < n:
            val = values[i]
            i += 1
            if val is not None:
                node.right = TreeNode(val)
                queue.append(node.right)
    return root


def from_tree(node):
    """Serialize a binary tree to LeetCode's level-order list (trailing Nones trimmed).

    Round-trips with ``to_tree``::

        from_tree(to_tree([1, 2, 3, None, None, 4, 5]))  # [1, 2, 3, None, None, 4, 5]
    """
    if node is None:
        return []
    out = []
    queue = deque([node])
    while queue:
        current = queue.popleft()
        if current is None:
            out.append(None)
            continue
        out.append(current.val)
        queue.append(current.left)
        queue.append(current.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    # Self-test: every builder round-trips.
    assert from_linked(to_linked([])) == []
    assert from_linked(to_linked([1])) == [1]
    assert from_linked(to_linked([1, 2, 3, 4])) == [1, 2, 3, 4]

    assert to_linked([]) is None
    assert isinstance(to_linked([5]), ListNode)

    assert from_tree(to_tree([])) == []
    assert to_tree([]) is None
    assert from_tree(to_tree([1])) == [1]
    assert from_tree(to_tree([1, 2, 3])) == [1, 2, 3]

    round_trip = [1, 2, 3, None, None, 4, 5]
    assert from_tree(to_tree(round_trip)) == round_trip

    lopsided = [1, None, 2, None, 3]
    assert from_tree(to_tree(lopsided)) == lopsided

    tree = to_tree([1, 2, 3, None, None, 4, 5])
    assert tree.val == 1
    assert tree.left.val == 2 and tree.right.val == 3
    assert tree.right.left.val == 4 and tree.right.right.val == 5
    assert tree.left.left is None and tree.left.right is None

    print("helpers.structures self-test passed.")
