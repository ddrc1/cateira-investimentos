# %%
import pandas as pd
from yfinance import Ticker
import sys
import ast
import json
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from tqdm import tqdm
sys.path.append("/mnt/d/Projetos/Python/cateira-investimentos/apps/utils/scripts")

#%%
import scraping.selenium_scraping as selenium_scraping
import scraping.get_csv_data as get_csv_data
import scraping.html_scraping as html_scraping

# %%
list_code_1 = get_csv_data.list_codes
list_code_2 = selenium_scraping.list_codes
list_code_3 = html_scraping.list_codes

list_codes = set(list(list_code_1) + list(list_code_2) + list(list_code_3))

# %%
list_codes = list(list_codes)
for i, (code, _) in enumerate(list_codes):
    if code == "":
        del list_codes[i]

# %%
info_list = []
for code, asset_type in tqdm(list_codes):
    try:
        if asset_type == 'Cryptocurrency':
            tick = Ticker(code + "-USD")
        else:
            tick = Ticker(code)

        info = tick.info

        if len(info.keys()) <= 1:
            tick = Ticker(code + ".SA")
            info = tick.info

            if len(info.keys()) <= 1:
                info_list.append({'code': code, 'asset_type': asset_type, 'info': None})
                continue

    except Exception as e:
        print(e)
        continue
    
    info_list.append({'code': code, 'asset_type': asset_type, 'info': info})

# %%
info_df = pd.DataFrame(info_list)

# %%
#info_df.to_csv("info_list_checkpoint.csv", index=False)
info_df = pd.read_csv("info_list_checkpoint.csv")

# %%
info_df.info()
# %%
info_df_na = info_df[info_df['info'].isna()]
info_df = info_df.dropna()

info_df.reset_index(inplace=True, drop=True)
info_df_na.reset_index(inplace=True, drop=True)

# %%
infos_dict = info_df['info'].apply(ast.literal_eval).to_list() #to_list()

# %%
info_df = pd.concat([info_df.drop(columns=['info']), pd.DataFrame(infos_dict)], axis=1)
info_df = pd.concat([info_df, info_df_na])
info_df.reset_index(inplace=True)

# %%
info_df
#info_df[(~info_df['name'].isna()) & (~info_df['longBusinessSummary'].isna())]
# info_df[info_df['asset_type'] == 'Cryptocurrency']

# %%
info_df = info_df[['code', 'asset_type', 'name', 'description', 'longBusinessSummary', 'longName', 'country', 'industry', 'sector']]
print(info_df['sector'].unique())
print(info_df['industry'].unique())

# %%
documents = []
with open("../../../assets/fixtures/sub_sector.json") as file:
    json_data = json.load(file)
    for sub_sector in tqdm(json_data):
        documents.append(Document(page_content=sub_sector['fields']['description'], 
                                  metadata={"pk": sub_sector['pk'], "name": sub_sector['fields']['name']}))

embedding = HuggingFaceEmbeddings()
vectorstore = FAISS.from_documents(documents=documents, embedding=embedding)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# %%
info_df['industry'] = info_df.apply(lambda row: retriever.invoke(row['longBusinessSummary'])[0].metadata['name']
                                                if pd.notna(row['longBusinessSummary']) and pd.isna(row['industry'])
                                                else row['industry'], axis=1)
# %%
info_df.info()

# %%
info_df.fillna("", inplace=True)

# %%
info_df
# %%
asset_types = []
with open("../../../assets/fixtures/asset_type.json") as file:
    asset_types = json.load(file)

asset_types
# %%
with open('../../../assets/fixtures/asset.json', encoding='utf-8', mode='w+') as file:
    data = []
    for row in info_df.itertuples():
        description = row.description if row.asset_type == "Cryptocurrency" else row.longBusinessSummary
        full_name = row.name if row.asset_type == "Cryptocurrency" else row.longName

        if row.industry != "":
            sub_sector = [document.metadata["pk"] for document in documents if document.metadata["name"] == row.industry][0]
        else:
            sub_sector = None

        asset_type = [asset_type["pk"] for asset_type in asset_types if asset_type["fields"]["name"] == row.asset_type][0]

        data.append(
            {
                "model": "apps_assets.Asset",
                "pk": row.Index + 1,
                "fields": {
                    "code": row.code,
                    "description": description,
                    "full_name": full_name,
                    "sub_sector": sub_sector,
                    "asset_type": asset_type,
                    "country": row.country,
                    "created_at": "2025-01-01T12:00:00Z",
                    "updated_at": "2025-01-01T12:00:00Z",
                    "active": True
                }
            }
        )
    
    json.dump(data, file, indent=4, ensure_ascii=False)
# %%
