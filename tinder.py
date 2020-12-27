import logging
import os
from configparser import RawConfigParser
from time import sleep

import attr
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

import constants
from events import ActionEvent, LoginEvent

logger = logging.getLogger(__name__)

config = RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "CONF.ini"))


@attr.s(auto_attribs=True)
class SeleOptions:
    chrome_options: Options = Options()
    executable_path: str = 'utils/chromedriver.exe'

    def __attrs_post_init__(self):
        self.chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        )


@attr.s
class Tinder:
    AVAILABLE_COMMANDS = ['like', 'dislike']
    options = SeleOptions()
    tinder_url: str = 'https://tinder.com'
    driver: WebDriver = attr.ib(default=None)
    base_window = attr.ib(default=None)
    base_sleep_time: int = constants.SLEEP_TIME

    def __attrs_post_init__(self):
        self.driver = webdriver.Chrome(executable_path=self.options.executable_path,
                                       chrome_options=self.options.chrome_options)
        self.driver.get(self.tinder_url)
        self.driver.maximize_window()
        self.base_window = self.driver.window_handles[0]

    def command(self, command):
        method = getattr(self, command)
        return method()

    def sleep(self, time=None):
        if not time:
            time = self.base_sleep_time
        sleep(time)

    def login(self):
        def fb_login_button_click():
            login_via_fb_button = self.driver.find_element_by_xpath(
                '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button')
            login_via_fb_button.click()

        login_button = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button')
        login_button.click()
        self.sleep(1)

        try:
            fb_login_button_click()
        except NoSuchElementException:
            login_options_button = self.driver.find_element_by_xpath(
                '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/button')
            login_options_button.click()
            sleep(1)
            fb_login_button_click()

        # fb window popup
        self.driver.switch_to.window(self.driver.window_handles[1])
        email_form = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_form.send_keys(constants.FB_LOGIN)
        pw_form = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_form.send_keys(constants.FB_PASSWORD)
        fb_login_button = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        fb_login_button.click()
        self.sleep(5)
        self.driver.switch_to.window(self.base_window)
        permission_button = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        permission_button.click()
        notification_button = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        notification_button.click()
        self.sleep(6)
        logger.info(LoginEvent().get_event('LOG_SUCCESS', constants.FB_LOGIN))
        return self

    def like_button_click(self):
        like_button = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[4]/button')
        like_button.click()
        logger.info(ActionEvent().get_event('PRESSED_LIKE'))

    def decline_main_window_add(self):
        no_thatks_button = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        no_thatks_button.click()
        logger.info(ActionEvent().get_event('MAIN_WINDOW_DISLIKE'))

    def decline_ask_for_superlike(self):
        no_thatks_button = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/button[2]')
        no_thatks_button.click()
        logger.info(ActionEvent().get_event('ASK_FOR_SUPERLIKE_DECLINED'))

    def decline_tinder_premium(self):
        no_thatks_button = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/button[2]')
        no_thatks_button.click()
        logger.info(ActionEvent().get_event('TINDER_PREMIUM_DISLIKE'))

    def send_message_on_match(self):
        logger.info(ActionEvent().get_event('ITS_A_MATCH'))
        text_form = self.driver.find_element_by_xpath('//*[@id="chat-text-area"]')
        text_form.send_keys(constants.MESSAGE_ON_SEND)
        send_button = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form/button')
        send_button.submit()
        logger.info(ActionEvent().get_event('ITS_A_MATCH'))

    def like(self):
        logger.debug(ActionEvent().get_event('PREPARE_TO_LIKE'))
        try:
            self.like_button_click()
        except ElementClickInterceptedException as e:
            logger.info(ActionEvent().get_event('ASK_FOR_SUPERLIKE', str(e)))
            try:
                self.decline_ask_for_superlike()
            except NoSuchElementException:
                try:
                    self.decline_main_window_add()
                except NoSuchElementException:
                    try:
                        self.decline_tinder_premium()
                    except NoSuchElementException:
                        self.send_message_on_match()
        return self

    def dislike(self):
        logger.debug(ActionEvent().get_event('PREPARE_TO_DISLIKE'))
        dislike_button = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/button')
        dislike_button.click()
        logger.info(ActionEvent().get_event('PRESSED_DISLIKE'))
        return self
