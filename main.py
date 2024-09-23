import requests
from bs4 import BeautifulSoup
import pprint


def fetch_page_content(page_number):
    url = f"https://news.ycombinator.com/news?p={page_number}"
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise error for bad status codes
        return BeautifulSoup(res.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        return None


# Function to extract relevant data from a page
def extract_data(soup):
    if soup is None:
        return [], []
    links = soup.select(".titleline")
    subtext = soup.select(".subtext")
    return links, subtext


# Fetch and combine content from multiple pages
soup1 = fetch_page_content(1)
soup2 = fetch_page_content(2)
links1, subtext1 = extract_data(soup1)
links2, subtext2 = extract_data(soup2)

mega_links = links1 + links2
mega_subtext = subtext1 + subtext2


def sort_stories_by_votes(hn_list):
    return sorted(hn_list, key=lambda k: k["votes"], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.find("a").get("href")
        vote = subtext[index].select(".score")
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points > 99:
                hn.append({"title": title, "link": href, "votes": points})
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(mega_links, mega_subtext))
