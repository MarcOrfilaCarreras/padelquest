# -*- coding: utf-8 -*-
import io
import os

import requests


class ImageDownloader:
    def __init__(self, image_folder):
        self.image_folder = image_folder

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

    def download_image(self, image_url, image_name):
        image_path = os.path.join(self.image_folder, image_name)

        if not os.path.exists(image_path):
            response = requests.get(image_url)

            if (response.status_code == 200) or (response.status_code == 206):
                with open(image_path, 'wb') as f:
                    f.write(response.content)

    def get_image(self, image_url, image_name):
        image_path = os.path.join(self.image_folder, image_name)

        if not os.path.exists(image_path):
            self.download_image(image_url, image_name)

        image_stream = None

        with open(image_path, 'rb') as f:
            image_stream = io.BytesIO(f.read())

        return image_stream
