import urllib
import urllib.request
from bs4 import BeautifulSoup
import os

def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata

soup = make_soup("https://www.realclearpolitics.com/epolls/2020/president/us/2020_democratic_presidential_nomination-6730.html")

spread_data_saved = ""
for record in soup.findAll('tr'):
    spread_data = ""
    for data in record.findAll('td'):
        spread_data = spread_data + "," + data.text
    if len(spread_data) != 0:
        spread_data_saved = spread_data_saved + "\n" + spread_data[1:]


header = "Poll,Date,Sample,Biden,Sanders,Warren,Bloomberg,Buttigieg,Klobuchar,Yang,Stayer,Gabbard,Bennet,Patrick,Spread"
file = open(os.path.expanduser("Polls.csv"), "wb")
file.write(bytes(header, encoding="ascii", errors='ignore'))
file.write(bytes(spread_data_saved, encoding="ascii", errors='ignore'))

