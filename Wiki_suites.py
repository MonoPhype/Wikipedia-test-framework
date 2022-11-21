import unittest as ut
import Wiki_tests
import Wiki_funcs


class MainRunner:
    def __init__(self):
        self.firefox_driver = 'geckodriver'
        self.chrome_driver = 'chromedriver'
        self.drivers = [self.firefox_driver, self.chrome_driver]
        self.multiple_drivers = False
        self.lines = '----------------------------------------------------------------------'

    def prompt_driver_type(self):
        select_driver = input(f'{self.lines}\nElse — Firefox | 2 — Chrome  ||  A/a — Both\nChoose: ')
        if select_driver == '2':
            self.driver_type = self.chrome_driver
            print('*Chrome chosen.')
        elif select_driver == 'A' or select_driver == 'a':
            self.multiple_drivers = True
            print('*Both chosen.')
        else:
            self.driver_type = self.firefox_driver
            print('*Firefox chosen.')
        self.url = 'https://en.wikipedia.org/wiki/Eskimo'
        updated_url = input(f'{self.lines}\nDefault — {self.url}\nSpecify Wikipedia URL: ')
        if 'wikipedia.org' in updated_url:
            self.url = updated_url
            print('*URL chosen.')
        else:
            print('*Default URL chosen.')
        # return [self.driver_type, self.url]

    def prompt_tests(self):
        test_classes_list = [Wiki_tests.TestingWikipedia]
        self.string_tests_list = []
        for test_class in test_classes_list:
            tests = [func for func in dir(test_class) if func.startswith('test')]
            tests_string = ''
            for i, e in enumerate(tests):
                tests_string += f'{i+1} — {e} | '
            tests_string = tests_string.strip().strip('|')
            user_input = input(f'{self.lines}\n{tests_string}'
                               f' ||  A/a — All | N/n — None\n(separated by commas)\nChoose: ')
            user_input_list = user_input.replace(' ', '').strip(',').split(',')
            for i in user_input_list:
                string_test_class = str(test_class)[8:-2]
                if i == 'a' or i == 'A':
                    self.string_tests_list.append(test_class)
                    print('*'+string_test_class)
                elif i == 'n' or i == 'N':
                    pass
                else:
                    executed_test = string_test_class+'.'+tests[int(i)-1]
                    self.string_tests_list.append(executed_test)
                    print('*'+executed_test)
        self.load_tests(self.string_tests_list)
        print(self.lines)

    def load_tests(self, list_of_tests=None):
        if list_of_tests is None:
            list_of_tests = self.string_tests_list
        self.loaded_tests_list = []
        for i in list_of_tests:
            if type(i) == str:
                self.loaded_tests_list.append(ut.TestLoader().loadTestsFromName(i))
            else:
                self.loaded_tests_list.append(ut.TestLoader().loadTestsFromTestCase(i))

    def set_vars(self, driver_type=None):
        if driver_type is None:
            driver_type = self.driver_type
        Wiki_tests.TestingWikipedia.driver_type = driver_type
        Wiki_tests.TestingWikipedia.url = self.url

    def run_tests(self):
        test_suite = ut.TestSuite(self.loaded_tests_list)
        ut.TextTestRunner().run(test_suite)


child = MainRunner()


# Will potentially expand with threading:
def many_funcs_single_thread(driver):
    child.set_vars(driver)
    child.run_tests()
    child.load_tests()


if __name__ == "__main__":
    child.prompt_driver_type()
    child.prompt_tests()
    if child.multiple_drivers:
        threads = []
        for driver in child.drivers:
            many_funcs_single_thread(driver)
    else:
        child.set_vars()
        child.run_tests()

