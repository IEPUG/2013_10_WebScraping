#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
import re
import os


def get_detail_pages(url):

    req = requests.get(url)
    assert req.status_code == 200

    # root = req.request.url.replace(req.request.path_url, '')
    soup = BeautifulSoup(req.content)

    for link in soup.find_all('a', href=re.compile('/details/omni')):
        # get_item(''.join([root, link.get('href')]))
        get_item(urljoin(req.request.url, link.get('href')))


def get_item(url):
    req = requests.get(url)
    assert req.status_code == 200

    # root = req.request.url.replace(req.request.path_url, '')
    soup = BeautifulSoup(req.content)

    for link in soup.find_all('a', href=re.compile('/download/omni.*\.pdf\Z')):
        # pdf_link = ''.join([root, link.get('href')])
        pdf_link = urljoin(req.request.url, link.get('href'))
        print(pdf_link)
        pdfList.append(pdf_link)
        save_file(pdf_link)


def save_file(url):
    # SAVE_DIR = './OMNI'
    SAVE_DIR = 'OMNI'
    req = requests.get(url)
    fname = req.request.path_url.split('/')[-1]
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    # with open(''.join([SAVE_DIR, '/', fname]), "wb") as content:
    with open(os.path.join(SAVE_DIR, fname), "wb") as content:
        content.write(req.content)


def main():
    # info: http://archive.org/details/omni-magazine
    # info: http://omnireboot.com/

    url = 'http://archive.org/search.php?query=collection%3Aomni-magazine&sort=-publicdate'
    req = requests.get(url)

    assert req.status_code == 200

    soup = BeautifulSoup(req.content)

    # root = req.request.url.replace(req.request.path_url, '')

    all_page_links = []
    for page_link in soup.find_all('a', href=re.compile('page=.\Z')):
        # all_page_links.append(''.join([root, page_link.get('href')]))
        all_page_links.append(urljoin(req.request.url, page_link.get('href')))
    pages = set(all_page_links)

    get_detail_pages(url)  # process page 1
    for page in sorted(pages):
        get_detail_pages(page)  # get rest of pages


if __name__ == "__main__":
    pdfList = []
    main()
    print('PDF Count: {0}'.format(len(pdfList)))
    assert len(pdfList) == 196

