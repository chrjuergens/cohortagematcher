import argparse
import csv
import itertools
import math
import os
import matplotlib.pyplot as plt
import networkx as nx

def main(path_to_csv_file: str):

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
            
            U_patients, V_controls, header = extract_sets_UV_from_csv(csv_file_path=path_to_csv_file, has_header=True, U_name="Kontrolle")
            
            # Filter gender
            if sex != 'all':
                U_patients = filter_by_sex(sex, U_patients)
                V_controls = filter_by_sex(sex, V_controls)

            print(f"Patienten, Anzahl: {len(U_patients)}")#\n{patienten}")
            print(f"Kontrollen, Anzahl: {len(V_controls)}")#\n{kontrolle}")

            edges = create_edges_from_UV(pot_key, U_patients, V_controls)

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

            pat_nodes = [pat[2] for pat in U_patients]
            kon_nodes = [kon[2] for kon in V_controls]
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

def create_edges_from_UV(pot_key, patients, controls):
    return [(pat[2], kon[2], pow(age_difference(pat[0], kon[0]), pot_key)) for pat, kon in itertools.product(patients, controls)]

def age_difference(pat, kon):
    return abs(int(pat)-int(kon))

def filter_by_sex(sex, patients):
    return [pat for pat in patients if pat[1] == sex]

def extract_sets_UV_from_csv(csv_file_path: str, U_name: str = None, V_name: str = None, has_header: bool = True) -> tuple[list, list, list]:
    """Method to extract U and V from a csv where each row corresponds to U or V.

    The csv must be structured as follows:
    - Each row corresponds to U or V
    - The decision is made on basis of the first element
    - You must name U_name which is the filter for U
    - You don't have to name V_name but if you do then only U_name and V_name are filtered
    """
    if U_name is None and V_name is None:
        raise ValueError("You must specify U_name or V_name")
    U = []
    V = []
    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        if has_header:
            header = next(csv_reader)
        for line in csv_reader:
            if U_name is not None:
                if line[0].startswith(U_name):
                    U.append(line[1:])
                else:
                    V.append(line[1:])
            elif V_name is not None:
                if line[0].startswith(V_name):
                    V.append(line[1:])
                else:
                    U.append(line[1:])
        if has_header:
            return U, V, header
        else:
            return U, V, []


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="path to csv file")
    parser.add_argument("-U", "--U-name", type=str, help="Name of U elements")
    parser.add_argument("-V", "--V-name", type=str, help="Name of V elements")
    args = parser.parse_args()

    csv_file_path = args.file

    if os.path.exists(csv_file_path):
        print("csv exists ...")
    else:
        print(f"Could not find csv file: {csv_file_path}")
        print("Abort!")
        exit(0)
    
    main(path_to_csv_file=args.file)