import traceback
from time import sleep

from selenium import webdriver

class DriverChrome:

    def __init__(self, link):
        self.link = link
        self.browser = webdriver.Chrome()
        self.browser.get(self.link)
        sleep(2)

    def get_cars(self):
        self.browser.refresh()
        sleep(10)

        cars_info = []

        div_car = self.browser.find_elements_by_css_selector('.iva-item-root-G3n7v')
        for car in div_car:
            car_info = {}
            div_title = car.find_element_by_css_selector('.iva-item-titleStep-2bjuh')
            car_info['title'] = div_title.find_element_by_tag_name('a').text

            mileage = car.find_element_by_css_selector('.iva-item-autoParamsStep-14Mv3')
            mileage = mileage.find_element_by_css_selector('div').text
            car_info['mileage'] = mileage

            try:
                img = car.find_element_by_css_selector('.photo-slider-image-1fpZZ')
                car_info['img'] = img.get_attribute('src')
            except:
                print(traceback.format_exc())

            cars_info.append(car_info)

        return cars_info

    def get_new_cars(self, last_car):

        cars_info = self.get_cars()

        cars_new = []
        for i, car in enumerate(cars_info):
            if last_car['title'] == car['title'] and last_car['mileage'] == car['mileage']:
                break
            else:
                cars_new.append(car)
            if i == (len(cars_info) - 1):
                cars_new.clear()
                print('Не нашло - ' + last_car['title'])

        new_last_car = cars_info[0]

        return new_last_car, cars_new

