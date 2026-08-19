import unittest
from html.parser import HTMLParser
from urllib.request import urlopen


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section_ids = []
        self.classes = set()
        self.service_group_count = 0
        self.case_card_count = 0
        self.faq_item_count = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "section" and attributes.get("id"):
            self.section_ids.append(attributes["id"])
        classes = attributes.get("class", "").split()
        self.classes.update(classes)
        if tag == "article" and "service-group" in classes:
            self.service_group_count += 1
        if tag == "article" and "case-card" in classes:
            self.case_card_count += 1
        if tag == "details" and "faq-item" in classes:
            self.faq_item_count += 1


class SiteStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with urlopen("http://localhost:8081/", timeout=3) as response:
            cls.status = response.status
            html = response.read().decode("utf-8")
        cls.html = html
        cls.parser = SiteParser()
        cls.parser.feed(html)

    def test_homepage_returns_full_original_layout(self):
        self.assertEqual(self.status, 200)
        self.assertEqual(
            self.parser.section_ids,
            ["home", "services", "philosophy", "cases", "about", "insights", "faq", "contact"],
        )

    def test_page_includes_original_content_regions(self):
        required = {
            "trust-strip",
            "service-map",
            "service-group",
            "method-chain",
            "case-list",
            "case-card",
            "insight-note",
            "faq-item",
            "footer-disclaimer",
        }
        self.assertTrue(required.issubset(self.parser.classes))

    def test_page_presents_three_service_groups_five_cases_and_three_faqs(self):
        self.assertEqual(self.parser.service_group_count, 3)
        self.assertEqual(self.parser.case_card_count, 5)
        self.assertEqual(self.parser.faq_item_count, 3)

    def test_license_number_is_not_published(self):
        self.assertNotIn("15101202611271621", self.html)
        self.assertNotIn("执业证号", self.html)

    def test_real_portraits_are_used(self):
        self.assertIn("assets/huang-huili-portrait.webp", self.html)
        self.assertIn("assets/huang-huili-profile.webp", self.html)

    def test_navigation_includes_original_sections(self):
        self.assertIn('href="#philosophy"', self.html)
        self.assertIn('href="#insights"', self.html)
        self.assertIn('href="#faq"', self.html)


if __name__ == "__main__":
    unittest.main()
