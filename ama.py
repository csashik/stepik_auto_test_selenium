from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from tqdm import tqdm
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
# from fake_useragent import UserAgent
from exp import lst, ls
import random


def steps(heght, min_max=[50, 150], down =True):
    lst = []
    if not down:
        min_max = [500, 800]
    while heght>0:
        step = random.randint(min_max[0], min_max[-1])
        lst += [step]
        heght -= step
    return lst

# url = 'https://yandex.ru'
# url = 'https://www.wildberries.ru/'
# url = 'https://www.browserscan.net/ru/bot-detection'
url = 'https://www.amazon.ca/'
items = {'bread maker': ['Neretva Bread Maker, 20-in-1 2LB Bread Machine', 'B0C9SY6R4H']} #[data-asin="B0BHYZ1KH7"]
ran = 1
login = 'alex.sem.test.01@gmail.com'

chrome_options = webdriver.ChromeOptions()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument('--force-device-scale-factor=1.25')
# chrome_options.add_argument('--headless')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('--disable-infobars')
# chrome_options.add_argument(f'user-agent={UserAgent('Chrome').random}')
tst = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={tst}')
with (webdriver.Chrome(options=chrome_options) as browser):
    #part1 acces to the web /stetik account
    actions = ActionChains(browser)
    browser.implicitly_wait(10)
    WW = WDW(browser, 45, 0.2)
    WW2 = WDW(browser, 1, 0.3)
    browser.get(url)
    time.sleep(0.5)
    [browser.add_cookie(i) for i in ls]
    time.sleep(0.5)
    browser.get(url)
    # input()
    # ls = browser.get_cookies()
    # print(ls)
    for item in items:
        browser.find_element('css selector', 'input#twotabsearchtextbox').send_keys(item)
        # time.sleep(0.5)
        browser.find_element('css selector', 'input#nav-search-submit-button').click()
        # height = browser.execute_script("return document.body.scrollHeight")
        # print(height)
        # n = steps(height)
        # [actions.scroll_by_amount(0, i).pause(random.uniform(0.2, 0.7)).perform() for i in n]
        # time.sleep(3)
        # n = steps(height, down=False)
        # [actions.scroll_by_amount(0, -i).pause(random.uniform(0.1, 0.4)).perform() for i in n]
        elms = browser.find_elements('css selector', '[role="listitem"][data-asin][data-index]') # a.a-link-normal.s-no-outline[href]
        links = [i.find_element('css selector','a.a-link-normal.s-no-outline[href]').get_attribute('href') for i in elms]
        tg = [i.find_element('css selector', 'a.a-link-normal.s-no-outline[href]').get_attribute('href') for i in elms if
              i.get_attribute('data-asin')==items[item][-1]]
        # names = [i.find_element('css selector', 'span').text for i in elms]
        # elms2 = browser.find_elements('css selector','[role="listitem"] div a h2 span')
        # names = [i.text for i in elms2]
        main_url = browser.current_url
        for _ in range(ran):
            browser.get(links[random.randint(0, len(links))])
            time.sleep(1)
            imgs = browser.find_elements('css selector','img[alt="Product Image"]')
            [actions.move_to_element(i).pause(2).perform() for i in imgs]
            # browser.back()
            time.sleep(1)
            browser.get(main_url)
            time.sleep(0.5)
        browser.get(tg[0])
        try:
            browser.find_element('css selector', '#newAccordionRow_1 i.a-icon.a-accordion-radio').click()
        except:
            continue
        time.sleep(2)
        cart = browser.find_element('css selector', 'span #add-to-cart-button')
        browser.execute_script('arguments[0].click()', cart)
        actions.move_to_element(cart).pause(0.5).click().perform()
        time.sleep(0.5)
        # alrt = browser.switch_to.alert
        # alrt.dismiss()
        browser.find_element('css selector', '#attachSiNoCoverage input').click()

    [print(i) for i in tg]
    print(len(tg))

    input()
