from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import time, os

# Populates tmp/ with jsons of urls to download
with open("nft_grab.json", "r") as f:
    data = json.load(f)

with open("gql.schema", "r") as f:
    query = gql(f.read())

gql_data = data["gql"]
for thing in gql_data:
    sample_transport = RequestsHTTPTransport(
        url=gql_data[thing]["api"],
        use_json=True,
        headers={
            "Content-type": "application/json",
        },
        verify=False,
        retries=3,
    )

    client = Client(transport=sample_transport, fetch_schema_from_transport=True)
    x = client.execute(query)
    path = f"tmp/{thing}/"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + "index.json", "w+") as f:
        f.write(json.dumps(x, indent=4))
