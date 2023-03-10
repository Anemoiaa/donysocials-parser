import time
import logging

from abc import ABCMeta, abstractmethod
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import settings


class LinkReaderFromSheetMixin:
    def get_links(self):
        arr = self.worksheet.col_values(1)
        return arr[1::]


class LinkWriterToSheetMixin:
    def write_col(self, data):
        self.worksheet.update_acell("A{}".format(self.next_row), data[0])
        self.worksheet.update_acell("B{}".format(self.next_row), data[1])


class Parser(LinkReaderFromSheetMixin, LinkWriterToSheetMixin):
    """
    Class description
    """
    __metaclass__ = ABCMeta

    selector: str = ''

    def __init__(self, driver, worksheet) -> None:
        self.driver = driver
        self.worksheet = worksheet
        self.links = self.get_links()
        self.next_row = 2

    @abstractmethod
    def string_transform_to_views_amount(self, text):
        pass

    def parse(self) -> None:
        for link in self.links:
            try:
                self.driver.get(url=link)
                content = WebDriverWait(self.driver, settings.PAGE_LOAD_WAITING_DELAY).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.selector))
                    )
                views = f'{self.string_transform_to_views_amount(content.text)}'
            except BaseException as e:
                logging.exception(e)
                views = f'Что-то пошло не так...'
            self.write_col([link, views])
            time.sleep(settings.DELAY)
            self.next_row += 1
        self.driver.quit()


class Tiktok(Parser):
    """
    Class description
    """

    selector = '[data-e2e=\'user-post-item-list\'] [data-e2e=\'video-views\']'

    def string_transform_to_views_amount(self, text):
        result = 0
        if 'K' in text:
            return int(float(text.split('K')[0]) * 1000)
        try:
            result = re.findall(r'\d+', text)[0]
        except IndexError:
            pass
        return result


class Youtube(Parser):
    """
    Class description
    """

    selector = '#contents #content #metadata-line span'

    def string_transform_to_views_amount(self, text):
        result = 0
        if 'K' in text:
            return int(float(text.split('K')[0]) * 1000)
        try:
            result = re.findall(r'\d+', text)[0]
        except IndexError:
            pass
        return result
