import traceback
from time import sleep
import random

from vk_api.longpoll import VkEventType

from Config import Config
from DriverChrome import DriverChrome
from Vk import Vk


browser = DriverChrome(Config.link)
vk = Vk()

for event in vk.longPoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            if msg == 'авито':
                vk.send_msg(user_id, 'Началось отслеживание новых объявлений по ссылке - ' + Config.link)

                last_car = {
                    'title': '',
                    'mileage': '',
                    'img': ''}
                while True:
                    try:
                        last_car, cars_new = browser.get_new_cars(last_car)

                        if len(cars_new) == 1:
                            # print('Добавилась машина - ', cars_new[0])
                            msg = 'Добавилась машина - ' + cars_new[0]['title'] + '\n' + cars_new[0]['mileage']
                            vk.send_msg_and_photo(user_id, msg, cars_new[0]['img'])

                        elif len(cars_new) > 1:
                            # print('Добавились машины:')
                            vk.send_msg(user_id, '------------')
                            vk.send_msg(user_id, 'Добавились машины:')

                            for car in cars_new:
                                # print(car)
                                msg = car['title'] + '\n' + car['mileage']
                                vk.send_msg_and_photo(user_id, msg, car['img'])

                            vk.send_msg(user_id, '------------')

                    except Exception:
                        print('Error:\n', traceback.format_exc())
                        print('Продолжение отслеживания..')

                    sleep(random.triangular(5, 10, 10))
