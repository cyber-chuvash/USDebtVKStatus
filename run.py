import time
import locale
import logging

import requests
import vk_requests

from config import Config


locale.setlocale(locale.LC_ALL, 'en_US')
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s', level=Config.log_level)


class StatusUpdater:
    def __init__(self):
        self.vk = vk_requests.create_api(
            app_id=6666569,
            login=Config.vk_login,
            password=Config.vk_pass,
            scope='status,offline',
            api_version='5.92',
        )
        logging.info('Initialized VK API instance')
        try:
            self.status_str = Config.status_str
            logging.info('Using user-defined status string: %s', self.status_str)
        except KeyError:
            self.status_str = 'Госдолг США: $%s'
            logging.info('Using default status string: %s', self.status_str)

    def run(self):
        while True:
            status = self.get_new_status_string()
            self.vk.status.set(text=status)
            logging.info('Updated status: %s', status)
            time.sleep(3600)

    @staticmethod
    def get_us_national_debt():
        res = requests.get(
            'https://www.treasurydirect.gov/NP_WS/debt/current',
            params={'format': 'json'}
        )
        data = res.json()
        logging.info('Response from debt API: code: %s, body: %s', res.status_code, res.text)
        return int(data['totalDebt'])

    def get_new_status_string(self):
        debt_str = locale.format_string('%d', self.get_us_national_debt(), grouping=True)
        return self.status_str % debt_str


updater = StatusUpdater()
updater.run()
