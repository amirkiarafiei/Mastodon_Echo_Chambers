import requests
import json
import os
from get_followers import get_followers_as_json

hashtags = [
    "ClimateChange",
    # "WomensRights"
]

counter = 0
for hashtag in hashtags:
    with open(f"hashtags/{hashtag}.json", "r") as json_file:
        roots = json.load(json_file)
    new_directory = f"roots/{hashtag}_roots"
    # Create new directory to store the roots for each hashtags along with the list of followings
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
        print(f"\nDirectory created at: {new_directory}")
    else:
        print(f"\nDirectory already exists at: {new_directory}")
    for root in roots:
        acc_id = root["account"]["id"]
        if os.path.exists(f"{new_directory}/{acc_id}_root_followers.json"):
            print(f"{acc_id} already exists. Skipping...")
        else:
            print(acc_id)
            with open(f"{new_directory}/{acc_id}_root_followers.json", 'w') as json_file:
                json.dump(get_followers_as_json(acc_id), json_file, indent=4)
                counter += 1
                if counter % 10 == 0:
                    print(counter)





