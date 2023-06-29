import re
import os

from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By


SELENIUM_IP = os.environ['SELENIUM_IP']
SELENIUM_PORT = os.environ['SELENIUM_PORT']


def shop_getter_factory(link) -> dict:
    """
    Constructs a specific class depending on the given link.
    """
    shop = re.match(r'(https?://)?(w{3}\.)?([\w-]+)(.+)', link).group(3)

    getters = {
        'mvideo': Mvideo,
        'dns-shop': Dns,
        'citilink': Citilink,
    }

    return getters.get(shop, Getter)().get_info(link)


class Getter:
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--headless=chrome')
    options.add_argument('--window-size=2560,1440')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-blink-features=AutomationControlled')

    def get_info(self, link: str):
        """
        Returns title, description and rating of a good by the given link.
        """
        return {'error_code': 99, 'status_code': 500,
                'result': f'The method for class {self.__class__.__name__} is not implemented.'}


class Mvideo(Getter):
    title_xpath = '//h1[@itemprop="name"]'
    description_xpath = '//div[contains(@class, "text-container-inner") and contains(@class, "with-overflow")]'
    rating_link_xpath = '//a[contains(@class, "rating-reviews") and contains(@class, "ng-star-inserted")]'
    rating_xpath = '//span[contains(@class, "rating-value") and contains(@class, "medium")]'

    def get_info(self, link: str) -> dict:
        driver = webdriver.Remote(command_executor=f'{SELENIUM_IP}:{SELENIUM_PORT}', options=self.options)
        driver.implicitly_wait(5)

        try:
            driver.get(link)

            title = driver.find_element(By.XPATH, self.title_xpath).text

            description = driver.find_element(By.XPATH, self.description_xpath).text.replace('\n\n', ' ')

            rating_link = driver.find_element(By.XPATH, self.rating_link_xpath)
            rating_link.click()

            rating = driver.find_element(By.XPATH, self.rating_xpath).text

            return {'error_code': 0, 'result': {'title': title, 'description': description, 'rating': rating}}
        except NoSuchElementException:
            return {'error_code': 1, 'status_code': 400, 'result': 'A searched element has not been found.'}
        except WebDriverException:
            return {'error_code': 2, 'status_code': 500, 'result': 'The link is not valid or the connection is lost.'}
        finally:
            driver.quit()


class Dns(Getter):
    pass


class Citilink(Getter):
    pass
