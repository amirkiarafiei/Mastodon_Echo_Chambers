import json
import networkx as nx
import os
from bs4 import BeautifulSoup


hashtags = [
    "ClimateChange",
    # "WomensRights"
]

for hashtag in hashtags:
    os.makedirs(f"texts/{hashtag}_texts", exist_ok=True)
    graphs_directory = f"graphs/{hashtag}_graphs"
    gexf_files = [file for file in os.listdir(graphs_directory) if file.endswith('.gexf')]
    # the loop to load data of each graph (each gexf)
    for gexf in gexf_files:
        context_id = gexf.split(".gexf")[0]
        graph = nx.read_gexf(f"{graphs_directory}/{gexf}")
        os.makedirs(f"texts/{hashtag}_texts/{context_id}_context", exist_ok=True)
        print("\n=============================================================== context", context_id )
        print("number of repliers with mutual followings", len(graph.nodes))
        # loop for finding the reply text of each node (replier) in the graph
        for node in graph.nodes():
            replier_id = node
            print("-----------------------------------------------------------")
            print("replier ID:", replier_id)
            # first line is for header (we add replier_id as header)
            replier_text = f"{replier_id}"
            html_content = ""
            with open(f"contexts/{hashtag}_context/{context_id}_context.json") as json_file:
                context = json.load(json_file)
            for status in context["descendants"]:
                # first we find the status dict of the replier under that context
                if status["account"]["id"] == replier_id:
                    # then we append the repliers text which is in HTML format
                    html_content += status["content"]
            # now we want to extract the content of <p> which is the text of reply
            soup = BeautifulSoup(html_content, 'html.parser')
            # Find all <p> tags
            replies = soup.find_all('p')
            for reply in replies:
                text = reply.get_text()
                replier_text += f"\n{text}"
            # Each reply of a replier (node) should appear in one line (reply 1 in line 1, reply 2 in line 2 and ...)
            replier_text = replier_text.replace('\u2029', ' ')
            print(replier_text)
            with open(f"texts/{hashtag}_texts/{context_id}_context/{replier_id}.txt", "w", encoding="utf-8") as txt_file:
                txt_file.write(replier_text)




