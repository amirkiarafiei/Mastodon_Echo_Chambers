import json
import os
import networkx as nx
import matplotlib.pyplot as plt

hashtags = [
    # "UKElections"
    # "RussianElections",
    # "GunControl"
    # "ClimateAction"
    # "EUElections2024", "EUElections"
    # "BlackLivesMatter"
    # "ClimateChange"
    "WomensRights"
]

# Create a graph which the nodes are the repliers under a root status, and the edges indicate
# that those nodes (repliers) follow each other

for hashtag in hashtags:
    print(f"\n================= {hashtag} ===============")
    directory = f"contexts/{hashtag}_context"
    # List all json files in the {hashtags}_context
    contexts = [file for file in os.listdir(directory) if file.endswith('_context.json')]
    # Loop to iterate the contexts under each hashtag ({hashtags}_context)
    counter = 0
    for context in contexts:
        # counter += 1
        # if counter == 5:
        #     break
        context_graph = nx.Graph()
        # First get the id of the context from file name
        context_id = context.split('_context.json')[0]
        print(f"\n---------context of {context_id}---------")
        # Now we want to iterate the repliers under a context
        path = f"contexts/{hashtag}_context/{context_id}_context_repliers"
        # Get the list of all json files (or repliers) under a context
        repliers = [file for file in os.listdir(path) if file.endswith('_replier_followings.json')]
        # print(f"List of repliers: {repliers}")
        print(f"Number of repliers: {len(repliers)}")
        # Loop to iterate the repliers under a context (using pairwise comparison)
        for u in range(len(repliers) - 1):
            for v in range(u + 1, len(repliers)):
                u_id = repliers[u].split('_replier_followings.json')[0]
                v_id = repliers[v].split('_replier_followings.json')[0]
                with open(f"{path}/{repliers[u]}", 'r') as json_file:
                    u_followings = json.load(json_file)
                with open(f"{path}/{repliers[v]}", 'r') as json_file:
                    v_followings = json.load(json_file)
                # Sometimes the repliers list is empty due to network errors, so we check for empty files
                if (len(u_followings) > 0) and (len(v_followings) > 0):
                    u_isFollowing_v = any(following["id"] == v_id for following in u_followings)
                    v_isFollowing_u = any(following["id"] == u_id for following in v_followings)
                    if u_isFollowing_v and v_isFollowing_u:
                        print(f"{u_id} and {v_id} follow each other")
                        context_graph.add_edge(u_id, v_id, relation="following")
                else:
                #     print(f"{u_id} and {v_id} do not follow each other")
                # if you want to add all nodes, uncomment this:
                #     context_graph.add_node(u_id)
                #     context_graph.add_node(v_id)
                    pass

        # save graph as png
        os.makedirs(f"images/{hashtag}_images", exist_ok=True)
        nx.draw(context_graph, with_labels=True)
        plt.suptitle(f"Context: {context_id}")
        plt.savefig(f"images/{hashtag}_images/{context_id}.png")
        # plt.show() #.show() function resets the plt object
        plt.close()
        # serialize graph as gexf file
        os.makedirs(f"graphs/{hashtag}_graphs", exist_ok=True)
        nx.write_gexf(context_graph, f'graphs/{hashtag}_graphs/{context_id}.gexf')
