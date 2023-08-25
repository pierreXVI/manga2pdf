import io
import re

import PIL.Image
import lxml.etree
import requests

import manga_downloader
import utils

URL_0 = "https://full-metal-alchemist.online/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}


class FMAOnline(manga_downloader.MangaDownloader):
    @staticmethod
    def get_title(root_url):
        return "Full Metal Alchemist"

    @staticmethod
    def get_chapter_list(root_url):
        root = lxml.etree.HTML(requests.get(root_url, headers=HEADERS).text)
        return [chapter[0] for chapter in root.findall('.//*[@id="Chapters_List"]/ul/li/ul/li')[::-1]]

    @staticmethod
    def get_chapter_number(chapter):
        return re.findall(r'Chapter (\d+(\.\d+)?)', chapter)[0]

    @staticmethod
    def get_chapter(chapter_url):
        images = []
        root = lxml.etree.HTML(requests.get(chapter_url, headers=HEADERS).text)
        urls = [data.attrib['data-lazy-src'] for data in root.findall('.//*[@class="entry-content"]/div/a/img')]
        title = root.find('.//*[@class="entry-title"]').text

        count = utils.Counter(title, len(urls))
        for i in range(len(urls)):
            response = requests.get(urls[i], headers={**HEADERS, 'referer': chapter_url})
            if not response:
                raise ConnectionError("Cannot get image from url \"{0}\"".format(response.url))

            img = PIL.Image.open(io.BytesIO(response.content))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
            count(i)

        return images


if __name__ == '__main__':
    FMAOnline().get_manga(URL_0)
