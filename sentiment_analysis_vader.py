import json
import networkx as nx
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

hashtags = [
    "ClimateChange",
    # "WomensRights"
]

analyzer = SentimentIntensityAnalyzer()
for hashtag in hashtags:
    graphs_directory = f"graphs/{hashtag}_graphs"
    gexf_files = [file for file in os.listdir(graphs_directory) if file.endswith('.gexf')]
    # the loop to load data of each graph (each gexf)
    for gexf in gexf_files:
        context_id = gexf.split(".gexf")[0]
        graph = nx.read_gexf(f"{graphs_directory}/{gexf}")
        print(f"\n=============================== context {context_id}")
        if nx.is_empty(graph):
            print("There is no connection between nodes in the graph.")
            continue
        # loop to iterate each node in the graph
        for node in graph.nodes():
            replier_id = node
            replier_text = ""
            with open(f"texts/{hashtag}_texts/{context_id}_context/{replier_id}.txt", "r", encoding="utf8") as text_file:
                lines = text_file.readlines()
                negative_sentiment = 0
                positive_sentiment = 0
                compound_sentiment = 0
                num_of_replies = 0
                # double-check if the node id and account_id are same (first line of txt file is account_id)
                print("------------------id:", replier_id, replier_id == lines[0].strip())
                # cumulative sum of replies of a node
                # we start from second line since the first line is header
                for line in lines[1:]:
                    # ===================================
                    sentiment_scores = analyzer.polarity_scores(line.strip())
                    negative_sentiment += sentiment_scores["neg"]
                    positive_sentiment += sentiment_scores["pos"]
                    compound_sentiment += sentiment_scores["compound"]
                    # ===================================
                    num_of_replies += 1
                # We normalize the sentiment values by calculating Mean, in case a replier has several replies under a context
                if num_of_replies != 0:
                    print("number of replies:", num_of_replies)
                    print(f"pos={round(positive_sentiment/num_of_replies, 3)}",
                          f"neg={round(negative_sentiment/num_of_replies, 3)}",
                          f"compound={round(compound_sentiment/num_of_replies, 3)}")
                    # Update the graphs with sentiment scores
                    graph.nodes[replier_id]["pos"] = round(positive_sentiment / num_of_replies, 3)
                    graph.nodes[replier_id]["neg"] = round(negative_sentiment / num_of_replies, 3)
                    graph.nodes[replier_id]["compound"] = round(compound_sentiment / num_of_replies, 3)

        # Write the updated graphs
        nx.write_gexf(graph, f"{graphs_directory}/{gexf}")

