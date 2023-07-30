# -*- coding: utf-8 -*-
import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler


class ScheduleCronJob:
    def __init__(self, image_folder, minutes):
        self.image_folder = image_folder

        scheduler = BackgroundScheduler()
        interval_minutes = minutes

        scheduler.add_job(self.delete_images, 'interval',
                          minutes=interval_minutes)

        scheduler.start()

    def delete_images(self):
        current_datetime = datetime.datetime.now()

        one_day_ago = current_datetime - datetime.timedelta(days=5)

        files = os.listdir(self.image_folder)

        for file_name in files:
            file_path = os.path.join(self.image_folder, file_name)
            if os.path.isfile(file_path) and os.path.getmtime(file_path) < one_day_ago.timestamp():
                os.remove(file_path)
