import requests
import json
 
url = 'https://api.ouedkniss.com/graphql'

# Create an empty list to store all the scraped data
all_announcements = []

for page in range(1, 20):
    payload = {
        "operationName": "SearchQuery", 
        "variables": {
            "mediaSize": "MEDIUM", 
            "q": None,
            "filter": {
                "categorySlug":"immobilier",
                "cityIds":[],
                "connected":False,
                "count": 48,
                "delivery":None,
                "exchange":False,
                "regionIds":[],
                "cityIds":[],
                "fields":[],
                "hasPictures":False,
                "hasPrice":False,
                "origin": None,
                "page":page,
                "priceRange": [None, None],
                "priceUnit": None,
                "regionIds": []
            }
        },
        "query": "query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        slug\n        icon\n        delivery\n        deliveryType\n        priceUnits\n        children {\n          id\n          name\n          slug\n          icon\n          __typename\n        }\n        specifications {\n          isRequired\n          specification {\n            id\n            codename\n            label\n            type\n            class\n            datasets {\n              codename\n              label\n              __typename\n            }\n            dependsOn {\n              id\n              codename\n              __typename\n            }\n            subSpecifications {\n              id\n              codename\n              label\n              type\n              __typename\n            }\n            allSubSpecificationCodenames\n            __typename\n          }\n          __typename\n        }\n        parentTree {\n          id\n          name\n          slug\n          icon\n          children {\n            id\n            name\n            slug\n            icon\n            __typename\n          }\n          __typename\n        }\n        parent {\n          id\n          name\n          icon\n          __typename\n        }\n        __typename\n      }\n      count\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        icon\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    isOfficial\n    isVerified\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    mimeType\n    thumbnail\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  oldPricePreview\n  priceType\n  exchangeType\n  category {\n    id\n    slug\n    __typename\n  }\n  __typename\n}\n",
    }

    headers = {
        'content-type':'application/json'
        }
    
    resp = requests.post(url,data=json.dumps(payload),headers=headers).json()
    announcements_data = resp['data']['search']['announcements']['data']
    
    
    # Extract relevant information from each announcement
    for announcement in announcements_data:
        cities_data = []
        surface_description = {}
        media = {}
        
        for city in announcement['cities']:
            city_name = city['name']
            region = city['region']['name']
            cities_data.append(f"{city_name}, {region}")

        for description in announcement['smallDescription']:
            value_text = description['valueText']
            surface_description = value_text

        if announcement.get('store') is not None:
            store_name = announcement['store']['name']
        else:
            store_name = None

        if announcement.get('defaultMedia') is not None:
            media = announcement['defaultMedia']['mediaUrl']
        else:
            media = None

        announcement_info = {
            'title': announcement['title'],
            'date published': announcement['createdAt'],
            'description': announcement['description'],
            'cities': cities_data,
            'store': store_name,
            'image': media,
            'price': announcement['price'],
            'pricePreview': announcement['pricePreview'],
            'priceUnit': announcement['priceUnit'],
            'pricetype': announcement['priceType'],
            'exchangeType': announcement['exchangeType'],
            'category': announcement['category']['slug'],
            'Surface': surface_description
        }
        all_announcements.append(announcement_info)

# Save all_announcements to a JSON file
with open('ouedkniss_immobilier.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_announcements, json_file,ensure_ascii=False, indent=4)
