import requests
import json

url = 'https://api.ouedkniss.com/graphql'

all_announcements = []

id = 38802808
def fetch_media_urls(id):
    link_payload = {
        "operationName" : "AnnouncementGet",
        "variables" : {
            "id": id,
        },
        "query" : "query AnnouncementGet($id: ID!) {\n  announcement: announcementDetails(id: $id) {\n    medias(size: LARGE) {\n      mediaUrl\n      mimeType\n      thumbnail\n      __typename\n    }\n    __typename\n  }\n}"
    }

    response = requests.post(url, data=json.dumps(link_payload), headers={'content-type':'application/json'}).json()
    return response.get('data', {}).get('announcement', {}).get('medias', [])

# Fetch mediaUrls for the announcement
media_urls = [media['mediaUrl'] for media in media_urls['medias']]

announcement_info = {
            'images': media_urls,
        }
all_announcements.append(announcement_info)


# Save all_announcements to a JSON file
with open('test.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_announcements, json_file, ensure_ascii=False, indent=4)
            