import unittest
from selenium import webdriver
import Wiki_funcs
import Wiki_suites


class TestingWikipedia(unittest.TestCase):
    def setUp(self):
        if self.driver_type.endswith('chromedriver'):
            self.driver = webdriver.Chrome(self.driver_type)
        else:
            self.driver = webdriver.Firefox(executable_path=self.driver_type)
        self.driver.get(self.url)
        self.diff_tests = Wiki_funcs.DifferentTests(self.driver, self.url)

    def tearDown(self):
        self.driver.close()

    def test_login(self):
        assert self.diff_tests.login()

    def test_top_right_login_changes(self):
        for i, e in enumerate(self.diff_tests.top_right_login_changes()):
            assert e
            print(i+1)

    def test_watch_bubble(self):
        result = self.diff_tests.watch_bubble()
        print(result[0])
        assert result[1]

    def test_change_password(self):
        result = self.diff_tests.change_password()
        print(result[0])
        assert result[1]


if __name__ == "__main__":
    unittest.main()

















