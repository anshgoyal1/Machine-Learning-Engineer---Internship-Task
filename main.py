import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

# base URL for website
base_url = "https://www.kijiji.ca"

# URL for first page
page_1_url = base_url + '/b-jewelry-watch/canada/watch/page-1/k0c133l0?rb=true'

# to get response
response = requests.get(page_1_url)

# parse the text of html response
soup = BeautifulSoup(response.text, 'lxml')

# find all relevant ads
ads = soup.findAll("div", attrs={"class": ["search-item", "regular-ad"]})

ads = [x for x in ads if ("cas-channel" not in x["class"]) and ("third-party" not in x["class"])]

ad_links = []
for ad in ads:

    link = ad.find_all("a", {"class": "title"})

    for l in link:
        ad_links.append(base_url + l["href"])

df = pd.DataFrame(columns=["title", "price", "description", "date_posted", "address", "url"])

for advert in (ad_links):
  # grab webpage information & transform with BS
  response = requests.get(advert)
  soup = BeautifulSoup(response.text, "lxml")

  # get ad title
  try:
      title = soup.find("h1").text
  except AttributeError:
      title = ""

  # get ad price
  try:
      price = soup.find("span", attrs={"itemprop": "price"}).text
  except AttributeError:
      price = ""

  # get date posted
  try:
      date_posted = soup.find("div", attrs={"itemprop": "datePosted"})['content']
  except (AttributeError, TypeError):
      date_posted = ""

  # get ad description
  try:
      description = soup.find("div", attrs={"itemprop": "description"}).text
  except AttributeError:
      description = ""

  # get the ad city
  try:
      address = soup.find("span", attrs={"itemprop": "address"}).text
  except AttributeError:
      address = ""

  # apend information to the dataframe
  df = df.append({
       "title": title,
       "price": price,
       "description": description,
       "date_posted": date_posted,
       "address": address, 
       "url": advert},
      ignore_index=True
  )

# save the final dataframe to a csv file
df.to_csv("kijiji_watch_data.csv")
