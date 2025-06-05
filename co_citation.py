import json
import itertools
import math

import networkx as nx
import os

hashtags = [
    # "GunControl",
    # "WomensRights",
    # "ClimateChange",
    # "BlackLivesMatter",
]

for hashtag in hashtags:
    common_reference = 0
    print(f"{hashtag} ==================================================================")
    graphs_directory = f"graphs/{hashtag}_root_graphs"

    gexf_files = [file for file in os.listdir(graphs_directory) if file.endswith('.gexf')]
    for gexf in gexf_files:
        graph = nx.read_gexf(f"{graphs_directory}/{gexf}")
        degree_centrality = nx.degree_centrality(graph)
        # betweenness_centrality = nx.betweenness_centrality(graph)

        # Find the top 5 nodes by degree centrality
        top_5_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        print("Top 5 nodes by degree centrality:")
        for node, centrality in top_5_degree:
            print(f"Node: {node}, Degree Centrality: {centrality}")

        # Find the top 5 nodes by betweenness centrality
        # top_5_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        # print("\nTop 5 nodes by betweenness centrality:")
        # for node, centrality in top_5_betweenness:
        #     print(f"Node: {node}, Degree Centrality: {centrality}")

        print(len(top_5_degree))
        for u_node, v_node in itertools.combinations([node for node, _ in top_5_degree], 2):
            with open(f"roots/{hashtag}_roots_followers/{u_node}_root_followers.json", "r") as json_file:
                u_followers = json.load(json_file)
                u_followers_ids = {follower["id"] for follower in u_followers}
            with open(f"roots/{hashtag}_roots_followers/{v_node}_root_followers.json", "r") as json_file:
                v_followers = json.load(json_file)
                v_followers_ids = {follower["id"] for follower in v_followers}
            mutual_followers = u_followers_ids.intersection(v_followers_ids)
            # Number of mutual followers (co-citation value)
            # print("\n-------------------------------------------------")
            # print(f"{u_node} and {v_node} \n {len(mutual_followers)}")
            co_citation = len(mutual_followers)
            normalized_co_citation = co_citation / math.sqrt(len(u_followers_ids)* len(v_followers_ids))
            print(f"normalized co-citation ({u_node}, {v_node}): {normalized_co_citation}")
            common_reference += normalized_co_citation
    print(f"\n######### Common Reference Metric = {common_reference}\n\n")

