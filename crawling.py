import re
import requests
from http.client import RemoteDisconnected
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def expand_document_with_crawled_data(doc_content: str) -> str:

    document_included_urls = __extractURLs(doc_content)
    if len(document_included_urls) > 0:
        for url in document_included_urls:
            crawled_text = __crawl(url)
            doc_content +=" "+ crawled_text
    # return f"{doc_content} {crawled_text}"
    return doc_content


def __extractURLs(content):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    return urls



def __is_text_url(url):
    # send a HEAD request to the URL to retrieve the headers
    response = requests.head(url)

    # check the Content-Type and Content-Disposition headers
    content_type = response.headers['Content-Type']
    content_disposition = response.headers.get('Content-Disposition', '')
    if 'text' in content_type and 'attachment' not in content_disposition:
        # check the file extension of the URL
        resource = urlparse(url).path
        file_extension = resource.split('.')[-1]
        # array of common text files extensions
        text_file_extensions = ['txt', 'html', 'htm', 'xml', 'csv', 'json', 'md', 'rst', 'php', 'asp', 'aspx', 'css',
                                'js', 'py', 'rb', 'java', 'c', 'cpp', 'h', 'sh', 'bat', 'log', 'ini', 'conf', 'yml',
                                'yaml']
        if file_extension in text_file_extensions:
            return True

        # download a small portion of the response and check its contents
        response = requests.get(url, stream=True)
        content = response.raw.read(1024)
        if all(32 <= c < 127 or c in (9, 10, 13) for c in content):
            return True

    return False


def __crawl(url)->str:
    try:
        if __is_text_url(url):
            print(f"crawling {url}")
            html = urlopen(url).read()
            soup = BeautifulSoup(html, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out

            # get text
            text = soup.get_text()

            # ###### some text processing #######
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text
        else:
            return ' '
    except (HTTPError, URLError, RemoteDisconnected) as e:
        return ' '
    except Exception as e:
        return ' '


__all__ = ['expand_document_with_crawled_data']