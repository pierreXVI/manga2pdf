import io
import re

import PIL.Image
import lxml.etree
import requests

import manga_downloader
import utils

URL_0 = "https://readmanganato.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}


class Manganato(manga_downloader.MangaDownloader):
    @staticmethod
    def get_title(root_url):
        """
        :rtype: str
        :param str root_url:
        """
        root = lxml.etree.HTML(requests.get(root_url, headers=HEADERS).text)
        return root.find('.//*[@class="story-info-right"]')[0].text

    @staticmethod
    def get_chapter_list(root_url):
        """
        :rtype: list
        :param str root_url:
        """
        root = lxml.etree.HTML(requests.get(root_url, headers=HEADERS).text)
        return root.findall('.//*[@class="row-content-chapter"]/*a')[::-1]

    @staticmethod
    def get_chapter_number(chapter):
        """
        :rtype: int
        :param str chapter:
        """
        return int(re.findall(r'Chapter (\d+)', chapter)[0])

    @staticmethod
    def get_chapter(chapter_url):
        """
        :rtype: list
        :param str chapter_url:
        """
        images = []
        root = lxml.etree.HTML(requests.get(chapter_url, headers=HEADERS).text)
        urls = [data.attrib['src'] for data in root.findall('.//*[@class="container-chapter-reader"]/img')]
        title = root.find('.//*[@class="panel-chapter-info-top"]/h1').text

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

    def get_manga(self, url, bounds=None):
        super(Manganato, self).get_manga(URL_0 + url, bounds)


if __name__ == '__main__':
    Manganato().get_manga('manga-aa951409', (401, 500))
    # Manganato().get_manga('manga-id957386', (1, 100))
