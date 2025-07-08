from pages.base_page import BasePage

class A3iPage(BasePage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)
        self.url = "https://www.ddn.com/products/a3i-accelerated-any-scale-ai/"
