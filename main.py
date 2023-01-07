from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from SocialParser import Tiktok, Youtube

pre = {1: Tiktok, 2:Youtube }

def main() -> None:
    social_media = int(input('Что парсим:\n1.Tiktok\n2.YoutTube\nВвод:'))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    parser = pre[social_media](driver)
    parser.parse()
    parser.write_results()

if __name__ == '__main__':
    main()

