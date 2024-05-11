import json
from datetime import datetime
import pandas as pd

date_str = datetime.now().strftime("%y%m%d")
print(f"date_str: {date_str}")

all_papers = json.load(open('backdoor_dblp_240511.json'))
print(f"Number of papers: {len(all_papers)}")

# Filter papers
group_by_title = {}
for paper in all_papers:
    title_lower = paper['info']['title'].lower()
    if title_lower not in group_by_title:
        group_by_title[title_lower] = []
    group_by_title[title_lower].append(paper)
print(f"Number of unique papers: {len(group_by_title)}")

# Process duplicates
# keys_dict = ['author', 'title', 'venue', 'volume', 'year', 'type', 'access', 'key', 'doi', 'ee', 'url']
# keys_dict = ['author', 'title', 'venue', 'volume', 'year', 'type', 'access', 'key', 'doi', 'ee', 'url']
keys_dict = ['year', 'title', 'author', 'venue', 'volume', 'url']
pp_dict = {k: [] for k in keys_dict}

for title, papers in group_by_title.items():
    paper = papers[0]['info']
    try:
        authors = paper['authors']['author']
        authors = [a['text'] for a in authors]
        authors = ', '.join(authors)
    except:
        authors = ''
    venue = paper.get('venue', '')
    if isinstance(venue, list):
        venue = ' - '.join(venue[::-1])
    pp_dict['author'].append(authors)
    pp_dict['title'].append(paper.get('title', ''))
    pp_dict['venue'].append(venue)
    pp_dict['year'].append(paper.get('year', ''))
    pp_dict['volume'].append(paper.get('volume', ''))
    pp_dict['url'].append(paper.get('ee', ''))

df_pp = pd.DataFrame(pp_dict)

# sort by year
df_pp = df_pp.sort_values(by='year', ascending=False)


df_pp.to_csv(f'fl_dblp_{date_str}.csv', index=False)

print(f"Number of venue: {len(df_pp['venue'].unique())}")


topics = {
    'Survey': ['survey'],
    'Federated Learning (FL)': ['federated'],
    'Natural Language Processing (NLP)': ['language', 'nlp'],
    'Automatic Speech Recognition (ASR)': ['speech', 'audio', 'voice'],
    'Watermarking': ['watermarking', 'watermarks'],
    'Reinforcement Learning': ['reinforcement learning'],
    'Few-Shot Learning': ['few-shot', 'zero-shot'],
    '3D': ['3d'],
    'Machine Unlearning': ['unlearning'],
    'Physical Backdoor': ['physical'],
    'Diffusion': ['diffusion'],
    'Transformer': ['transformer'],
    'Clean-label Backdoor': ['clean-label', 'clean label'],
    'Video': ['video'],
    'Segmentation': ['segmentation'],
    'Graph Learning': ['graph'],
    'Machine Learning (ML)': ['machine learning'],
    'Others': [],
    'Irrelevance': [],
}

data_cat = {k: [] for k in topics.keys()}

for _, paper in df_pp.iterrows():
    default_cat = 'Others'
    year = paper['year']
    if int(year) <= 2015:
        default_cat = 'Irrelevance'
    else:
        for cat in data_cat.keys():
            kw =  topics[cat]
            for w in kw:
                if w in paper['title'].lower():
                    default_cat = cat
            if default_cat != 'Others':
                break
    data_cat[default_cat].append(paper)

for k in data_cat:
    print(k, len(data_cat[k]))



data_fl_md = ""

for kk, vv in data_cat.items():

    data_to_md = f'# {kk}\n'
    data_to_md += '|No. | Title | Venue | Year | Author | Volume | \n'
    data_to_md += '|----|-------|-------|------|--------|--------|\n'

    for id, pp in enumerate(vv):
        # print(f"Other {id}: {pp['title']} -- {pp['info']}")
        # data_to_md += f"| {id + 1} | {pp['title']} | {pp['info']} | {pp['pub_time']} | {pp['author']} |\n"
        data_to_md += f"| {id + 1} | [{pp['title']}]({pp['url']}) | {pp['venue']} | {pp['year']} | {pp['author']} | {pp['volume']} | {pp['url']} |\n"

    # print(data_to_md)
    data_fl_md += data_to_md
    
with open(f'./backdoor_dblp_{date_str}.md', "w") as fw:
    fw.write(data_fl_md)



