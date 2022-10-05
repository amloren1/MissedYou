"""
Simple webscraper using beautiful soup


"""
# Import modules
import requests
from bs4 import BeautifulSoup
import re
import os
import sys

import time

# read in craigs_list.txt
with open('craigs_list.txt', 'r') as f:
    # read in the lines
    locations = f.readlines()
    f.close()

# craigslist phoenix missed connections base url
base_url = "https://{}.craigslist.org/search/mis"


def get_page_main_text_body(url):
    """
    Get the main text body of the page
    """
    # Get the page
    page = requests.get(url)
    # Parse the page
    soup = BeautifulSoup(page.content, 'html.parser')
    # Get the main text body
    main_text_body = soup.find(id="postingbody")

    # get only the text
    main_text_body = main_text_body.text
    # Return the main text body
    return main_text_body.split('\n')[-2]

for locale in locations:
    base_url = base_url.format(locale.strip())

    while True:
        # request base url for search result
        r = requests.get(base_url)

        # parse html
        soup = BeautifulSoup(r.text, "html.parser")

        # find all links
        links = soup.find_all("a", {"class": "result-title hdrlnk"})

        # extract next page link
        next_page = soup.find("a", {"title": "next page"})
        if next_page:
            next_page_link = next_page.get("href", None )

        texts = []
        # find all links in search result
        for link in links:
            # get link text
            link_text = link.text
            # get link url
            link_url = link.get("href")
            # print link text and url
            print(link_text)
            print(link_url)
            # breakpoint()
            # store body text to file next line

            # use asyncio to append the
            # body text to the file
            # store text asynchronously
       
            # with open('res.txt', 'a') as f:
            #     f.write(get_page_main_text_body(link_url))
            #     f.write('\n')
            #     f.close()
            
            print(get_page_main_text_body(link_url))
            texts.append(get_page_main_text_body(link_url))
            # request link url
            # r = requests.get(link_url)
            # parse html and return the main text
            
            # # for p_tag in p_tags:
            # #     # get p tag text
            # #     p_tag_text = p_tag.text
            # #     # print p tag text
            # #     print(p_tag_text)
            
            print("")
            # time.sleep(5)

        # if next page link exists
        if next_page_link:
            # set base url to next page link
            base_url = next_page_link
        else:
            # exit
            with open('res.txt', 'a') as f:
                f.write('\n\n'.join(texts))
                f.close()
            texts = None
            break