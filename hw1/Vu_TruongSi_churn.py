import requests
import json
import sys

def churned_customers(k):
    database_url = 'https://dsci-551-eee46-default-rtdb.firebaseio.com/users.json?orderBy="Churn"&equalTo="Yes"&limitToFirst=' + k
    r = requests.get(database_url)
    results = json.loads(r.content)
    customer_ids = []
    for customer in results.keys():
        customer_ids.append(results[customer]["customerID"])

    customer_ids = sorted(customer_ids)
    for id in customer_ids:
        print(id)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        churned_customers(sys.argv[1])
    else:
        print("Please provide the correct arguments")
else:
    print("Please run this program from the command line")