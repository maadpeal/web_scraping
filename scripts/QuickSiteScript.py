from scripts.GeneralClass import GeneralClass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import logging
import re


class QuickSiteScript(GeneralClass):

    def __init__(self):
        super().__init__()
        self.site = self.get_site_quick()
        self.log = super().setup_logger('QuickSiteScript', './logs/quick_site.log')

    def process(self):
        self.log.info('Iniciando proceso de QuickSiteScript')
        super().process()
        elements = self.page_content.select('.et_pb_row_8 a')
        href_list = [element['href'] for element in elements if element.has_attr('href')]
        page_content_dict = self.get_brands_page(href_list)
        devices_urls = self.process_devices(page_content_dict)
        devices_page = self.get_devices_page(devices_urls)
        self.write_csv(devices_page)
        return 'QuickSiteScript terminado'

    def get_brands_page(self, href_list):
        self.log.info('Obteniendo páginas de marcas')
        out = {}
        for href in href_list:
            page_content = self.get_site(href)
            out[href] = page_content
        return out

    def process_devices(self, page_content_dict):
        self.log.info('Procesando páginas de marcas')
        out = {}
        pattern = re.compile(r'/items/[\w]+/?')
        for key, page in page_content_dict.items():
            elements = page.select('.searchresult_cardContainer__m4c8x a')
            base_path = re.sub(pattern, '', key)
            out[key] = [base_path + element['href'] for element in elements if element.has_attr('href')]
        return out

    def get_devices_page(self, devices_urls):
        self.log.info('Obteniendo páginas de dispositivos')
        out = {}
        for key, urls in devices_urls.items():
            out[key] = {}
            driver = webdriver.Chrome()
            for url in urls:
                if 'contactanos' in url:
                    continue
                try:
                    driver.get(url)
                    wait = WebDriverWait(driver, 10)
                    buttons = wait.until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'pdp_pdpBuyButton__R4uEw')))
                    self.log.info(url + ' ok')
                except Exception as e:
                    self.log.error('error: ' + url)
                    self.log.error(e)
                    continue
                prices = {}
                for button in buttons:
                    try:
                        button.click()
                        price_element = wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//div[@class="pdp_serviceDescriptionCard__jJ6Dx"]//strong')))
                        price_text = price_element.text
                        prices[button.text] = price_text
                    except Exception as e:
                        self.log.error('error: ' + url)
                        self.log.error(e)
                        driver.quit()
                        continue
                self.log.info(prices)
                out[key][url] = prices
            driver.quit()
        return out

    def write_csv(self, devices_page):
        self.log.info('Escribiendo archivo csv')
        df = pd.DataFrame([], columns=['brand', 'device', 'price_type', 'price'])
        for key, content in devices_page.items():
            brand = key.split('/')[-1]
            for key_device, content_device in content.items():
                device = key_device.split('/')[-1]
                for key_price, price in content_device.items():
                    df.loc[len(df)] = [brand, device, key_price, price]
        df.to_csv('./csv/quick_prices.csv', index=False)
