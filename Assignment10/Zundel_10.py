# Modify the previous program to randomly choose a few links from among the list of clean links, then retrieve and print to screen the text on those few webpages.
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse
import random
import justext
import re

def get_links(anchors):
    links = []
    for anchor in anchors:
        try:
            links.append(anchor.attrs['href'])
        except KeyError:
            print("skipping this anchor because it doesn't have an href attribute")

    links = [l for l in links if len(l) > 0 and l[0] != '#']
    return list(set(links))

def get_absolute_path_link(url, relative_link):
    parsed_url = urllib.parse.urlparse(url)
    return urllib.parse.urljoin(parsed_url.scheme + "://" + parsed_url.netloc, relative_link)

def write_to_file(current_url, scraped_text):
    # Get rid of the first part of the link
    current_url = re.sub('https?[\:]//', '', current_url)
    current_url = re.sub('/', ' ', current_url)

    # Some links exceeded the max length for a file name
    if len(current_url) > 100:
        current_url = current_url[:100]
    with open(f'{current_url}.txt', 'w') as outfile:
        for text in scraped_text:
            outfile.write(f'{text}\n')

def web_crawl(links):
    # Var to keep track of sites with non-boilerplate text
    sites_visited = 0
    for link in links:
        if 'octoparse' in link:  # Always takes a long time and never gets a response
            continue
        try:
            response = requests.get(link, headers=headers)
        except:
            print('Something happened')
            continue

        # Parsing out the content
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
        # Filters out any non-boilerplate text
        scraped_text = [p.text for p in paragraphs if not p.is_boilerplate]

        # Only writing files that have content
        if len(scraped_text) > 0:
            write_to_file(link, scraped_text)
            sites_visited += 1

        # Limit writing to files to 10 .txt files
        if sites_visited > 10:
            break

if __name__ == '__main__':
    url = 'https://medium.com/@dan_21864/best-web-scraping-tools-apis-and-frameworks-655cb71944fe'
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = bs(response.content, "html.parser")
    anchors = soup.find_all("a")

    # Gets all the unique links and removes any site specific links
    links = get_links(anchors)

    # Changes all links to an absolute path
    links = [get_absolute_path_link(url, l) for l in links]

    random.shuffle(links) # modifies in place!

    # Crawl through all the links
    web_crawl(links)