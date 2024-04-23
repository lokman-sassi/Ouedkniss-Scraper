import requests
import json
from datetime import datetime, timedelta
import pymongo

 
# Ouedkniss API url of the link: "https://www.ouedkniss.com/immobilier/1", it retrieves the listings of those categories: Vente-Location-Echange-Cherche location-Cherche achat.
url = 'https://api.ouedkniss.com/graphql'
all_announcements = []



# Function to fetch data (all images of a listing if found) from a given id of a listing
def fetch_medias_urls(id):
    try:
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
        return response.get('data', {}).get('announcement', {}).get('medias', {})
    except Exception as e:
        print("An error occured while fetching images: ", str(e))
        return []
    
    
    
# Function that retieves the listings data    
def fetch_listings(page):
        payload = {
            "operationName": "SearchQuery", 
            "variables": {
                "mediaSize": "MEDIUM", 
                "q": None,
                "filter": {
                    "categorySlug":"immobilier", # it can be: "immobilier-vente" - "immobilier-location"
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
                    "priceUnit": None, # 0: "MILLION", 1: "UNIT", 2: "BILLION", 3: "UNIT_PER_SQUARE", 4: "MILLION_PER_SQUARE"
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
        return announcements_data
    
    
    
# Function that retrieves the number of the last page    
def get_last_page(page):
        payload = {
            "operationName": "SearchQuery", 
            "variables": {
                "mediaSize": "MEDIUM", 
                "q": None,
                "filter": {
                    "categorySlug":"immobilier", # it can be: "immobilier-vente" - "immobilier-location"
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
                    "priceUnit": None, # 0: "MILLION", 1: "UNIT", 2: "BILLION", 3: "UNIT_PER_SQUARE", 4: "MILLION_PER_SQUARE"
                    "regionIds": []
                }
            },
            "query": "query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        slug\n        icon\n        delivery\n        deliveryType\n        priceUnits\n        children {\n          id\n          name\n          slug\n          icon\n          __typename\n        }\n        specifications {\n          isRequired\n          specification {\n            id\n            codename\n            label\n            type\n            class\n            datasets {\n              codename\n              label\n              __typename\n            }\n            dependsOn {\n              id\n              codename\n              __typename\n            }\n            subSpecifications {\n              id\n              codename\n              label\n              type\n              __typename\n            }\n            allSubSpecificationCodenames\n            __typename\n          }\n          __typename\n        }\n        parentTree {\n          id\n          name\n          slug\n          icon\n          children {\n            id\n            name\n            slug\n            icon\n            __typename\n          }\n          __typename\n        }\n        parent {\n          id\n          name\n          icon\n          __typename\n        }\n        __typename\n      }\n      count\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        icon\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    isOfficial\n    isVerified\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    mimeType\n    thumbnail\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  oldPricePreview\n  priceType\n  exchangeType\n  category {\n    id\n    slug\n    __typename\n  }\n  __typename\n}\n",
        }

        headers = {
            'content-type':'application/json'
        }
        
        resp = requests.post(url,data=json.dumps(payload),headers=headers).json()
        last_page = resp['data']['search']['announcements']['paginatorInfo']['lastPage']  
        return last_page
            


# Function to save all the announcements to a JSON file
def save_data():
    for announcement in all_announcements:
        if '_id' in announcement:
            del announcement['_id']

    with open("ouedkniss_immobilier.json", 'w', encoding= 'utf-8') as json_file:
        json.dump(all_announcements, json_file,ensure_ascii=False, indent=4)
        
        

# Function that stores the announcements in the data base
def save_to_database(records):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    mydb = client["Real-Estate"]
    information = mydb.RealEstateListing
    if information is not None:
        existing_urls = []
        for record in information.find():
            existing_urls.append(record['Link'])
                
        for record in records:
            if record['Link'] in existing_urls:
                break
            else:
                information.insert_one(record)
    
    else:
        information.insert_many(records)



# Main function
def main():
    last_page = get_last_page(1)
    print("Total number of pages: ", last_page)
    try:
        for page in range(1, last_page):
            announcements_data = fetch_listings(page)
            
            # Extract relevant information from each announcement
            for announcement in announcements_data:
                source = "Ouedkniss"
                surface = ""              
                cities_data = []
                surface_description = ""
                announcement_id =  announcement['id'] 
                price = ""            
                
                
                # Changing location format
                for city in announcement['cities']:
                    city_name = city['name']
                    region = city['region']['name']
                    cities_data.append(f"{city_name}, {region}")
                    
                if cities_data:
                    location = cities_data[0]
                else:
                    location = None
                
                
                # Fetching the surface value
                if announcement['smallDescription']:  
                    for description in announcement['smallDescription']:
                        value_text = description['valueText']
                        surface_description = value_text[0]
                        if surface is None:
                            surface = None
                        else:
                            surface = surface_description
                else:
                    surface = None
                
                
                # Changing price format      
                if announcement['price']:
                    price = str(announcement['price']) + ' ' + "DZD"
                else:
                    price = None
                    
                    
                # Calling fetch_listing_content function and extracting media urls from media key
                media_urls = fetch_medias_urls(announcement_id)
                images = [media['mediaUrl'] for media in media_urls if media]
                if not images:
                    images = "No images were found"
                elif len(images) == 1:
                    images = images[0]
                    
                
                # Parse the createdAt timestamp as a datetime object
                createdAt = datetime.strptime(announcement['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")

                # Add one hour to the createdAt timestamp
                parsed_time = createdAt + timedelta(hours=1)

                # Convert the updated timestamp back to the string format
                Date = parsed_time.strftime('%Y-%m-%dT%H:%M:%S') + ".000Z"
                
                
                print("Title:", announcement['title'])
                print("Price:", price)
                print("Location:", location)
                print("Description:", announcement['description'])
                print("Images:", images)
                print("Source:", source)
                print("Published Date:", Date)
                print("Link:", f'https://www.ouedkniss.com/{announcement["slug"]}-d{announcement["id"]}')
                print("Category:", announcement['category']['slug'])
                print("Surface:", surface)
                print("-" * 50)

                announcement_info = {
                    'Title': announcement['title'],
                    'Price': price,
                    'Location': location,
                    'Description': announcement['description'],
                    'Images': images,
                    'Source': source,
                    'Published Date': Date,
                    'Link': f'https://www.ouedkniss.com/{announcement["slug"]}-d{announcement["id"]}',
                    'Category': announcement['category']['slug'],
                    'Surface': surface,
                }
                all_announcements.append(announcement_info)
                save_data()
                
        
        save_to_database(all_announcements)
        
    except Exception as e:
        print("An error occured: ", str(e))
    
    finally:
        save_to_database(all_announcements)
            
                        
              
if __name__ == "__main__":
    main()
