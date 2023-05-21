import time
from selenium import webdriver

def make_screen_bubbles():
    url = 'https://cryptobubbles.net/'
    filename = 'bot/source/bubbles.png'
    width = 1920
    height = 1080

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument(f'window-size={width},{height}')
    options.add_argument('hide-scrollbars')

    browser = webdriver.Chrome(options=options)
    browser.get(url)
    # browser.find_element("xpath", '/html/body/div/main/div[1]/div/button[1]').click()
    time.sleep(3)
    # browser.find_element("xpath", '/html/body/div/main/div[1]/div[2]/section/div/fieldset[1]/button[4]').click()
    # time.sleep(0.1)
    # browser.find_element("xpath", '/html/body/div/main/div[1]/div[2]/section/header/button[3]').click()
    # time.sleep(7)
    browser.save_screenshot(filename)