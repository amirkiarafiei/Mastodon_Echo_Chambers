import os
import networkx as nx
import matplotlib.pyplot as plt

hashtags = [
    "ClimateChange",
    # "WomensRights"
]

hashtag = hashtags[0]
saveGraphs = True
graphs_directory = f"graphs/{hashtag}_graphs"
gexf_files = [file for file in os.listdir(graphs_directory) if file.endswith('.gexf')]

# =================================== Visualize with replier_id labels
counter = 0
for gexf in gexf_files:
    graph = nx.read_gexf(f"{graphs_directory}/{gexf}")
    nx.draw(graph, with_labels=True)
    if saveGraphs:
        context_id = gexf.split(".gexf")[0]
        plt.suptitle(f"Context: {context_id}")
        plt.savefig(f"images/{hashtag}_images/{context_id}.png")
    # plt.show()
    plt.close()
    counter += 1
    print(counter)

# ==================================== Visualize with attrbiutes
# for gexf in gexf_files:
#     graph = nx.read_gexf(f"{graphs_directory}/{gexf}")
#     pos = nx.spring_layout(graph)  # get the node positions
#     nx.draw_networkx(graph, pos, with_labels=False)  # draw the graph without labels
#     labels = {node: f"{graph.nodes[node]['positive']}\n{graph.nodes[node]['negative']}" for node in graph.nodes()}
#     nx.draw_networkx_labels(graph, pos, labels=labels)  # draw the labels with attribute values
#     if saveGraphs:
#         context_id = gexf.split(".gexf")[0]
#         plt.savefig(f"images/{hashtag}_images/{context_id}.png")
#     plt.show()
