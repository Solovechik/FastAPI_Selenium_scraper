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
        'citilink': Mvideo,
    }

    return getters.get(shop, Getter)().get_price(link)


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

    def get_price(self, link: str):
        """
        Returns a price of a good by the given link.
        """
        return {'error_code': 99, 'status_code': 500,
                'result': f'The method for class {self.__class__.__name__} is not implemented.'}


class Mvideo(Getter):
    price_xpath = '//mvideoru-product-details-card//span[contains(@class, "price__main-value")]'

    def get_price(self, link: str) -> dict:
        driver = webdriver.Remote(command_executor=f'{SELENIUM_IP}:{SELENIUM_PORT}', options=self.options)
        driver.implicitly_wait(5)

        try:
            driver.get(link)

            price = driver.find_element(By.XPATH, self.price_xpath).text

            return {'error_code': 0, 'result': float(price[:-1].replace(' ', ''))}
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
