import os
import subprocess

OUTPUT_FILE = 'Library'
TMP_FILE = 'tmp'


class MangaDownloader:
    @staticmethod
    def get_title(root_url):
        """
        :rtype: str
        :param str root_url:
        """
        raise NotImplementedError

    @staticmethod
    def get_chapter_list(root_url):
        """
        :rtype: list
        :param str root_url:
        """
        raise NotImplementedError

    @staticmethod
    def get_chapter_number(chapter):
        """
        :rtype: int or str
        :param str chapter:
        """
        raise NotImplementedError

    @staticmethod
    def get_chapter(chapter_url):
        """
        :rtype: list
        :param str chapter_url:
        """
        raise NotImplementedError

    def get_manga(self, root_url, bounds=None):
        title = self.get_title(root_url)
        chapter_list = self.get_chapter_list(root_url)

        os.makedirs(os.path.join(TMP_FILE, title), exist_ok=True)
        os.makedirs(os.path.join(TMP_FILE, 'tmp', title), exist_ok=True)

        chapter_done, n_chapter_done = [], []

        for i in range(len(chapter_list)):
            try:
                n_chap = self.get_chapter_number(chapter_list[i].text)
            except IndexError:
                continue
            if n_chap in n_chapter_done or (bounds and not bounds[0] <= n_chap <= bounds[1]):
                continue

            filename = os.path.join(TMP_FILE, title, chapter_list[i].text + '.pdf')
            filename_tmp = os.path.join(TMP_FILE, 'tmp', title, chapter_list[i].text + '.pdf')

            if not os.path.isfile(filename):
                if not os.path.isfile(filename_tmp):
                    img = self.get_chapter(chapter_list[i].attrib['href'])
                    if not img:
                        continue
                    img[0].save(filename_tmp, "PDF", title=chapter_list[i].text, save_all=True, append_images=img[1:])

                if not subprocess.run(
                        ['gs', '-o', filename.replace('%', '%%'), '-q', '-sDEVICE=pdfwrite', filename_tmp, '-c',
                         '[/Page 1 /View [/XYZ null null null] /Title ({0}) /OUT pdfmark'.format(chapter_list[i].text)
                         ]).returncode:
                    os.remove(filename_tmp)
                else:
                    exit()

            chapter_done.append(filename)
            n_chapter_done.append(n_chap)

        if bounds:
            title = '{0} {1}-{2}'.format(title, *bounds)
        subprocess.call(['gs', '-o', os.path.join(OUTPUT_FILE, title + '.pdf'), '-q', '-sDEVICE=pdfwrite',
                         *chapter_done, '-c', '[ /Title ({0}) /DOCINFO pdfmark'.format(title)])
