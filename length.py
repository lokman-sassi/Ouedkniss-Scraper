import json
import pymongo

url =  'https://api.ouedkniss.com/graphql'

# Load the data from the JSON file
with open('ouedkniss_immobilier.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
            
# Get the length of the scraped data
print("Scraped items:", len(data))

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
mydb = client["Real-Estate"]
information = mydb.RealEstateListing
    
if information is not None:
    print("There is available data")
else:
    print("No data available")
num_documents = information.count_documents({})

print("Number of documents in the collection:", num_documents)

