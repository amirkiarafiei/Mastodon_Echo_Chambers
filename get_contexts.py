import json
import requests
import os
import time

# ========================================== Get the context of all root Statuses for a hashtag
hashtags = [
            "ClimateChange",
            # "WomensRights"
            ]

min_replies = 2
# Open the JSON file of each hashtag, then loop over the IDs of each status, and then get the context of that ID
for hashtag in hashtags:
    with open(f"hashtags/{hashtag}.json", 'r') as json_file:
        statuses = json.load(json_file)
    new_directory = f"contexts/{hashtag}_context"
    # Create new directory to store contexts
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
        print(f"Directory created at: {new_directory}")
    else:
        print(f"Directory already exists at: {new_directory}")
    counter = 0
    for status in statuses:
        # If the status is a root status and has replies
        # if status["in_reply_to_id"] is None and status["replies_count"] >= min_replies:
        if status["replies_count"] >= min_replies:
            response = requests.get(f"https://mastodon.social/api/v1/statuses/{status['id']}/context")
            if response.status_code == 200:
                with open(f"{new_directory}/{status['id']}_context.json", 'w') as json_file:
                    json.dump(json.loads(response.text), json_file, indent=4)
                    counter += 1
                    if (counter % 10 == 0):
                        print(f"Contexts Retrieved for {hashtag}:", counter)
            elif response.status_code == 429:  # Too many requests
                print("Rate limit exceeded. Waiting for 5 minutes...")
                time.sleep(310)  # Wait for 5 minutes before trying again
                with open(f"{new_directory}/{status['id']}_context.json", 'w') as json_file:
                    json.dump(json.loads(response.text), json_file, indent=4)
                    counter += 1
                    if (counter % 10 == 0):
                        print(f"Contexts Retrieved for {hashtag}:", counter)
            else:
                print(f"Error {response.status_code} for status {status['id']}")
                time.sleep(1)  # Add a delay of 1 second


