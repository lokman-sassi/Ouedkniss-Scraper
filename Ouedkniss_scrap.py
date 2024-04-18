import requests
import json
 
url = 'https://api.ouedkniss.com/graphql'

# Create an empty list to store all the scraped data
all_announcements = []

def fetch_media_urls(id):
    link_payload = {
        "operationName" : "AnnouncementGet",
        "variables" : {
            "id": id,
        },
        "query" : "query AnnouncementGet($id: ID!) {\n  announcement: announcementDetails(id: $id) {\n    id\n    reference\n    title\n    slug\n    description\n    orderExternalUrl\n    createdAt: refreshedAt\n    price\n    pricePreview\n    oldPrice\n    oldPricePreview\n    priceType\n    exchangeType\n    priceUnit\n    hasDelivery\n    deliveryType\n    hasPhone\n    hasEmail\n    quantity\n    status\n    street_name\n    category {\n      id\n      slug\n      name\n      deliveryType\n      __typename\n    }\n    defaultMedia(size: ORIGINAL) {\n      mediaUrl\n      __typename\n    }\n    medias(size: LARGE) {\n      mediaUrl\n      mimeType\n      thumbnail\n      __typename\n    }\n    categories {\n      id\n      name\n      slug\n      parentId\n      __typename\n    }\n    specs {\n      specification {\n        label\n        codename\n        type\n        __typename\n      }\n      value\n      valueText\n      __typename\n    }\n    user {\n      id\n      username\n      displayName\n      avatarUrl\n      __typename\n    }\n    isFromStore\n    store {\n      id\n      name\n      slug\n      description\n      imageUrl\n      url\n      followerCount\n      announcementsCount\n      locations {\n        location {\n          address\n          region {\n            slug\n            name\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      categories {\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    cities {\n      id\n      name\n      region {\n        id\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    isCommentEnabled\n    noAdsense\n    variants {\n      id\n      hash\n      specifications {\n        specification {\n          codename\n          label\n          __typename\n        }\n        valueText\n        value\n        mediaUrl\n        __typename\n      }\n      price\n      oldPrice\n      pricePreview\n      oldPricePreview\n      quantity\n      __typename\n    }\n    showAnalytics\n    messengerLink\n    __typename\n  }\n}"
    }
    headers = {
        'content-type':'application/json'
        }
    response = requests.post(url, data=json.dumps(link_payload), headers=headers).json()
    return response.get('data', {}).get('announcement', {}).get('medias', [])


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

        announcement_id =  announcement['id']

        #listing_link = f'https://www.ouedkniss.com/{announcement["slug"]}-d{announcement["id"]}'
    
            
        
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

        if announcement.get('price') is None:
            price = announcement['price']
        else:
            price = str(announcement['price']) + ' ' +  announcement['priceUnit'],
        

        media_urls = fetch_media_urls(announcement_id)
        
        images = [media['mediaUrl'] for media in media_urls]
        
        # Append announcement_info to all_announcements

        announcement_info = {
            'title': announcement['title'],
            'date published': announcement['createdAt'],
            'description': announcement['description'],
            'location': cities_data,
            'images': images,
            'price': price,
            'category': announcement['category']['slug'],
            'link': f'https://www.ouedkniss.com/{announcement["slug"]}-d{announcement["id"]}',
            'Surface': surface_description,
            'Store': 'Ouedkniss',
        }
        all_announcements.append(announcement_info)

# Save all_announcements to a JSON file
with open('ouedkniss_immobilier.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_announcements, json_file,ensure_ascii=False, indent=4)
