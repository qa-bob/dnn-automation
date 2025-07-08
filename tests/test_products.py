import pytest
from pages.infinia_page import InfiniaPage
from pages.a3i_page import A3iPage
from pages.insight_page import InsightPage

@pytest.mark.functional
class TestProducts:
    def test_infinia_page_title(self, driver, wait):
        infinia_page = InfiniaPage(driver, wait)
        infinia_page.go_to_url(infinia_page.url)
        assert "Infinia" in driver.title

    def test_a3i_page_title(self, driver, wait):
        a3i_page = A3iPage(driver, wait)
        a3i_page.go_to_url(a3i_page.url)
        assert "A³I" in driver.title

    def test_insight_page_title(self, driver, wait):
        insight_page = InsightPage(driver, wait)
        insight_page.go_to_url(insight_page.url)
        assert "Insight" in driver.title
