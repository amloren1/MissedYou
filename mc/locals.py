import requests
from bs4 import BeautifulSoup

URL = "https://www.craigslist.org/about/sites"


def get_city_links(state="Arizona"):
    r = requests.get(URL)

    # parse html
    soup = BeautifulSoup(r.text, "html.parser")

    # find all links
    links = soup.find_all("a", {"class": "result-title hdrlnk"})

    # find links for each state heading
    states = soup.find_all("h4")
    for state in states:
        print(state.text)
        # get all links in state
        state_links = state.find_next_sibling().find_all("a")
        for state_link in state_links:
            print(state_link.get("href"))
