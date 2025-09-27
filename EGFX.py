#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup 
import datetime
import os


# In[20]:


URL = "https://www.cbe.org.eg/en/economic-research/statistics/exchange-rates"
Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36" , "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1" }
# Note 
# The cbe displays the rate after 2 days so if the scrape date is 5 the data is for day 3
page = requests.get(URL , headers = Headers)
page.encoding = "utf-8"
soup = BeautifulSoup(page.content, "html.parser")
scrape_time = datetime.date.today().isoformat()

print("Status code:", page.status_code)
print("Response length:", len(page.text))
print("First 300 chars of response:\n", page.text[:300])

table = soup.find("table", class_= "table-comp layout-auto")
if not table:
    raise RuntimeError("❌ Table not found — check if request blocked or HTML structure changed")

rows = []

for tr in table.select("tbody tr"):
    cells = [td.get_text(strip=True) for td in tr.find_all("td")]
    # Skip empty rows
    if any(cells):
        rows.append(cells)
for r in rows:
    r.append(scrape_time)


# In[25]:


column = ["currencies", "Buy", "Sell", "Scrape_time"]
df = pd.DataFrame(rows, columns = column)

csv_file = "EGFX.csv"
if os.path.exists(csv_file):
    df_old= pd.read_csv(csv_file)
else:
    df_old = pd.DataFrame(columns = column)

df_combined = pd.concat([df_old, df], ignore_index = True)
df_clean = df_combined.drop_duplicates(subset=["currencies", "Scrape_time"])

df_clean.to_csv(csv_file, index = False)



# In[ ]:




