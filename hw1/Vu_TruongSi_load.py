import pandas as pd
import requests

database_url = "https://dsci-551-eee46-default-rtdb.firebaseio.com/users.json"
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
senior_df = df[df["SeniorCitizen"] == 1]
r = requests.put(database_url, data=senior_df.to_json(orient="records"))
