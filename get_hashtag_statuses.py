import requests
import json
import datetime
from parse_date import parse_date

# ================================================ hashtags
topics = {
    "hashtags_social": [
        # "WomensRights"
    ],
    "hashtags_policy": [
        "ClimateChange"
    ]
}

# ================================================ parameters
limit = 40
pages = 150
filter_date = datetime.datetime(2018, 1, 1)
saveAll = False # True means save all statuses based on limit and pages, False means save only filtered statuses

# ================================================ main loop (with pagination)
for topic, hashtags in topics.items():
    print("\n---", topic)
    # initial request
    for hashtag in hashtags:
        response = requests.get(f"https://mastodon.social/api/v1/timelines/tag/{hashtag}?limit={limit}")
        if response.status_code != 200:
            print(f"{hashtag}: None")
            continue
        statuses = json.loads(response.text)
        # next pages
        for _ in range(pages - 1):
            last_id = statuses[-1]["id"]
            response = requests.get(f"https://mastodon.social/api/v1/timelines/tag/{hashtag}?limit={limit}&max_id={last_id}")
            if response.status_code != 200:
                break
            else:
                new_statuses = json.loads(response.text)
                statuses.extend(new_statuses)
        filtered_statuses = []
        for status in statuses:
            created_at = parse_date(status["created_at"])
            if created_at >= filter_date:
                filtered_statuses.append(status)
        print(f"{hashtag}:", len(statuses), "\tfiltered:", len(filtered_statuses))
        if saveAll:
            with open(f"hashtags/{hashtag}_all.json", 'w') as json_file:
                json.dump(statuses, json_file, indent=4)
        else:
            with open(f"hashtags/{hashtag}.json", 'w') as json_file:
                json.dump(filtered_statuses, json_file, indent=4)

