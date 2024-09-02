# Detect echo chambers based on Clustering Coefficient and Average Jaccard Similarity values

import time
import networkx as nx
import os
import matplotlib.pyplot as plt

hashtags = [
    "ClimateChange",
    # "WomensRights"
]

def average_jaccard(graph):
    jaccard_coef = nx.jaccard_coefficient(graph)
    total_similarities = 0
    num_pairs = 0
    average_jaccard_similarity = 0
    for u, v, similarity in jaccard_coef:
        total_similarities += similarity
        num_pairs += 1
    if num_pairs > 0:
        average_jaccard_similarity = total_similarities / num_pairs
    return average_jaccard_similarity


for hashtag in hashtags:
    graphs_directory = f"graphs/{hashtag}_graphs"
    gexf_files = [file for file in os.listdir(graphs_directory) if file.endswith('.gexf')]
    for gexf in gexf_files:
        context_id = gexf.split(".gexf")[0]
        graph = nx.read_gexf(f"{graphs_directory}/{gexf}")
        print("====================================================", gexf)
        if nx.is_empty(graph):
            print("There is no connection between nodes in the graph.")
            continue
        nodes_pos = []
        nodes_neg = []
        # create list of pos and neg nodes based on sentiment score
        for node in graph.nodes():
            sentiment_compound = 0
            if "compound" in graph.nodes[node]:
                # There might be some nodes missing compound attribute due to sentiment analysis error
                sentiment_compound = graph.nodes[node]["compound"]
            # We assign the compound sentiment value as the final score
            if sentiment_compound > 0:
                nodes_pos.append(node)
            else:
                nodes_neg.append(node)
        # create subgraphs from pos and neg nodes
        subgraph_pos = graph.subgraph(nodes_pos)
        subgraph_neg = graph.subgraph(nodes_neg)
        num_of_echo_chambers = 0
        # ========================================= Results for positive subgraph
        if nx.number_of_nodes(subgraph_pos) != 0:
            # Clustering coefficient
            clustering_pos = nx.average_clustering(subgraph_pos)
            print("POS", subgraph_pos, "=>", clustering_pos)
            # Echo-chamber detected (in red) print statement
            if clustering_pos >= 0.3:
                print("\033[91m ECHO-CHAMBER DETECTED! \033[0m")
            # Jaccard similarity
            jaccard_pos = average_jaccard(subgraph_pos)
            print("Jaccard", jaccard_pos)
            # Echo-chamber detected (in yellow) print statement
            if jaccard_pos >= 0.5:
                print("\033[93m ECHO-CHAMBER DETECTED! \033[0m")
        else:
            print("POS Subgraph is Empty!")
        # ========================================= Results for negative subgraph
        if nx.number_of_nodes(subgraph_neg ) != 0:
            # Clustering coefficient
            clustering_neg = nx.average_clustering(subgraph_neg)
            print("NEG", subgraph_neg, "=>", clustering_neg)
            # Echo-chamber detected (in red) print statement
            if clustering_neg >= 0.3:
                print("\033[91m ECHO-CHAMBER DETECTED! \033[0m")
            # Jaccard similarity
            jaccard_neg = average_jaccard(subgraph_neg)
            print("Jaccard", jaccard_neg)
            # Echo-chamber detected (in yellow) print statement
            if jaccard_neg >= 0.5:
                print("\033[93m ECHO-CHAMBER DETECTED! \033[0m")
        else:
            print("NEG Subgraph is Empty!")

        # Visualize subgraphs and save them
        fig, (ax1, ax2) = plt.subplots(1, 2)
        nx.draw_networkx(subgraph_pos, ax=ax1, node_color='green', with_labels=True)
        nx.draw_networkx(subgraph_neg, ax=ax2, node_color='red', with_labels=True)
        plt.suptitle(f"Context: {context_id}")
        plt.savefig(f"images/{hashtag}_images/{context_id}_sentiment.png")
        # plt.show()
        # Close the figure to free up resources
        plt.close(fig)



