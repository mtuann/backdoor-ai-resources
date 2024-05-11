import requests
import json
from datetime import datetime

# need to update the keywords by year and number of papers from DBLP
keywords = [ ['backdoor', [[2024, 1514] ] ] ] 
all_data = []
acc_num = 0
for kw in keywords:
    print(kw[0])
    for year, cnt in kw[1]:
        acc_num += cnt
        for num_page in range((cnt + 999) // 1000):            
            kwq = f'{kw[0]}'
            url_api = f'https://dblp.org/search/publ/api?q={kwq}&h=1000&f={num_page * 1000}&format=json'
            print(url_api)
            
            try:
                json_data = requests.get(url_api).json()
                all_data.extend(json_data['result']['hits']['hit'])                
            except Exception as e:
                pass
        print(f"Up to {year} : {len(all_data)}, cnt: {acc_num}")


date_str = datetime.now().strftime("%y%m%d")
with open(f'backdoor_dblp_{date_str}.json', 'w') as f:
    json.dump(all_data, f, indent=2)

