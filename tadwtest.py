import re
import requests
from bs4 import BeautifulSoup as BS






def get_performance_links():
    response = requests.get('https://www.theater-wien.at/de/programm/saison-2020-2021')
    soup = BS(response.content, 'html.parser')
    event_cats = soup.find_all("h2", class_="eventcattitle")

    #skrifa sem filter()?
    for cat in event_cats:
        print(cat)
        if cat.string=="Oper":
            oper = list(cat.find_next_sibling("div").find_all("a", recursive=True))
        elif cat.string=="Kammeroper":
            kammeroper = list(cat.find_next_sibling("div").find_all("a", recursive=True))
        elif cat.string=="Oper konzertant":
            oper_konzertant = list(cat.find_next_sibling("div").find_all("a", recursive=True))

    performance_links = {'https://www.theater-wien.at/' + performance["href"] for performance in [*oper, *kammeroper, *oper_konzertant]}
    return performance_links

def is_in_performance(person, performance_url):
    response = requests.get(performance_url)
    soup = BS(response.content, 'html.parser')
    cast_table = soup.find(class_="cast-table", recursive=True)
    cast = (cast_table.find_all(class_="castname"))
    cast = [item.string for item in cast]
    # of óskiljanlegt?
    if list(filter(lambda string: re.search(person, string), cast)):
        return True
    else:
        return False

#næst: finna Höfund, stað og stund 