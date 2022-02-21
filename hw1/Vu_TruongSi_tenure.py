import requests
import json
import sys

def tenure_count(k):
    database_url = 'https://dsci-551-eee46-default-rtdb.firebaseio.com/users.json?orderBy="tenure"&startAt=' + k
    r = requests.get(database_url)
    results = json.loads(r.content)
    print(len(results))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        tenure_count(sys.argv[1])
    else:
        print("Please provide the correct arguments")
else:
    print("Please run this program from the command line")