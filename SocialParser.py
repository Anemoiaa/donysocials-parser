import time
import logging

from abc import ABCMeta, abstractmethod

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import settings


class LinkReaderMixin:
    def get_links(self, filename: str = settings.INPUT_FILE_NAME):
        with open(filename, 'r') as f:
            return f.readlines()


class LinkWriterToSheetMixin:
    def next_available_row(self):
        str_list = list(filter(None, self.worksheet.col_values(1)))
        return str(len(str_list) + 1)

    def write_col(self, data):
        self.worksheet.update_acell("A{}".format(self.next_row), data[0])
        self.worksheet.update_acell("B{}".format(self.next_row), data[1])


class Parser(LinkReaderMixin, LinkWriterToSheetMixin):
    """
    Class description
    """
    __metaclass__ = ABCMeta

    selector: str = ''

    def __init__(self, driver, worksheet) -> None:
        self.driver = driver
        self.links = self.get_links()
        self.worksheet = worksheet
        self.next_row = self.next_available_row()

    @abstractmethod
    def text_transform(self, text):
        pass

    def parse(self) -> None:
        for link in self.links:
            try:
                self.driver.get(url=link)
                content = WebDriverWait(self.driver, settings.PAGE_LOAD_WAITING_DELAY).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.selector))
                    )
                views = f'{self.text_transform(content.text)}\n'
            except BaseException as e:
                logging.exception(e)
                views = f'Что-то пошло не так...\n'
            self.write_col([link, views])
            time.sleep(settings.DELAY)
        self.driver.quit()


class Tiktok(Parser):
    """
    Class description
    """

    selector = '[data-e2e=\'user-post-item-list\'] [data-e2e=\'video-views\']'

    def text_transform(self, text):
        return text


class Youtube(Parser):
    """
    Class description
    """

    selector = '#contents #content #metadata-line span'

    def text_transform(self, text):
        is_rus = text.find('про')
        if is_rus != -1:
            return text[0: is_rus]
        else:
            eng = text.find('vie')
            return text[0: eng]
