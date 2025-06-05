import networkx as nx
import os
import matplotlib.pyplot as plt

hashtags = [
    "GunControl",
    # "ClimateAction"
]


for hashtag in hashtags:
    graphs_directory = f"graphs/{hashtag}_graphs"
    gexf_files = [file for file in os.listdir(graphs_directory) if file.endswith('.gexf')]
    for gexf in gexf_files:
        graph = nx.read_gexf(f"{graphs_directory}/{gexf}")
        if nx.is_empty(graph):
            continue
        nodes_pos = []
        nodes_neg = []
        # create list of pos and neg nodes
        for node in graph.nodes():
            sentiment_pos = graph.nodes[node]["positive"]
            sentiment_neg = graph.nodes[node]["negative"]
            # We assign the largest absolute value of pos and neg sentiments to final sentiment score of the node
            if abs(sentiment_pos) > abs(sentiment_neg):
                sentiment_score = sentiment_pos
                nodes_pos.append(node)
            else:
                sentiment_score = sentiment_neg
                nodes_neg.append(node)
            # print(node, sentiment_score)
        # create subgraphs of pos and neg nodes
        subgraph_pos = graph.subgraph(nodes_pos)
        subgraph_neg = graph.subgraph(nodes_neg)
        print("========================", gexf)
        if not nx.number_of_nodes(subgraph_pos) == 0:
            print("POS", subgraph_pos, "=>", nx.average_clustering(subgraph_pos))
        else:
            print("POS Subgraph is Empty!")
        if not nx.number_of_nodes(subgraph_neg ) == 0:
            print("NEG", subgraph_neg, "=>", nx.average_clustering(subgraph_neg))
        else:
            print("NEG Subgraph is Empty!")
        fig, (ax1, ax2) = plt.subplots(1, 2)
        nx.draw_networkx(subgraph_pos, ax=ax1, node_color='green', with_labels=True)
        nx.draw_networkx(subgraph_neg, ax=ax2, node_color='red', with_labels=True)
        plt.show()



