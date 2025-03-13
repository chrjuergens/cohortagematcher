import argparse
import csv
import itertools
import math
import os
import matplotlib.pyplot as plt
import networkx as nx

def main():
    csv_file_path = "Zuordnung_math.csv"

    if os.path.exists(csv_file_path):
        print("csv exists ...")
    else:
        print(f"Could not find csv file: {csv_file_path}")
        print("Abort!")
        exit(0)

    sexes = ['m', 'w', 'all']

    potenzen = {
        1: 'linear',
        2: 'quadratisch',
        3: 'kubisch'
    }

    results_dir = "big_k_min"

    big_k = 1000

    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    for sex in sexes:
        print("########################################################")
        for pot_key, pot_val in potenzen.items():
            print("-------------------------------------------------------")
            
            print(f"Geschlecht: {sex}\n")
            print(f"Kantenpotenz (der Altersabstände): {pot_key}, also {pot_val}\n")
            
            patients = []
            controls = []
            
            # Extract patienten, kontrollen
            with open(csv_file_path, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                header = next(csv_reader)
    #                print(f"Header: {header}")

                for line in csv_reader:
                    if line[0].startswith("Kontrolle"):
                        controls.append(line[1:])
                    else:
                        patients.append(line[1:])
            
            # Filter gender
            if sex != 'all':
                patients = [pat for pat in patients if pat[1] == sex]
                controls = [kon for kon in controls if kon[1] == sex]

            print(f"Patienten, Anzahl: {len(patients)}")#\n{patienten}")
            print(f"Kontrollen, Anzahl: {len(controls)}")#\n{kontrolle}")

            edges = [(pat[2], kon[2], pow(abs(int(pat[0])-int(kon[0])), pot_key)) for pat, kon in itertools.product(patients, controls)]

            G = nx.Graph()

            G.add_weighted_edges_from(edges)

            #print(f"Nodes: {G.nodes}")
            #for u, v in G.edges:
            #    print(f"Edge {u} --> {v}: weight: {G.get_edge_data(u, v)}")
            #print(f"Inserted edges {len(edges)}:")


            edges_subset = nx.min_weight_matching(G)
            #print(f"Maximal weighted matching (#edges: {len(edges_subset)}):")
            #print(sorted(edges_subset))

            print(f"Edges with weights for maximal weighted matching:")
            gesamt_gewicht = 0.0
            result = "patient;kontrolle;altersabstand\n"
            for u, v in edges_subset:
                edge_weight = math.ceil((int(G.get_edge_data(u, v)['weight']))**(1/pot_key))
                gesamt_gewicht += edge_weight
                print(f"Edge {u} --> {v}: {edge_weight}")
                result += f"{u};{v};{edge_weight}\n"

            filename = sex + "_" + pot_val + "_" + str(int(gesamt_gewicht))
            with open(os.path.join(results_dir, filename), 'w') as outfile_wrt_sex:
                outfile_wrt_sex.write(result)              

            print(f"Gesamtgewicht: {gesamt_gewicht}")
            print(f"Anzahl Kanten: {len(edges_subset)}")
            R = nx.Graph()

            pat_nodes = [pat[2] for pat in patients]
            kon_nodes = [kon[2] for kon in controls]
            R.add_nodes_from(pat_nodes, bipartite=0)
            R.add_nodes_from(kon_nodes, bipartite=1)
            R.add_edges_from(edges_subset)

            l, r = nx.bipartite.sets(R, pat_nodes)

            option = 1
            pos = {}
            if option == 1:
                # OPTION 1: working
                pos.update((node, (1, 10*index)) for index, node in enumerate(l))
                pos.update((node, (2, 10*index)) for index, node in enumerate(r))

            if option == 2:
                # OPTION 2: not working
                pos = nx.layout.bipartite_layout(R, nodes=pat_nodes, aspect_ratio=0.5, scale=20.0)

            nx.draw(R, pos=pos, with_labels=True)
            plt.draw()
            plt.savefig("test")

            #layout = nx.layout.bipartite_layout(R, nodes=pat_nodes)

if __name__ == '__main__':
    parser = argparse.ArgumentParser

    parser.add_argument("file", type=str, help="path to csv file")

    args = parser.parse_args()


    
    main()