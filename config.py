"""
MindMesh AI - Configuration & Constants
"""

APP_NAME = "MindMesh AI"
APP_SUBTITLE = "Your Personal Open-Source AI Study Assistant"
APP_VERSION = "1.0.0"
APP_ICON = "🧠"

# AI Inference Defaults
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_GEMMA_MODEL = "gemma:2b"
AVAILABLE_MODELS = [
    "gemma:2b",
    "gemma2:2b",
    "gemma:7b",
    "gemma2:9b",
    "gemma2:27b"
]

# Demo Sample Study Material for Hackathon Presentation
SAMPLE_OS_NOTES = """Operating Systems Revision Notes
An operating system (OS) is essential system software that manages computer hardware and software resources, acting as an intermediary between the computer user and the hardware.

Core Subsystems and Responsibilities:
1. Process Management:
A process is a program in execution. The OS allocates CPU time using scheduling algorithms (FCFS, Round Robin, Shortest Job First, Multi-Level Feedback Queues). Process states include New, Ready, Running, Waiting, and Terminated. Inter-Process Communication (IPC) is achieved via Shared Memory and Message Passing.

2. Synchronization & Deadlocks:
When multiple processes access shared resources concurrently, race conditions occur. Critical section problems are solved using Semaphores, Mutexes, and Monitors.
Deadlock occurs when two or more processes are blocked indefinitely, each holding a resource while waiting for a resource held by another process.
The four Coffman conditions necessary for deadlock are:
- Mutual Exclusion: Only one process can use a resource at a time.
- Hold and Wait: A process holds at least one resource and is waiting to acquire additional resources.
- No Preemption: Resources cannot be forcibly taken from a process.
- Circular Wait: A closed chain of processes exists where each waits for a resource held by the next.
Deadlock handling strategies: Prevention (negating one condition), Avoidance (Banker's Algorithm), Detection & Recovery (process termination, resource preemption), and Ignorance (Ostrich Algorithm).

3. Memory Management & Virtual Memory:
Physical memory (RAM) is divided into frames, while logical memory is divided into pages (Paging). A Page Table translates logical addresses to physical addresses.
When a requested page is not in RAM, a Page Fault occurs, triggering the OS to fetch the page from secondary storage.
Virtual Memory enables the execution of processes larger than physical RAM using Demand Paging. Page replacement algorithms include FIFO, Optimal (OPT), and Least Recently Used (LRU).
Thrashing happens when the OS spends more time swapping pages in and out than executing instructions.

4. Storage & File Systems:
Files are organized logically into hierarchical directories. Disk scheduling algorithms (SSTF, SCAN, C-SCAN) optimize disk arm movements.
Security and protection mechanisms enforce access control lists (ACLs) and cryptographic authorization."""

SAMPLE_DSA_NOTES = """Data Structures & Algorithms - Revision Notes
Data structures organize and store data for efficient access and modification.

1. Binary Search Trees (BST):
A binary tree where the left subtree contains nodes with keys less than the parent node, and the right subtree contains nodes with keys greater than the parent node.
- Operations: Search O(h), Insert O(h), Delete O(h), where h is the tree height.
- Traversal types: In-order (yields sorted elements), Pre-order, Post-order, and Level-order (BFS).
- Balanced Trees: In the worst-case (skewed tree), operations degrade to O(n). Self-balancing trees like AVL Trees and Red-Black Trees maintain h = O(log n) through tree rotations.

2. Graph Theory:
Graphs consist of vertices (V) and edges (E), directed or undirected.
- Representations: Adjacency Matrix O(V^2 space) and Adjacency List O(V + E space).
- Search: Breadth-First Search (BFS) using a Queue finds shortest paths in unweighted graphs; Depth-First Search (DFS) using recursion/Stack is used for cycle detection and topological sorting.
- Minimum Spanning Trees (MST): Kruskal's Algorithm (Greedy, Disjoint Set Union) and Prim's Algorithm (Priority Queue).

3. Algorithm Complexities & Big-O:
- O(1): Constant time (Hash map lookup)
- O(log n): Logarithmic (Binary search)
- O(n): Linear (Linear search)
- O(n log n): Linearithmic (MergeSort, QuickSort average)
- O(n^2): Quadratic (Bubble, Selection, Insertion Sort)
- O(2^n): Exponential (Recursive Fibonacci)"""
