import requests
import json
import os
from get_followings import get_followings_as_json

hashtags = [
    "ClimateChange",
    # "WomensRights"
]

def parse_filename(filename):
    return filename.split(".")[0]


for hashtag in hashtags:
    directory = f"contexts/{hashtag}_context"
    all_files = [file for file in os.listdir(directory) if file.endswith('.json')]
    for file in all_files[144:]:
        with open(os.path.join(directory, file), 'r') as json_file:
                root_context = json.load(json_file)
        print(f"\n---{file}")
        list_of_replier_ids = [replier["account"]["id"] for replier in root_context["descendants"]]
        # print(list_of_replier_ids)
        filename = parse_filename(file)
        new_directory = f"contexts/{hashtag}_context/{filename}_repliers"
        # Create new directory to store the list of followings of repliers under each a root (context)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
            print(f"Directory created at: {new_directory}")
        else:
            print(f"Directory already exists at: {new_directory}")
        for id in list_of_replier_ids:
            with open(f"{new_directory}/{id}_replier_followings.json", 'w') as json_file:
                json.dump(get_followings_as_json(id), json_file, indent=4)
                print(f"Followings of {id} retrieved.")