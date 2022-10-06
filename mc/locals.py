import requests
from bs4 import BeautifulSoup

from const import SITES_URL


def get_city_links(locals: list =["Arizona"]):
    
    r = requests.get(SITES_URL)

    # parse html
    soup = BeautifulSoup(r.text, "html.parser")

    # find all links
    links = soup.find_all("a", {"class": "result-title hdrlnk"})
    # find links for each state heading
    states = soup.find_all("h4")
    city_links = []
    for state in states:
        if state.text in locals:
            # print(state.text)
            # get all links in state
            state_links = state.find_next_sibling().find_all("a")

            for state_link in state_links:
                print(state_link.get("href"))
                print(state_link.text)
                city_links.append(state_link.get("href"))
    return city_links


get_city_links()