
'''
Possible solutions to in-class practice exercises
for Lesson 11.1
about webscraping
'''
# Create a program that webscrapes a blog of your choice and print the text to the screen.
import justext, requests
url = "https://www.r-bloggers.com/"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
response = requests.get(url, headers=headers)
paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
for paragraph in paragraphs:
    if not paragraph.is_boilerplate:
        print(paragraph.text)
# Modify the previous program to save the text to a .txt file on your hard drive.
import justext, requests
url = "https://www.r-bloggers.com/"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
response = requests.get(url, headers=headers)
paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
with open("webscrape_text.txt", mode='w') as outfile:
    outfile.write(url + '\n')
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            outfile.write(paragraph.text + '\n')
# Create a program that prints to screen the links on a webpage, that is, the URLs within the href attribute of anchor tags <a>.
import requests
from bs4 import BeautifulSoup as bs
url = "https://www.r-bloggers.com"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
response = requests.get(url, headers=headers)
soup = bs(response.content, "html.parser")
anchors = soup.find_all("a")
links = []
for anchor in anchors:
    try:
        links.append(anchor.attrs['href'])
    except KeyError:
        print("skipping this anchor because it doesn't have an href attribute")
print(links)
# Modify the previous program to clean up the links
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse
url = "https://www.r-bloggers.com"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
response = requests.get(url, headers=headers)
soup = bs(response.content, "html.parser")
anchors = soup.find_all("a")
links = []
for anchor in anchors:
    try:
        links.append(anchor.attrs['href'])
    except KeyError:
        print("skipping this anchor because it doesn't have an href attribute")
links = [l for l in links if len(l) > 0]
links = set(links)
links = [l for l in links if l[0] != "#"]
def get_absolute_path_link(url, relative_link):
    parsed_url = urllib.parse.urlparse(url)
    return urllib.parse.urljoin(parsed_url.scheme + "://" + parsed_url.netloc, relative_link)

links = [get_absolute_path_link(url, l) for l in links]
print(links)
# Modify the previous program to randomly choose a few links from among the list of clean links, then retrieve and print to screen the text on those few webpages.
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse
import random
import justext
url = "https://www.r-bloggers.com"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
response = requests.get(url, headers=headers)
soup = bs(response.content, "html.parser")
anchors = soup.find_all("a")
links = []
for anchor in anchors:
    try:
        links.append(anchor.attrs['href'])
    except KeyError:
        print("skipping this anchor because it doesn't have an href attribute")
links = [l for l in links if len(l) > 0]
links = set(links)
links = [l for l in links if l[0] != "#"]
def get_absolute_path_link(url, relative_link):
    parsed_url = urllib.parse.urlparse(url)
    return urllib.parse.urljoin(parsed_url.scheme + "://" + parsed_url.netloc, relative_link)

links = [get_absolute_path_link(url, l) for l in links]
random.shuffle(links) # modifies in place!
num_links = 2
if len(links) < num_links:
    num_links = len(links)
for i in range(num_links):
    current_url = links[i]
    try:
        response = requests.get(current_url, headers=headers)
    except:
        continue

    paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            print(paragraph.text)
