from scripts.GeneralClass import GeneralClass
import logging
import csv


class PhoneSiteScript(GeneralClass):

    def __init__(self):
        super().__init__()
        self.site = self.get_site_phone()
        self.log = super().setup_logger('PhoneSiteScript', './logs/phone_site.log')

    def process(self):
        self.log.info('Iniciando proceso de PhoneSiteScript')
        super().process()
        self.write_csv([], "", "", True)
        list_brands = self.get_list_elements(self.page_content)

        for brand in list_brands:
            page_brand = self.get_site(list_brands[brand])
            list_models = self.get_list_elements(page_brand)
            for model in list_models:
                self.log.info(model)
                page_model = self.get_site(list_models[model])
                list_devices = self.get_list_elements(page_model)
                for service in list_devices:
                    self.log.info(service)
                    page_services = self.get_site(list_devices[service])
                    if page_services:
                        list_services = self.get_list_services(page_services)
                        self.write_csv(list_services, brand, model)
                    else:
                        self.write_csv([{'price': 0, 'title': None}], brand, model)
        return 'PhoneSiteScript terminado'

    def get_list_elements(self, soup, class_="transition"):
        self.log.info('Obteniendo lista de elementos')
        if not soup:
            return []
        elements = soup.find_all('a', class_=class_)
        list_brands = {}
        for element in elements:
            try:
                text = ' '.join(element['title'].split(' ')[1:]) if element['title'] else []
                href = element['href']
                list_brands[text] = href
            except KeyError as e:
                self.log.error("No se encontró el atributo: " + str(e) + " en el elemento: " + str(element))
        return list_brands

    def get_list_services(self, page_services):
        self.log.info('Obteniendo lista de servicios')
        list_reparacion_items = page_services.select('.list-reparacion li')
        data = []
        for li_item in list_reparacion_items:
            li_data = {}
            input_element = li_item.find('input', type='checkbox')
            if input_element and 'data-price' in input_element.attrs:
                li_data['price'] = input_element['data-price']
            title_element = li_item.find('p', class_='title')
            if title_element:
                title = title_element.get_text(strip=True)
                li_data['title'] = title.replace('Reparar', '').strip()
            data.append(li_data)
        return data

    def write_csv(self, list_services, brand, model, first=False):
        self.log.info('Escribiendo csv')
        if first:
            with open('./csv/mundo_movil_precios.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["servicio", "precio", "marca", "modelo"])
        else:
            with open('./csv/mundo_movil_precios.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                for row in list_services:
                    brand = brand.replace('Reparar ', '').strip()
                    result_list = [row['price'], row['title']] + [brand, model]
                    csvwriter.writerow(result_list)
