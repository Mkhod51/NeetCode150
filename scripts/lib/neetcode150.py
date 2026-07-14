"""Canonical NeetCode 150 problem list — the single source of truth.

Category membership, difficulty, and LeetCode slug were pulled live from the
rendered https://neetcode.io/practice ("NeetCode 150" tab) on 2026-07-14.
LeetCode problem numbers and canonical titles are mapped from those slugs.

This module contains NO solution code and NO approach hints — only public
metadata (number, title, difficulty, slug). scripts/progress.py renders the
README checklist from this list; scripts/new_problem.py reads difficulty back
out of the generated README.

If neetcode.io changes the list, update the tuples below and re-run
`python scripts/progress.py` to regenerate the README.
"""

# (folder_name, display_name) in the order they appear in the README.
CATEGORY_ORDER = [
    ("arrays-hashing", "Arrays & Hashing"),
    ("two-pointers", "Two Pointers"),
    ("sliding-window", "Sliding Window"),
    ("stack", "Stack"),
    ("binary-search", "Binary Search"),
    ("linked-list", "Linked List"),
    ("trees", "Trees"),
    ("tries", "Tries"),
    ("heap-priority-queue", "Heap / Priority Queue"),
    ("backtracking", "Backtracking"),
    ("graphs", "Graphs"),
    ("advanced-graphs", "Advanced Graphs"),
    ("one-d-dp", "1-D Dynamic Programming"),
    ("two-d-dp", "2-D Dynamic Programming"),
    ("greedy", "Greedy"),
    ("intervals", "Intervals"),
    ("math-geometry", "Math & Geometry"),
    ("bit-manipulation", "Bit Manipulation"),
]

# folder -> [(leetcode_number, title, difficulty, slug), ...]
_BY_CATEGORY = {
    "arrays-hashing": [
        (217, "Contains Duplicate", "Easy", "contains-duplicate"),
        (242, "Valid Anagram", "Easy", "valid-anagram"),
        (1, "Two Sum", "Easy", "two-sum"),
        (49, "Group Anagrams", "Medium", "group-anagrams"),
        (347, "Top K Frequent Elements", "Medium", "top-k-frequent-elements"),
        (271, "Encode and Decode Strings", "Medium", "encode-and-decode-strings"),
        (238, "Product of Array Except Self", "Medium", "product-of-array-except-self"),
        (36, "Valid Sudoku", "Medium", "valid-sudoku"),
        (128, "Longest Consecutive Sequence", "Medium", "longest-consecutive-sequence"),
    ],
    "two-pointers": [
        (125, "Valid Palindrome", "Easy", "valid-palindrome"),
        (167, "Two Sum II - Input Array Is Sorted", "Medium", "two-sum-ii-input-array-is-sorted"),
        (15, "3Sum", "Medium", "3sum"),
        (11, "Container With Most Water", "Medium", "container-with-most-water"),
        (42, "Trapping Rain Water", "Hard", "trapping-rain-water"),
    ],
    "sliding-window": [
        (121, "Best Time to Buy and Sell Stock", "Easy", "best-time-to-buy-and-sell-stock"),
        (3, "Longest Substring Without Repeating Characters", "Medium", "longest-substring-without-repeating-characters"),
        (424, "Longest Repeating Character Replacement", "Medium", "longest-repeating-character-replacement"),
        (567, "Permutation in String", "Medium", "permutation-in-string"),
        (76, "Minimum Window Substring", "Hard", "minimum-window-substring"),
        (239, "Sliding Window Maximum", "Hard", "sliding-window-maximum"),
    ],
    "stack": [
        (20, "Valid Parentheses", "Easy", "valid-parentheses"),
        (155, "Min Stack", "Medium", "min-stack"),
        (150, "Evaluate Reverse Polish Notation", "Medium", "evaluate-reverse-polish-notation"),
        (739, "Daily Temperatures", "Medium", "daily-temperatures"),
        (853, "Car Fleet", "Medium", "car-fleet"),
        (84, "Largest Rectangle in Histogram", "Hard", "largest-rectangle-in-histogram"),
    ],
    "binary-search": [
        (704, "Binary Search", "Easy", "binary-search"),
        (74, "Search a 2D Matrix", "Medium", "search-a-2d-matrix"),
        (875, "Koko Eating Bananas", "Medium", "koko-eating-bananas"),
        (153, "Find Minimum in Rotated Sorted Array", "Medium", "find-minimum-in-rotated-sorted-array"),
        (33, "Search in Rotated Sorted Array", "Medium", "search-in-rotated-sorted-array"),
        (981, "Time Based Key-Value Store", "Medium", "time-based-key-value-store"),
        (4, "Median of Two Sorted Arrays", "Hard", "median-of-two-sorted-arrays"),
    ],
    "linked-list": [
        (206, "Reverse Linked List", "Easy", "reverse-linked-list"),
        (21, "Merge Two Sorted Lists", "Easy", "merge-two-sorted-lists"),
        (141, "Linked List Cycle", "Easy", "linked-list-cycle"),
        (143, "Reorder List", "Medium", "reorder-list"),
        (19, "Remove Nth Node From End of List", "Medium", "remove-nth-node-from-end-of-list"),
        (138, "Copy List with Random Pointer", "Medium", "copy-list-with-random-pointer"),
        (2, "Add Two Numbers", "Medium", "add-two-numbers"),
        (287, "Find the Duplicate Number", "Medium", "find-the-duplicate-number"),
        (146, "LRU Cache", "Medium", "lru-cache"),
        (23, "Merge k Sorted Lists", "Hard", "merge-k-sorted-lists"),
        (25, "Reverse Nodes in k-Group", "Hard", "reverse-nodes-in-k-group"),
    ],
    "trees": [
        (226, "Invert Binary Tree", "Easy", "invert-binary-tree"),
        (104, "Maximum Depth of Binary Tree", "Easy", "maximum-depth-of-binary-tree"),
        (543, "Diameter of Binary Tree", "Easy", "diameter-of-binary-tree"),
        (110, "Balanced Binary Tree", "Easy", "balanced-binary-tree"),
        (100, "Same Tree", "Easy", "same-tree"),
        (572, "Subtree of Another Tree", "Easy", "subtree-of-another-tree"),
        (235, "Lowest Common Ancestor of a Binary Search Tree", "Medium", "lowest-common-ancestor-of-a-binary-search-tree"),
        (102, "Binary Tree Level Order Traversal", "Medium", "binary-tree-level-order-traversal"),
        (199, "Binary Tree Right Side View", "Medium", "binary-tree-right-side-view"),
        (1448, "Count Good Nodes in Binary Tree", "Medium", "count-good-nodes-in-binary-tree"),
        (98, "Validate Binary Search Tree", "Medium", "validate-binary-search-tree"),
        (230, "Kth Smallest Element in a BST", "Medium", "kth-smallest-element-in-a-bst"),
        (105, "Construct Binary Tree from Preorder and Inorder Traversal", "Medium", "construct-binary-tree-from-preorder-and-inorder-traversal"),
        (124, "Binary Tree Maximum Path Sum", "Hard", "binary-tree-maximum-path-sum"),
        (297, "Serialize and Deserialize Binary Tree", "Hard", "serialize-and-deserialize-binary-tree"),
    ],
    "tries": [
        (208, "Implement Trie (Prefix Tree)", "Medium", "implement-trie-prefix-tree"),
        (211, "Design Add and Search Words Data Structure", "Medium", "design-add-and-search-words-data-structure"),
        (212, "Word Search II", "Hard", "word-search-ii"),
    ],
    "heap-priority-queue": [
        (703, "Kth Largest Element in a Stream", "Easy", "kth-largest-element-in-a-stream"),
        (1046, "Last Stone Weight", "Easy", "last-stone-weight"),
        (973, "K Closest Points to Origin", "Medium", "k-closest-points-to-origin"),
        (215, "Kth Largest Element in an Array", "Medium", "kth-largest-element-in-an-array"),
        (621, "Task Scheduler", "Medium", "task-scheduler"),
        (355, "Design Twitter", "Medium", "design-twitter"),
        (295, "Find Median from Data Stream", "Hard", "find-median-from-data-stream"),
    ],
    "backtracking": [
        (78, "Subsets", "Medium", "subsets"),
        (39, "Combination Sum", "Medium", "combination-sum"),
        (40, "Combination Sum II", "Medium", "combination-sum-ii"),
        (46, "Permutations", "Medium", "permutations"),
        (90, "Subsets II", "Medium", "subsets-ii"),
        (22, "Generate Parentheses", "Medium", "generate-parentheses"),
        (79, "Word Search", "Medium", "word-search"),
        (131, "Palindrome Partitioning", "Medium", "palindrome-partitioning"),
        (17, "Letter Combinations of a Phone Number", "Medium", "letter-combinations-of-a-phone-number"),
        (51, "N-Queens", "Hard", "n-queens"),
    ],
    "graphs": [
        (200, "Number of Islands", "Medium", "number-of-islands"),
        (695, "Max Area of Island", "Medium", "max-area-of-island"),
        (133, "Clone Graph", "Medium", "clone-graph"),
        (286, "Walls and Gates", "Medium", "walls-and-gates"),
        (994, "Rotting Oranges", "Medium", "rotting-oranges"),
        (417, "Pacific Atlantic Water Flow", "Medium", "pacific-atlantic-water-flow"),
        (130, "Surrounded Regions", "Medium", "surrounded-regions"),
        (207, "Course Schedule", "Medium", "course-schedule"),
        (210, "Course Schedule II", "Medium", "course-schedule-ii"),
        (261, "Graph Valid Tree", "Medium", "graph-valid-tree"),
        (323, "Number of Connected Components in an Undirected Graph", "Medium", "number-of-connected-components-in-an-undirected-graph"),
        (684, "Redundant Connection", "Medium", "redundant-connection"),
        (127, "Word Ladder", "Hard", "word-ladder"),
    ],
    "advanced-graphs": [
        (743, "Network Delay Time", "Medium", "network-delay-time"),
        (332, "Reconstruct Itinerary", "Hard", "reconstruct-itinerary"),
        (1584, "Min Cost to Connect All Points", "Medium", "min-cost-to-connect-all-points"),
        (778, "Swim in Rising Water", "Hard", "swim-in-rising-water"),
        (269, "Alien Dictionary", "Hard", "alien-dictionary"),
        (787, "Cheapest Flights Within K Stops", "Medium", "cheapest-flights-within-k-stops"),
    ],
    "one-d-dp": [
        (70, "Climbing Stairs", "Easy", "climbing-stairs"),
        (746, "Min Cost Climbing Stairs", "Easy", "min-cost-climbing-stairs"),
        (198, "House Robber", "Medium", "house-robber"),
        (213, "House Robber II", "Medium", "house-robber-ii"),
        (5, "Longest Palindromic Substring", "Medium", "longest-palindromic-substring"),
        (647, "Palindromic Substrings", "Medium", "palindromic-substrings"),
        (91, "Decode Ways", "Medium", "decode-ways"),
        (322, "Coin Change", "Medium", "coin-change"),
        (152, "Maximum Product Subarray", "Medium", "maximum-product-subarray"),
        (139, "Word Break", "Medium", "word-break"),
        (300, "Longest Increasing Subsequence", "Medium", "longest-increasing-subsequence"),
        (416, "Partition Equal Subset Sum", "Medium", "partition-equal-subset-sum"),
    ],
    "two-d-dp": [
        (62, "Unique Paths", "Medium", "unique-paths"),
        (1143, "Longest Common Subsequence", "Medium", "longest-common-subsequence"),
        (309, "Best Time to Buy and Sell Stock with Cooldown", "Medium", "best-time-to-buy-and-sell-stock-with-cooldown"),
        (518, "Coin Change II", "Medium", "coin-change-ii"),
        (494, "Target Sum", "Medium", "target-sum"),
        (97, "Interleaving String", "Medium", "interleaving-string"),
        (329, "Longest Increasing Path in a Matrix", "Hard", "longest-increasing-path-in-a-matrix"),
        (115, "Distinct Subsequences", "Hard", "distinct-subsequences"),
        (72, "Edit Distance", "Medium", "edit-distance"),
        (312, "Burst Balloons", "Hard", "burst-balloons"),
        (10, "Regular Expression Matching", "Hard", "regular-expression-matching"),
    ],
    "greedy": [
        (53, "Maximum Subarray", "Medium", "maximum-subarray"),
        (55, "Jump Game", "Medium", "jump-game"),
        (45, "Jump Game II", "Medium", "jump-game-ii"),
        (134, "Gas Station", "Medium", "gas-station"),
        (846, "Hand of Straights", "Medium", "hand-of-straights"),
        (1899, "Merge Triplets to Form Target Triplet", "Medium", "merge-triplets-to-form-target-triplet"),
        (763, "Partition Labels", "Medium", "partition-labels"),
        (678, "Valid Parenthesis String", "Medium", "valid-parenthesis-string"),
    ],
    "intervals": [
        (57, "Insert Interval", "Medium", "insert-interval"),
        (56, "Merge Intervals", "Medium", "merge-intervals"),
        (435, "Non-overlapping Intervals", "Medium", "non-overlapping-intervals"),
        (252, "Meeting Rooms", "Easy", "meeting-rooms"),
        (253, "Meeting Rooms II", "Medium", "meeting-rooms-ii"),
        (1851, "Minimum Interval to Include Each Query", "Hard", "minimum-interval-to-include-each-query"),
    ],
    "math-geometry": [
        (48, "Rotate Image", "Medium", "rotate-image"),
        (54, "Spiral Matrix", "Medium", "spiral-matrix"),
        (73, "Set Matrix Zeroes", "Medium", "set-matrix-zeroes"),
        (202, "Happy Number", "Easy", "happy-number"),
        (66, "Plus One", "Easy", "plus-one"),
        (50, "Pow(x, n)", "Medium", "powx-n"),
        (43, "Multiply Strings", "Medium", "multiply-strings"),
        (2013, "Detect Squares", "Medium", "detect-squares"),
    ],
    "bit-manipulation": [
        (136, "Single Number", "Easy", "single-number"),
        (191, "Number of 1 Bits", "Easy", "number-of-1-bits"),
        (338, "Counting Bits", "Easy", "counting-bits"),
        (190, "Reverse Bits", "Easy", "reverse-bits"),
        (268, "Missing Number", "Easy", "missing-number"),
        (371, "Sum of Two Integers", "Medium", "sum-of-two-integers"),
        (7, "Reverse Integer", "Medium", "reverse-integer"),
    ],
}


def display_name(folder):
    """Return the human-readable name for a category folder."""
    for f, name in CATEGORY_ORDER:
        if f == folder:
            return name
    return folder


def problems():
    """Yield every problem as a dict, in README order.

    Keys: number, title, difficulty, slug, category (folder), filename.
    """
    for folder, _ in CATEGORY_ORDER:
        for number, title, difficulty, slug in _BY_CATEGORY[folder]:
            yield {
                "number": number,
                "title": title,
                "difficulty": difficulty,
                "slug": slug,
                "category": folder,
                "filename": "{:04d}-{}.py".format(number, slug),
            }


def problems_by_category():
    """Return an ordered list of (folder, display_name, [problem dicts])."""
    grouped = []
    for folder, name in CATEGORY_ORDER:
        items = [p for p in problems() if p["category"] == folder]
        grouped.append((folder, name, items))
    return grouped


if __name__ == "__main__":
    all_problems = list(problems())
    total = len(all_problems)
    print("NeetCode 150 canonical list: {} problems".format(total))
    for folder, name, items in problems_by_category():
        print("  {:<26} {}".format(name, len(items)))
    assert total == 150, "expected 150 problems, found {}".format(total)
    slugs = [p["slug"] for p in all_problems]
    assert len(set(slugs)) == total, "duplicate slug detected"
    numbers = [p["number"] for p in all_problems]
    assert len(set(numbers)) == total, "duplicate LeetCode number detected"
    print("OK: 150 unique problems, unique slugs and numbers.")
