from .base import FunctionalTest
import time
from selenium.webdriver.support.ui import WebDriverWait

class LoginTest(FunctionalTest):
    def test_login_with_persona(self):
        # 伊迪丝访问这个很棒的超级列表网站
        # 第一次注意到 “ Sign in ” 链接
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('login').click()

        # 出现一个Persona登录框
        self.switch_to_new_window('Mozilla Persona') # ➊

        # 伊迪丝使用她的电子邮件地址登录
        ## 测试中的电子邮件使用mockmyid.com
        self.browser.find_element_by_id(
        'authentication_email' # ➋
        ).send_keys('edith@mockmyid.com') # ➌
        self.browser.find_element_by_tag_name('button').click()

        # Persona窗口关闭
        self.switch_to_new_window('To-Do')

        # 她发现自己已经登录
        self.wait_for_element_with_id('logout') # ➍
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('edith@mockmyid.com', navbar.text)

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
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id)
        )