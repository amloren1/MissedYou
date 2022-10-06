"""
Simple webscraper using beautiful soup


"""
# Import modules


from bs4 import BeautifulSoup
import os
import requests
import sys

import time

from const import US_STATES, VPN
from locals import get_city_links

# # read in craigs_list.txt
# with open("craigs_list.txt", "r") as f:
#     # read in the lines
#     locations = f.readlines()
#     f.close()


class Scrapper:
    def __init__(self, locations=US_STATES) -> None:
        pass

        # craigslist missed connections base url. format
        self.url_path = "{}/search/mis"
        self.locations = locations
        self.city_links = get_city_links(locations)

    def _get_page_main_text_body(self, url):
        """
        Get the main text body of the page
        """
        # Get the page
        page = requests.get(url)
        # Parse the page
        soup = BeautifulSoup(page.content, "html.parser")
        # Get the main text body
        main_text_body = soup.find(id="postingbody")

        # get only the text
        try:
            main_text_body = main_text_body.text
            main_text_body = main_text_body.split("\n")[-2]
        except AttributeError:
            if soup.find("h2"):
                if "flagged" in soup.find("h2").text:
                    main_text_body = "Post Flagged"
            elif soup.find("title"):
                if soup.find("title").text == "blocked":
                    main_text_body = "Post Deleted"
                    print("BLOCKED: Changing VPN connection")
                    if VPN:
                        os.system("protonvpn-cli c -r")
                        time.sleep(2)
                        main_text_body = self._get_page_main_text_body(url)

                    else:
                        sys.exit()
            else:
                print("\n\n Not sure what happened here. Bye")
                sys.exit()

        # Return the main text body
        return main_text_body

    def get_location_urls(self):
        get_city_links(self.locations)
        pass

    def write_line_to_file(self, line):
        """
        Write a line to a file
        """
        with open("res.txt", "a") as f:
            f.write(f"\n{line[0]}\t|\t{line[1]}")
            f.close()

    def write_lines_to_file(self, lines: list):
        """
        Write a line to a file
        """
        with open("res.txt", "a") as f:
            for line in lines:
                f.write(f"\n{line[0]}\t|\t{line[1]}")
        f.close()

    def get_posts(self):
        for locale in self.city_links:
            # add base to url path
            url = self.url_path.format(locale)
            print(url)
            while True:
                # request base url for search result
                r = requests.get(url)

                # parse html
                soup = BeautifulSoup(r.text, "html.parser")

                # find all links
                links = soup.find_all("a", {"class": "result-title hdrlnk"})

                # extract next page link
                next_page = soup.find("a", {"title": "next page"})
                if next_page:
                    next_page_link = next_page.get("href", None)

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

                    # skip current and further links if not the correct base url
                    if locale not in link_url:
                        break

                    print(self._get_page_main_text_body(link_url))
                    texts.append((link_text, self._get_page_main_text_body(link_url)))

                    print("")

                # if next page link exists
                if next_page_link:
                    # set base url to next page link
                    base_url = next_page_link
                else:
                    self.write_lines_to_file(texts)
                    texts = None
                    break
