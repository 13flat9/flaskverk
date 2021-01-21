import requests
from bs4 import BeautifulSoup as BS
import re
import datetime
from dateutil.parser import isoparse


class Performance:

    def __init__(self, date, title, composer):
        #Skoða hvernig tímasvæði virka
        self.date = date 
        self.title = title
        self.composer = composer

    def __str__(self):
        return f"{self.composer}'s {self.title}. On {self.date}"

    def get_date(self):
        return self.date

    def get_title(self):
        return self.title

    def get_composer(self):
        return self.composer








def staatsoper_search(person):

    page = requests.get("https://www.wiener-staatsoper.at/suche/spezielle-suche/?tx_gdstop_search[location]=spielplan&tx_gdstop_search[sword]=" + person)
    soup = BS(page.content, 'html.parser')

    calendar = soup.find('div', class_="calendar-list load-culturall")
    operas = calendar.find_all('div', class_=re.compile('oper$'))
    

    if not operas:
        return None

    performances = []

    # get performance metadata 
    for div in operas:    
        get = False
        
        
        metadata = div.find('div', class_ = "metadata")
        
        if not metadata:
            continue

        date = metadata.find('span', itemprop='startDate')
        date = str(date.string)
        #breyta í datetime hlut
        #Ath. skoða hvernig DST virkar í datetime
        date = isoparse(date)



        title = metadata.find('span', itemprop='name', recursive = False)
        title = str(title.string)

        composer = metadata.find('span', itemprop='performer')
        composerName = composer.find('span', itemprop='name')
        composerName = str(composerName.string)


        # breyta í performance object í stað strengs
        performances.append(Performance(date, title, composerName))

    return performances



for performance in staatsoper_search("rachvelishvili"):
    print(performance)