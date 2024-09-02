import json
import os
import networkx as nx
import matplotlib.pyplot as plt

hashtags = [
    "ClimateChange",
    # "WomensRights"
]

for hashtag in hashtags:
    print(f"\n================= {hashtag} ===============")
    hashtag_graph = nx.Graph()
    directory = f"roots/{hashtag}_roots"
    roots = [file for file in os.listdir(directory) if file.endswith('_root_followings.json')]
    # print("List of roots", roots)
    counter = 0
    for u in range(len(roots) - 1):
        for v in range(u + 1, len(roots)):
            u_id = roots[u].split('_root_followings.json')[0]
            v_id = roots[v].split('_root_followings.json')[0]
            with open(f"{directory}/{u_id}_root_followings.json", 'r') as json_file:
                u_followings = json.load(json_file)
            with open(f"{directory}/{v_id}_root_followings.json", 'r') as json_file:
                v_followings = json.load(json_file)
            u_isFollowing_v = any(following["id"] == v_id for following in u_followings)
            v_isFollowing_u = any(following["id"] == u_id for following in v_followings)
            if u_isFollowing_v and v_isFollowing_u:
                print(f"{u_id} and {v_id} follow each other")
                hashtag_graph.add_edge(u_id, v_id, relation="following")
            else:
                # print(f"{u_id} and {v_id} do not follow each other")
                pass
            counter += 1
            if counter % 50 == 0:
                print(u, v)

    # save graph as png
    os.makedirs(f"images/{hashtag}_root_images", exist_ok=True)
    nx.draw(hashtag_graph, with_labels=True)
    plt.savefig(f"images/{hashtag}_root_images/{hashtag}.png")
    plt.show() #.show() function resets the plt object
    plt.close()
    # serialize graph as gexf file
    os.makedirs(f"graphs/{hashtag}_root_graphs", exist_ok=True)
    nx.write_gexf(hashtag_graph, f'graphs/{hashtag}_root_graphs/{hashtag}.gexf')

