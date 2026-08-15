import unittest
from html.parser import HTMLParser
from urllib.request import urlopen


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section_ids = []
        self.classes = set()
        self.selected_case_count = 0
        self.hero_secondary_link_count = 0
        self.practice_photos = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "section" and attributes.get("id"):
            self.section_ids.append(attributes["id"])
        classes = attributes.get("class", "").split()
        self.classes.update(classes)
        if tag == "article" and "selected-case" in classes:
            self.selected_case_count += 1
        if tag == "a" and "hero-secondary-link" in classes:
            self.hero_secondary_link_count += 1
        if tag == "img" and "practice-photo__image" in classes:
            self.practice_photos.append(
                {
                    "motif": attributes.get("data-practice-motif"),
                    "src": attributes.get("src"),
                    "alt": attributes.get("alt"),
                    "loading": attributes.get("loading"),
                }
            )


class SiteStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with urlopen("http://localhost:8081/", timeout=3) as response:
            cls.status = response.status
            html = response.read().decode("utf-8")
        cls.html = html
        cls.parser = SiteParser()
        cls.parser.feed(html)

    def test_homepage_uses_client_decision_order(self):
        self.assertEqual(self.status, 200)
        self.assertEqual(
            self.parser.section_ids,
            ["home", "services", "about", "service", "cases", "contact"],
        )

    def test_redesign_has_integrated_trust_and_credentials(self):
        required = {
            "hero-practice-list",
            "practice-ledger",
            "problem-list",
            "about-credentials",
            "contact-panel",
        }
        self.assertTrue(required.issubset(self.parser.classes))
        self.assertNotIn("trust-strip", self.parser.classes)
        self.assertNotIn("hero-trust", self.parser.classes)

    def test_later_page_is_a_concise_private_client_journey(self):
        required = {
            "service-relationship",
            "relationship-stage",
            "selected-case",
            "contact-preparation",
        }
        retired = {"method-list", "insight-note", "faq-item"}

        self.assertTrue(required.issubset(self.parser.classes))
        self.assertTrue(retired.isdisjoint(self.parser.classes))
        self.assertEqual(self.parser.selected_case_count, 3)

    def test_mobile_editorial_layout_contract(self):
        self.assertIn("mobile-editorial-layout", self.parser.classes)

    def test_mobile_hero_prioritizes_the_lawyer(self):
        self.assertIn("hero--portrait-first", self.parser.classes)
        self.assertEqual(self.parser.hero_secondary_link_count, 0)

    def test_each_practice_area_has_a_distinct_local_photo(self):
        self.assertEqual(
            [photo["motif"] for photo in self.parser.practice_photos],
            ["performance", "governance", "family-assets"],
        )
        self.assertEqual(
            [photo["src"] for photo in self.parser.practice_photos],
            [
                "assets/practice-contract.jpg",
                "assets/practice-business.jpg",
                "assets/practice-family.jpg",
            ],
        )
        self.assertTrue(all(photo["alt"] == "" for photo in self.parser.practice_photos))
        self.assertTrue(
            all(photo["loading"] == "lazy" for photo in self.parser.practice_photos)
        )

    def test_page_removes_mechanical_identity_repetition(self):
        self.assertNotIn("footer-brand", self.parser.classes)
        self.assertNotIn("footer-nav", self.parser.classes)
        self.assertIn("footer-minimal", self.parser.classes)
        self.assertNotIn("<figcaption>", self.html)
        self.assertNotIn(
            "黄绘莉律师&nbsp;&nbsp;/&nbsp;&nbsp;四川观今律师事务所",
            self.html,
        )
        self.assertIn("成都 · 民商事争议解决", self.html)
        self.assertIn("执业方向与工作重点", self.html)


if __name__ == "__main__":
    unittest.main()
