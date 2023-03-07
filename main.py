import utils
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def main():
    n, m = 2, 3
    
    for _ in range(1000):
        D, Q = utils.random_game(n, m)
        #D = np.array([0.5, 0.3, 0.2])
        #Q = np.array([[0.1, 0.4, 0.8], [0.9, 0.4, 0.2]])
        G_better, G_worse = utils.generate_graph(n, m, D, Q)

        pnes = utils.find_pnes(G_better)
        best_u, best_pne = max([(utils.nsw([utils.action_targeted_utility(D, Q, p, pne[p], pne) for p in range(n)]), pne) for pne in pnes])

        # print("Best utility: {} with startegies profile: {}".format(best_u, best_pne))
        
        all_pairs_shortest_path = dict(nx.all_pairs_shortest_path(G_better))

        # all possible start positions: profiles minus the pnes
        start_positions = [p for p in G_better.nodes() if p not in pnes]

        # all possible end positions: pnes minus the best_pne
        end_positions = [p for p in pnes if p != best_pne]

        # if there is a path from one of the start positions to one of the end positions
        # save the game to a file
        '''for start in start_positions:
            for end in end_positions:
                if end in all_pairs_shortest_path[start]:
                    path = all_pairs_shortest_path[start][end]
                    print("Path from {} to {} is {}".format(start, end, path))
                    utils.save_game_to_file(n, m, D, Q, start, end, path, "game.txt")'''

        # is there a path from a start position to the best_pne?
        for start in start_positions:
            if best_pne not in all_pairs_shortest_path[start]:
                print("No path from {} to the best PNE {}".format(start, best_pne))
                
                # print the game
                print("n = {}".format(n))
                print("m = {}".format(m))
                print("D = {}".format(D))
                print("Q = {}".format(Q))

                return

if __name__ == "__main__":
    main()
