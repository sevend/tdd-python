from .base import FunctionalTest
import time
from selenium.webdriver.support.ui import WebDriverWait

from unittest import skip


TEST_EMAIL = 'edith@mockmyid.com'

@skip
class LoginTest(FunctionalTest):


    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find window')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=3).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was {}'.format(element_id, self.browser.find_element_by_tag_name('body').text)
        )

    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def test_login_with_persona(self):
        # 伊迪丝访问这个很棒的超级列表网站
        # 第一次注意到 “ Sign in ” 链接
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # 出现一个Persona登录框
        # self.switch_to_new_window('Mozilla Persona') # ➊

        # 伊迪丝使用她的电子邮件地址登录
        ## 测试中的电子邮件使用mockmyid.com
        self.browser.find_element_by_id(
        'authentication_email' # ➋
        ).send_keys(TEST_EMAIL) # ➌
        self.browser.find_element_by_tag_name('button').click()

        # Persona窗口关闭
        self.switch_to_new_window('To-Do')

        # 她发现自己已经登录
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # 刷新页面，她发现真的通过会话登录了
        # 而且并不只在那个页面中有效
        self.browser.refresh()
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # 对这项新功能有些恐惧，她立马点击了退出按钮
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

        # 刷新后仍旧保持退出状态
        self.browser.refresh()
        self.wait_to_be_logged_out(email=TEST_EMAIL)