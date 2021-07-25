import os
import requests

import vk_api
from vk_api.longpoll import VkLongPoll

from Config import Config


class Vk:

    def __init__(self):
        self.vk_session = vk_api.VkApi(token=Config.vk_token)
        self.longPoll = VkLongPoll(self.vk_session)

        VkLongPoll(self.vk_session)

    def send_msg(self, user_id, msg):
        self.vk_session.method('messages.send', {
            'user_id': user_id,
            'message': str(msg),
            'random_id': 0
        })

    def send_msg_and_photo(self, user_id, msg, link_photo):
        try:
            photo_response = requests.get(link_photo)
            filename = link_photo.split('/')[-1]
            open(filename, 'wb').write(photo_response.content)

            uploader = vk_api.upload.VkUpload(self.vk_session)
            img = uploader.photo_messages(filename)
            media_id = img[0]['id']
            owner_id = img[0]['owner_id']

            self.vk_session.method('messages.send', {
                'user_id': user_id,
                'message': msg,
                'attachment': 'photo' + str(owner_id) + '_' + str(media_id),
                'random_id': 0})

            os.remove(filename)
        except Exception:
            uploader = vk_api.upload.VkUpload(self.vk_session)
            img = uploader.photo_messages('img/placeholder_car.png')
            media_id = img[0]['id']
            owner_id = img[0]['owner_id']

            self.vk_session.method('messages.send', {
                'user_id': user_id,
                'message': msg,
                'attachment': 'photo' + str(owner_id) + '_' + str(media_id),
                'random_id': 0})




