import requests, json

def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


new_query = """
{
    items{
        id
        name
        shortName
    }
}
"""

result = run_query(new_query)
a = open("./game_info/items.json","w")
a.write(json.dumps(result["data"]["items"]))
a.close()