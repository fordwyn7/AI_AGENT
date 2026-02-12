# type: ignore
import os
from dotenv import load_dotenv
load_dotenv()


from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]

search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

results = search_client.search(search_text="best place")

for result in results:
    print(f"Title: {result['title']} \n Content: {result['chunk']}\n\n")


from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SimpleField, SearchFieldDataType, SearchableField, ComplexField, CorsOptions, SearchIndex, ScoringProfile
from typing import List

key = "ic02ge9qW3Db1VDRV2cHQOlbO6SoPTCgJ78XyncrY0AzSeCQ3XH6"
client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
name = "hotels"
fields = [
    SimpleField(name="hotelId", type=SearchFieldDataType.String, key=True),
    SimpleField(name="baseRate", type=SearchFieldDataType.Double),
    SearchableField(name="description", type=SearchFieldDataType.String),
    ComplexField(
        name="address",
        fields=[
            SimpleField(name="streetAddress", type=SearchFieldDataType.String),
            SimpleField(name="city", type=SearchFieldDataType.String),
        ],
        collection=True,
    ),
]
cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
scoring_profiles: List[ScoringProfile] = []
index = SearchIndex(name=name, fields=fields, scoring_profiles=scoring_profiles, cors_options=cors_options)

result = client.create_index(index)
client.delete_index(name)


DOCUMENT = {
    "hotelId": "1000",
    "baseRate": 4.0,
    "address": [{
        "streetAddress": "Sample street adress",
        "city": "London"
    }],
    "description": "Azure Inn",
}


search_client = SearchClient(service_endpoint, name, AzureKeyCredential(key))
result = search_client.upload_documents(documents=[DOCUMENT])

print("Upload of new document succeeded: {}".format(result[0].succeeded))

