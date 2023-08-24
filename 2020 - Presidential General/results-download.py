import requests
from datetime import datetime
import time

from result_ETL import build_results

url = 'https://feeds-elections.foxnews.com/archive/politics/elections/2020/3/2020_Generals/President/national_summary_results/file.json'

while True:
    r = requests.get(url, allow_redirects=True)
    fName = 'election-results/results'+ str(datetime.now().timestamp())+ '.json'
    f = open(fName, 'wb').write(r.content)
    print("Saved " + fName)
    build_results()
    time.sleep(600)