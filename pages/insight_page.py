from pages.base_page import BasePage

class InsightPage(BasePage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)
        self.url = "https://www.ddn.com/products/insight-software/"
