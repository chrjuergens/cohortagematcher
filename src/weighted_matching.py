"""Module for cohort age matching"""
import argparse
import csv
import itertools
import math
import os
import sys
# import matplotlib.pyplot as plt
import networkx as nx


def main(csv_path: str, results_dir: str):
    """Computes chort age matching"""
    SEXES = ['m', 'w', 'all']
    POTENZEN = {
        1: 'linear',
        2: 'quadratisch',
        3: 'kubisch'
    }

    for sex in SEXES:
        print("########################################################")
        for pot_key, pot_val in POTENZEN.items():
            print("-------------------------------------------------------")
            print(f"Geschlecht: {sex}\n")
            print(
                f"Kantenpotenz (der Altersabstände): {pot_key}, also {pot_val}\n")
            u_patients, v_controls, header = extract_sets_uv_from_csv(path_to_csv_file=csv_path,
                                                                      has_header=True,
                                                                      u_name="Kontrolle")
            # Filter gender
            if sex != 'all':
                u_patients = filter_by_sex(sex, u_patients)
                v_controls = filter_by_sex(sex, v_controls)
            print(f"Patienten, Anzahl: {len(u_patients)}")  # \n{patienten}")
            print(f"Kontrollen, Anzahl: {len(v_controls)}")  # \n{kontrolle}")
            edges = create_edges_from_uv(
                u_patients, v_controls, pot_key=pot_key)
            g, edges_subset = compute_age_matching(edges)
            # print(f"Maximal weighted matching (#edges: {len(edges_subset)}):")
            # print(sorted(edges_subset))
            gesamt_gewicht, result = create_result_representation(g,
                                                                  edges_subset,
                                                                  pot_key,
                                                                  header=header,
                                                                  do_print=True)
            filename = sex + "_" + pot_val + "_" + str(int(gesamt_gewicht))
            with open(os.path.join(results_dir, filename), 'w', encoding='utf8') as outfile_wrt_sex:
                outfile_wrt_sex.write(result)
            print(f"Gesamtgewicht: {gesamt_gewicht}")
            print(f"Anzahl Kanten: {len(edges_subset)}")

            # g = nx.Graph()
            # pat_nodes = [pat[2] for pat in u_patients]
            # kon_nodes = [kon[2] for kon in v_controls]
            # g.add_nodes_from(pat_nodes, bipartite=0)
            # g.add_nodes_from(kon_nodes, bipartite=1)
            # g.add_edges_from(edges_subset)

            # u, v = nx.bipartite.sets(g, pat_nodes)

            # option = 1
            # pos = {}
            # if option == 1:
            #     # OPTION 1: working
            #     pos.update((node, (1, 10*index)) for index, node in enumerate(u))
            #     pos.update((node, (2, 10*index)) for index, node in enumerate(v))

            # if option == 2:
            #     # OPTION 2: not working
            #     pos = nx.layout.bipartite_layout(v, nodes=pat_nodes, aspect_ratio=0.5, scale=20.0)

            # nx.draw(g, pos=pos, with_labels=True)
            # plt.draw()
            # plt.savefig("test")


def create_result_representation(g, edges_subset, pot_key, header, do_print: bool = False):
    """Creates result representation string containing the age-matched cohort"""
    if do_print:
        print("Edges with weights for maximal weighted matching:")
        print("Edges with weights for maximal weighted matching:")
    gesamt_gewicht = 0.0
    if header is not None:
        result = ",".join(header)
    else:
        result = "patient;kontrolle;altersabstand\n"
    for u, v in edges_subset:
        edge_weight = math.ceil(
            (int(g.get_edge_data(u, v)['weight']))**(1/pot_key))
        gesamt_gewicht += edge_weight
        if do_print:
            print(f"Edge {u} --> {v}: {edge_weight}")
            print(f"Edge {u} --> {v}: {edge_weight}")
        result += f"{u};{v};{edge_weight}\n"
    return gesamt_gewicht, result


def compute_age_matching(edges):
    """Creates graph and computes min_weight_matching"""
    g = nx.Graph()
    g.add_weighted_edges_from(edges)
    # print(f"Nodes: {G.nodes}")
    # for u, v in G.edges:
    #    print(f"Edge {u} --> {v}: weight: {G.get_edge_data(u, v)}")
    # print(f"Inserted edges {len(edges)}:")
    edges_subset = nx.min_weight_matching(g)
    return g, edges_subset


def create_edges_from_uv(patients, controls,
                         pot_key: int = 1, age_pos: int = 0):
    """Create weighted edge set where e x w = (u, v) x w_uv for all u in U, v in V"""
    return [(pat[2], kon[2], pow(age_difference(
        pat[age_pos],
        kon[age_pos]),
        pot_key))
        for pat, kon in itertools.product(patients, controls)]


def age_difference(pat, kon):
    """Compute age difference"""
    return abs(int(pat)-int(kon))


def filter_by_sex(sex, patients, pos_sex: int = 1):
    """Filter list by sex"""
    return [pat for pat in patients if pat[pos_sex] == sex]


def extract_sets_uv_from_csv(path_to_csv_file: str, u_name: str = None, v_name: str = None,
                             has_header: bool = True) -> tuple[list, list, list]:
    """Method to extract U and V from a csv where each row corresponds to U or V.

    The csv must be structured as follows:
    - Each row corresponds to U or V
    - The decision is made on basis of the first element
    - You must name U_name which is the filter for U
    - You don't have to name V_name but if you do then only U_name and V_name are filtered
    """
    if u_name is None and v_name is None:
        raise ValueError("You must specify U_name or V_name")
    u = []
    v = []
    with open(path_to_csv_file, "r", encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        if has_header:
            header = next(csv_reader)
        for line in csv_reader:
            if u_name is not None:
                if line[0].startswith(u_name):
                    u.append(line[1:])
                else:
                    v.append(line[1:])
            elif v_name is not None:
                if line[0].startswith(v_name):
                    v.append(line[1:])
                else:
                    u.append(line[1:])
        if has_header:
            return u, v, header
        return u, v, []


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="path to csv file")
    parser.add_argument("-U", "--U-name", type=str, help="Name of U elements")
    parser.add_argument("-V", "--V-name", type=str, help="Name of V elements")
    parser.add_argument("-r", "--results-dir", type=str, help="Directory for results")
    args = parser.parse_args()

    csv_file_path = args.file

    if os.path.exists(csv_file_path):
        print("csv exists ...")
    else:
        print(f"Could not find csv file: {csv_file_path}")
        print("Abort!")
        sys.exit(0)
    results_dir = "big_k_min"
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)
    main(csv_path=args.file, results_dir=results_dir)
