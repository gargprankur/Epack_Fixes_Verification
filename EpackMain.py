import argparse
import sys
import time
import re
import logging
import datetime

from selenium.common import NoAlertPresentException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from BaseClass import BaseClass
from EpachHomePage import EpackHomePage
from HostConnectivity import HostConnectivity


class EpackMain(BaseClass):
    def __init__(self):
        self.epack_home = EpackHomePage(self.driver)
        self.driver.get("http://pmaxepackprd.corp.emc.com")
        time.sleep(5)
        date_today = datetime.datetime.today()
        date_today = date_today.strftime('%Y%m%d')
        file_name = "Fixes_" + date_today
        self._logger = logging.getLogger(__name__)
        file_handler = logging.FileHandler(filename= file_name)
        self._logger.addHandler(file_handler)
        self._logger.setLevel(logging.DEBUG)
        self._formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s ')

        file_handler.setFormatter(self._formatter)



    def parse_cmd_args(self):

        parser = argparse.ArgumentParser("help = We need to provide epack number")
        parser.add_argument('--epack', type = int, required= True)
        parser.add_argument('--host_ip', type = str, required= True)
        parser.add_argument('--username', type = str, default = "root")
        parser.add_argument('--password', type = str, default = "dangerous")
        parser.add_argument('--sid', type = int, required= True)
        parse_args = parser.parse_args()
        self._epack = parse_args.epack
        self._host_ip = parse_args.host_ip
        self._username = parse_args.username
        self._password = parse_args.password
        self._sid = parse_args.sid



    def search_epack(self):
        search_epack = self.epack_home.search_epack_input()
        search_epack.send_keys(self._epack)
        search_button = self.epack_home.search_button_field()
        search_button.click()
        time.sleep(10)
        try:
            alert_1 = self.driver.switch_to.alert
            print(f' The Epack Number which you entered is incorrect and the message of alert is {alert_1.text}')
            alert_1.accept()
            self.driver.close()
            sys.exit()
        except NoAlertPresentException as ex:
            print("No alert found")


    def get_instructions(self):
        test_instructions = self.epack_home.test_instructions_paragraph()
        test_instructions = test_instructions.text

        self._epack_page_digits = re.findall(r'\d{5,7}', test_instructions)
        self._symmwin_fixes = re.findall(r'OPT\d{5,7}', test_instructions)
        #print(f' Total symmwin fixes at epack page are {len(self._symmwin_fixes)}')
        #print(f'Type of epack_page_digits is {type(self._epack_page_digits)} and value is {self._epack_page_digits}')
        self.driver.close()

    def get_symm_ucode_fixes(self):
        host = HostConnectivity(self._host_ip, self._username, self._password, self._sid)
        self._symm_fixes = host.get_symm_fixes()

    def match_ucode_fixes(self):
        i = 0
        for symm_fix in self._symm_fixes:
            if str(symm_fix) in self._epack_page_digits:
                self._logger.info(f'{symm_fix} is found and matched')
                i = i+1

        self._logger.info(f'Total fixes matched are {i}')


    def match_symmwin_fixes(self):
        symmwin_box_fixes = []
        count = 0
        with open('symmwin', 'r') as f1:
            for symmwin_fix in f1:
                symmwin_fix = symmwin_fix.strip('\n')
                symmwin_box_fixes.append(symmwin_fix)

        for symmwin_box_fix in symmwin_box_fixes:
            for symmwin_epack_fix in self._symmwin_fixes:
                if str(symmwin_box_fix) == str(symmwin_epack_fix):
                    self._logger.info(f"Symmwin fix {symmwin_box_fix} is matched")
                    count = count + 1

        self._logger.info(f'Total symmwin fixes matches are {count}')


epack_main = EpackMain()
epack_main.parse_cmd_args()
epack_main.search_epack()
epack_main.get_instructions()
epack_main.get_symm_ucode_fixes()
epack_main.match_ucode_fixes()
epack_main.match_symmwin_fixes()

