import requests
import json
import os
import time

def get_followings_as_json(account_id):
    limit = 80
    followings = []
    # Function to parse the Link header
    def parse_link_header(header):
        links = {}
        for part in header.split(','):
            section = part.split(';')
            url = section[0].strip()[1:-1]
            name = section[1].strip().split('=')[1][1:-1]
            links[name] = url
        return links

    # Initial request
    url = f"https://mastodon.social/api/v1/accounts/{account_id}/following?limit={limit}"
    while url:
        followings_response = requests.get(url)
        time.sleep(1)
        if followings_response.status_code != 200:
            break
        new_followings = followings_response.json()
        if not new_followings:
            break
        followings.extend(new_followings)
        # Parse the Link header
        link_header = followings_response.headers.get('Link', '')
        pagination_urls = parse_link_header(link_header)
        url = pagination_urls.get('next')

    return followings


if __name__ == '__main__':
    # =================================== get followings based on account id
    account_id = 112688684539194456
    with open(f"followings/{account_id}_followings.json", 'w') as json_file:
        json.dump(get_followings_as_json(account_id), json_file, indent=4)

