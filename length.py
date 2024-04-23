import json
import requests
import pymongo


url =  'https://api.ouedkniss.com/graphql'


# Load the data from the JSON file
with open('ouedkniss_immobilier.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

            

# Get the length of the scraped data
print("Scraped items:", len(data))

"page that contains the first listing in 2022: 3611"

"link of the first listing in 2022" "https://www.ouedkniss.com/local-vente-alger-bab-el-oued-algerie-d29167436"


client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
mydb = client["Real-Estate"]
information = mydb.RealEstateListing
    
if information is not None:
    print("There is available data")
else:
    print("No data available")
num_documents = information.count_documents({})

print("Number of documents in the collection:", num_documents)

for page in range(1, 6):
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
        paginator = resp['data']['search']['announcements']['paginatorInfo']['lastPage']  
        
print(paginator)
        
