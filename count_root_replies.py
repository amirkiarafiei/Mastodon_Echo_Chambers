import json

# ========================================== Count of replies for a root status (for each ID in each hashtag)
hashtags = [
            "ClimateChange",
            # "WomensRights"
            ]

# Open the JSON file of each hashtag, then loop over the IDs of each status, and then get the context of that ID
min_replies = 2
for hashtag in hashtags:
    print(f"\n--- {hashtag}")
    with open(f"hashtags/{hashtag}.json", 'r') as json_file:
        statuses = json.load(json_file)
        count = 0
        for status in statuses:
            if status["replies_count"] >= min_replies:
                print(f"{status['id']}: {status['replies_count']}")
                count += 1
        print(f"Total: {count}")