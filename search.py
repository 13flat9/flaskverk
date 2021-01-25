import requests
from bs4 import BeautifulSoup as BS
import re
from datetime import datetime
from dateutil.parser import isoparse
import pytz
import locale

#bæta einhvern tímann við stillingu fyrir þetta?
locale.setlocale(locale.LC_ALL, 'de_DE')


class Performance:

    def __init__(self, datetime, title, composer, venue, event_link):
        self.datetime = datetime
        self.title = title
        if composer == None:
            self.composer = "missing"
        self.composer = composer
        self.event_link = "https://www.wiener-staatsoper.at" + event_link
        self.venue = venue

        
    def __str__(self):
        #ATH. skoða Locale modulinn fyrir þýsku
        return f"{self.title} von {self.composer}. " + datetime.strftime(self.datetime, "%A, %d. %B, %H:%M. ") + self.venue

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
        self.performances = self.staatsoper_search()


    def __str__(self):
        performanceStrings = [performance.__str__() for performance in self.performances] 
        return f"{self.name}. Number of found performances: {len(self.performances)}\n" + "\n".join(performanceStrings)       


    # vantar að sækja hlekkinn á sýninguna 
    # sækir bara óperur, ekki tónleika
    def staatsoper_search(self):

        page = requests.get("https://www.wiener-staatsoper.at/suche/spezielle-suche/?tx_gdstop_search[location]=spielplan&tx_gdstop_search[sword]=" + self.name)
        soup = BS(page.content, 'html.parser')

        calendar = soup.find('div', class_="calendar-list load-culturall")
        if not calendar: 
            return None

        operas = calendar.find_all('div', class_=re.compile('oper$'))
        if not operas:
            return None

        performances = []

        # gets performance metadata 
        for div in operas:
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
            if composer:        
                composerName = composer.find('span', itemprop='name')
                composerName = str(composerName.string)

            location = metadata.find('span', itemprop='location', recursive = False)
            location = location.find('span', itemprop='name', recursive = False)
            location = str(location.string)

            event_title = div.find('h2', class_='event-title')
            event_link = event_title.find('a')
            event_link = event_link['href']

            # breytir í performance hlut
            performances.append(Performance(date, title, composerName, location, event_link))

        return performances
