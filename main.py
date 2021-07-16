import requests
from pprint import pprint
from datetime import datetime
from tqdm import tqdm
current_datetime = datetime.now()

token_ydisk ='my_token'
user_id = '585749225'

class Backup_VK_profile_photo_to_Yandex_Disk:
    def __init__(self, token_ydisk, user_id):
        self.token = token_ydisk
        self.user_id = user_id

    def get_vk_token(self):
        with open('token.txt', 'r') as file:
            token_vk = file.read().strip()
        return token_vk

    def get_photos_and_likes(self):
        URL1 = 'https://api.vk.com/method/photos.get'
        params_1 = {
            'owner_id': user_id,
            'album_id': 'profile',
            'access_token': self.get_vk_token(),
            'v':'5.77',
            'extended': '1',
        }
        res = requests.get(URL1, params=params_1)
        photos_and_likes = {}
        for fields in res.json()['response']['items']:
            likes = str(fields['likes']['count'])
            max_size_photo_url = fields['sizes'][-1]['url']
            photos_and_likes[max_size_photo_url] = likes
        return photos_and_likes

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(token_ydisk)
        }

    def create_folder(self):
        upload_url_0 = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params_2 = {"path": 'Backup_profile_photos_from_VK_on' + '_' + str(current_datetime.year) + '_' + str(current_datetime.month)
                            + '_' + str(current_datetime.day) + '_' + str(current_datetime.hour) + '_' + str(current_datetime.minute) + '_' + str(current_datetime.second)}
        response = requests.put(upload_url_0, headers=headers, params=params_2)
        response.raise_for_status()
        if response.status_code == 201:
            print('Backup folder successfully created on Yandex.Disk')
        else:
            print(response.status_code)
        return response.json()

    def get_folder_name(self):
        upload_url_1 = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params_3 = {"path": 'Backup_profile_photos_from_VK_on' + '_' + str(current_datetime.year) + '_' + str(current_datetime.month)
                        + '_' + str(current_datetime.day) + '_' + str(current_datetime.hour) + '_' + str(current_datetime.minute) + '_' + str(current_datetime.second)}
        response = requests.get(upload_url_1, headers=headers, params=params_3)
        response.raise_for_status()
        if response.status_code == 200:
            pass
        else:
            print(response.status_code)
        folder_name = response.json()['name']
        return folder_name

    def upload_file(self):
        upload_url_2 = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        photos_and_likes = self.get_photos_and_likes()
        for photo in tqdm(photos_and_likes):
            params_4 = {"url": photo, "path": self.get_folder_name() + '/' + photos_and_likes[photo]}
            response = requests.post(upload_url_2, headers=headers, params=params_4)
            response.raise_for_status()
            if response.status_code == 202:
                pprint (f' File: {photo} successfully uploaded to folder: {self.get_folder_name()}')
            else:
                print(response.status_code)
        return print('The process of backup VK profile photos to Yandex Disk is over')

    def upload_file_and_get_info(self):
        upload_url_3 = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        self.upload_file()
        photos_and_likes = self.get_photos_and_likes()
        information_list = []
        for photo in photos_and_likes:
            params_5 = {"path": self.get_folder_name() + '/' + photos_and_likes[photo]}
            response = requests.get(upload_url_3, headers=headers, params=params_5)
            response.raise_for_status()
            if response.status_code == 200:
                pass
            else:
                print(response.status_code)
            information_dict = {}
            information_dict['file_name'] = response.json()['name'] + '.jpg'
            information_dict['size'] = str(response.json()['size'])
            information_list.append(information_dict)
        with open('output.json', 'w')as file:
            file.write(str(information_list))
        return

    def perform_all_functions(self):
        self.create_folder()
        self.upload_file_and_get_info()
        return

if __name__ == '__main__':
    VK_photo_uploader = Backup_VK_profile_photo_to_Yandex_Disk(token_ydisk, user_id)
    VK_photo_uploader.perform_all_functions()

