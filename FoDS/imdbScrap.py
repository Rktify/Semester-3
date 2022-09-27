from urllib import response
from bs4 import BeautifulSoup
import requests
import pandas as pd

list = []

for i in range(1, 4):
    response = requests.get('https://www.imdb.com/title/tt1190634/episodes?season=' + str(i))
    soup = BeautifulSoup(response.text, "html.parser")

    episode_container = soup.find_all('div', class_ ="info")
    for episodes in episode_container:
        season = i
        image = ""
        episode = episodes.meta['content']
        title = episodes.a['title']
        airdate = episodes.find('div', class_='airdate').text.strip()
        images = soup.find_all('img', class_ ='zero-z-index')
        for img in images:
            if img['alt'] == title:
                image = img['src']
        rating = episodes.find('span', class_='ipl-rating-star__rating').text
        total_votes = episodes.find('span', class_='ipl-rating-star__total-votes').text.strip()
        votes = total_votes.replace("(","").replace(")","")
        description = episodes.find('div', class_='item_description').text.strip()
        url = episodes.a['href']
        realURL = "https://www.imdb.com" + url
        data = [season, episode, title, airdate, rating, votes, description, realURL, image]
        list.append(data)

list = pd.DataFrame(list, columns=["Season", "Episode", "Title", "Airdate", "Rating", "Total Votes", "Description", "URL", "Image"])
list.to_csv('The Boys.csv',index=False)
