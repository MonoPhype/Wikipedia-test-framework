from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time


class DifferentTests:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.user = '''user'''
        self.password1 = '''password1'''
        self.password2 = '''password2'''

    def login(self, password=None):
        if password is None:
            password = self.password1
        self.driver.find_element(By.CSS_SELECTOR, '#pt-login a').click()
        self.driver.find_element(By.ID, 'wpName1').clear()
        self.driver.find_element(By.ID, 'wpName1').send_keys(self.user)
        self.driver.find_element(By.ID, 'wpPassword1').send_keys(password)
        try:
            self.driver.find_element(By.ID, 'mw-input-captchaWord')
        except:
            pass
        else:
            input('Type-CAPTCHA wait...')
        self.driver.find_element(By.ID, 'wpLoginAttempt').click()
        try:
            already_logged_msg = self.driver.find_element(By.CSS_SELECTOR, '#userloginForm .mw-message-box-warning')
        except:
            pass
        else:
            if 'You are already logged in' in already_logged_msg.text:
                print('Already logged in message popped up.')
                return True
            else:
                print('Examine popped up message.')
                return False
        try:
            return self.driver.find_element(By.CSS_SELECTOR, '#pt-userpage a').text == self.user
        except:
            return False

    def top_right_login_changes(self):
        log_text_elem = self.driver.find_element(By.CSS_SELECTOR, '#pt-anonuserpage span')
        first = bool(log_text_elem.text == 'Not logged in')
        second = bool(self.driver.find_element(By.CSS_SELECTOR, '#pt-login span').text == 'Log in')
        third = bool(self.driver.find_element(By.CSS_SELECTOR, '#pt-createaccount span').text == 'Create account')
        try:
            self.driver.find_element(By.ID, 'pt-preferences')
        except:
            fourth = True
        else:
            fourth = False
        self.login()
        try:
            self.driver.find_element(By.ID, 'pt-preferences')
        except:
            fifth = False
        else:
            fifth = True
        sixth = bool(self.driver.find_element(By.CSS_SELECTOR, '#pt-preferences a').text == 'preferences')
        return [first, second, third, fourth, fifth, sixth]

    def watch_bubble(self):
        self.login()
        self.driver.get(self.url)
        try:
            self.driver.find_element(By.ID, 'ca-watch')
        except:
            try:
                self.driver.find_element(By.ID, 'ca-unwatch')
            except:
                return ['No watch/unwatch elements found.', False]
            else:
                try:
                    time.sleep(1.5)
                    self.driver.find_element(By.CSS_SELECTOR, '#ca-unwatch a').click()
                    self.driver.find_element(By.ID, 'mw-notification-area')
                except:
                    return ['''Unwatch bubble didn't show.''', False]
                else:
                    return ['Unwatch bubble showed Successfully.', True]
        else:
            try:
                time.sleep(1.5)
                self.driver.find_element(By.CSS_SELECTOR, '#ca-watch a').click()
                self.driver.find_element(By.ID, 'mw-watchlink-notification')
            except:
                return ['''Watch bubble didn't show.''', False]
            else:
                return ['Watch bubble showed Successfully.', True]

    def change_password_process(self, password1, password2):
        self.driver.find_element(By.CSS_SELECTOR, '#pt-preferences a').click()
        self.driver.find_element(By.CSS_SELECTOR, '#ooui-php-17 a').click()
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#userloginForm .mw-message-box-warning')
        except:
            pass
        else:
            self.driver.find_element(By.ID, 'wpPassword1').send_keys(password1)
            self.driver.find_element(By.ID, 'wpLoginAttempt').click()
        self.driver.find_element(By.ID, 'ooui-php-1').send_keys(password2)
        self.driver.find_element(By.ID, 'ooui-php-2').send_keys(password2)
        self.driver.find_element(By.CSS_SELECTOR, '#change_credentials_submit .oo-ui-buttonElement-button').click()

    def change_password(self):
        self.login()
        self.change_password_process(self.password1, self.password2)
        self.driver.find_element(By.CSS_SELECTOR, '#pt-logout a').click()
        time.sleep(1)
        if not self.login():
            if self.login(self.password2):
                positive_result = ['', True]
            else:
                return ['''Old and new passwords didn't work.''', False]
        else:
            self.driver.find_element(By.CSS_SELECTOR, '#pt-logout a').click()
            if self.login(self.password2):
                return ['''Password didn't change.''', False]
            else:
                return ['''Both passwords work.''', False]
        self.change_password_process(self.password2, self.password1)
        return positive_result

