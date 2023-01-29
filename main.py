from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import gspread

from SocialParser import Tiktok, Youtube
from config import  settings
pre = {1: Tiktok, 2:Youtube }


def main() -> None:
    social_media = int(input('Что парсим:\n1.Tiktok\n2.YoutTube\nВвод:'))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    gc = gspread.service_account(filename=settings.SERVICE_ACCOUNT)
    wrk = gc.open(settings.SHEET_NAME).sheet1
    parser = pre[social_media](driver, wrk)
    parser.parse()


if __name__ == '__main__':
    main()

