import requests
from bs4 import BeautifulSoup as BS
import re
from datetime import datetime
from dateutil.parser import isoparse
import pytz

class Performance:

    def __init__(self, datetime, title, composer, venue):
        self.datetime = datetime
        self.title = title
        self.composer = composer
        self.venue = venue

        
    def __str__(self):
        #ATH. skoða Locale modulinn fyrir þýsku
        return f"{self.title} von {self.composer}. " + datetime.strftime(self.datetime, "Am %x, um %X. ") + self.venue

    def get_datetime(self):
        return self.datetime

    def get_title(self):
        return self.title

    def get_composer(self):
        return self.composer

class Artist:

    def __init__(self, name):
        '''name: string, performances: list of Performance objects'''
        self.name = name
        self.performances = staatsoper_search(name)


    def __str__(self):
        performanceStrings = [performance.__str__() for performance in self.performances] 
        return f"{self.name}. Number of found performances: {len(self.performances)}\n" + "\n".join(performanceStrings)       



def staatsoper_search(person):

    page = requests.get("https://www.wiener-staatsoper.at/suche/spezielle-suche/?tx_gdstop_search[location]=spielplan&tx_gdstop_search[sword]=" + person)
    soup = BS(page.content, 'html.parser')

    calendar = soup.find('div', class_="calendar-list load-culturall")
    operas = calendar.find_all('div', class_=re.compile('oper$'))
    
    if not operas:
        return None

    performances = []

    # gets performance metadata 
    for div in operas:    
        get = False
        
        metadata = div.find('div', class_ = "metadata")
        
        if not metadata:
            continue

        date = metadata.find('span', itemprop='startDate')
        date = str(date.string)
        #breytir í datetime hlut
        date = isoparse(date)

        title = metadata.find('span', itemprop='name', recursive = False)
        title = str(title.string)

        composer = metadata.find('span', itemprop='performer')
        composerName = composer.find('span', itemprop='name')
        composerName = str(composerName.string)

        # breytir í performance hlut
        performances.append(Performance(date, title, composerName, "Wiener Staatsoper"))

    return performances

print(Artist("Rachvelishvili"))