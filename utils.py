import numpy as np
import networkx as nx

# Constants ################################
MAX_QUALITY = 10
MIN_QUALITY = 0
############################################


def random_game(n, m):
    D = np.random.rand(m)
    D = D / np.sum(D)

    Q = np.random.rand(n, m) * MAX_QUALITY + MIN_QUALITY
    return D, Q


def nsw(u):
    return np.prod(u)


def sw(u):
    return np.sum(u)


def exposure_trageted_utility(D, Q, j, k, a):
    """
    a :: tuple of the form (i, j)
    j :: player index
    k :: topic index
    """

    assert k == a[j]

    B_k_a = max([Q[i, a[i]] for i in range(len(a))])
    H_k_a = len([i for i in range(len(a)) if Q[i, a[i]] == B_k_a])
    if Q[j, a[j]] == B_k_a:
        return D[k] / H_k_a
    else:
        return 0


def action_targeted_utility(D, Q, j, k, a):
    assert k == a[j]
    return exposure_trageted_utility(D, Q, j, k, a) * Q[a[0], a[1]]


def generate_graph(n, m, D, Q):
    """
    The graph is a directed graph with node representing a strategy profile
    and an edge representing a transition from one strategy profile to another.

    The nodes are labeled with a tuple of the form (i, j)
    where i is the topic of the first player and j is the topic of the second player.

    Topics are from range [0, m-1].

    Edges represent a deviation of a single player from their current strategy, to any other strategy.
    In addition, edges are directed from a worst utility to a better utility.
    """
    G_better = nx.DiGraph()
    G_worse = nx.DiGraph()
    for i in range(m):
        for j in range(m):
            G_better.add_node((i, j))
            G_worse.add_node((i, j))

    # player 0 deviates
    for i in range(m):
        for j in range(m):
            for k in range(m):
                if k == i:
                    # no deviation
                    continue
                elif exposure_trageted_utility(
                    D, Q, 0, k, (k, j)
                ) > exposure_trageted_utility(D, Q, 0, i, (i, j)):
                    G_better.add_edge((i, j), (k, j))
                    G_worse.add_edge((k, j), (i, j))

    # player 1 deviates
    for i in range(m):
        for j in range(m):
            for k in range(m):
                if k == j:
                    # no deviation
                    continue
                elif exposure_trageted_utility(
                    D, Q, 1, k, (i, k)
                ) > exposure_trageted_utility(D, Q, 1, j, (i, j)):
                    G_better.add_edge((i, j), (i, k))
                    G_worse.add_edge((i, k), (i, j))

    return G_better, G_worse


def find_pnes(G_better):
    """
    Calculate the PNEs of a game.
    """
    PNEs = []
    for node in G_better.nodes():
        if G_better.out_degree(node) == 0:
            PNEs.append(node)
    return PNEs


def save_game_to_file(n, m, D, Q, start, end, path, filename):
    """
    Save the game to a file.
    """
    with open(filename, "w") as f:
        f.write("{} {} {}\n".format(n, m, len(path)))
        f.write(" ".join([str(x) for x in D]) + "\n")
        for i in range(n):
            f.write(" ".join([str(x) for x in Q[i]]) + "\n")
        f.write(" ".join([str(x) for x in start]) + "\n")
        f.write(" ".join([str(x) for x in end]) + "\n")
        for i in range(len(path)):
            f.write(" ".join([str(x) for x in path[i]]) + "\n")


def read_game_from_file(filename):
    """
    Read the game from a file.
    """
    with open(filename, "r") as f:
        n, m, path_length = [int(x) for x in f.readline().split()]
        D = np.array([float(x) for x in f.readline().split()])
        Q = np.zeros((n, m))
        for i in range(n):
            Q[i] = np.array([float(x) for x in f.readline().split()])
        start = np.array([int(x) for x in f.readline().split()])
        end = np.array([int(x) for x in f.readline().split()])
        path = []
        for i in range(path_length):
            path.append(np.array([int(x) for x in f.readline().split()]))
        return n, m, D, Q, start, end, path


def main():
    # read the game from a file
    n, m, D, Q, start, end, path = read_game_from_file("game.txt")

    # print the game
    print("n = {}".format(n))
    print("m = {}".format(m))
    print("D = {}".format(D))
    print("Q = {}".format(Q))
    print("start = {}".format(start))
    print("end = {}".format(end))
    print("path = {}".format(path))


if __name__ == "__main__":
    main()
