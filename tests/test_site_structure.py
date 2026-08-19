import unittest
from html.parser import HTMLParser
from urllib.request import urlopen


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section_ids = []
        self.classes = set()
        self.practice_dossier_count = 0
        self.case_file_count = 0
        self.case_field_counts = []
        self._inside_case_file = False
        self._current_case_field_count = 0
        self.hero_secondary_link_count = 0
        self.practice_photos = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "section" and attributes.get("id"):
            self.section_ids.append(attributes["id"])
        classes = attributes.get("class", "").split()
        self.classes.update(classes)
        if tag == "article" and "practice-dossier" in classes:
            self.practice_dossier_count += 1
        if tag == "article" and "case-file" in classes:
            self.case_file_count += 1
            self._inside_case_file = True
            self._current_case_field_count = 0
        if tag == "section" and self._inside_case_file and "case-field" in classes:
            self._current_case_field_count += 1
        if tag == "a" and "hero-secondary-link" in classes:
            self.hero_secondary_link_count += 1
        if tag == "img" and "practice-photo__image" in classes:
            self.practice_photos.append(
                {
                    "motif": attributes.get("data-practice-motif"),
                    "src": attributes.get("src"),
                    "alt": attributes.get("alt"),
                    "loading": attributes.get("loading"),
                    "width": attributes.get("width"),
                    "height": attributes.get("height"),
                }
            )

    def handle_endtag(self, tag):
        if tag == "article" and self._inside_case_file:
            self.case_field_counts.append(self._current_case_field_count)
            self._inside_case_file = False
            self._current_case_field_count = 0


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

    def test_premium_profile_has_required_semantic_regions(self):
        required = {
          "hero-practice-list",
            "practice-dossiers",
            "client-questions",
            "profile-facts",
            "contact-panel",
        }
        self.assertTrue(required.issubset(self.parser.classes))
        self.assertNotIn("trust-strip", self.parser.classes)
        self.assertNotIn("hero-trust", self.parser.classes)

    def test_page_presents_three_equal_practices_and_five_detailed_cases(self):
        required = {
            "service-relationship",
            "relationship-stage",
            "case-file",
            "case-field",
            "contact-preparation",
        }
        retired = {"method-list", "insight-note", "faq-item"}

        self.assertTrue(required.issubset(self.parser.classes))
        self.assertTrue(retired.isdisjoint(self.parser.classes))
        self.assertEqual(self.parser.practice_dossier_count, 3)
        self.assertEqual(self.parser.case_file_count, 5)
        self.assertEqual(self.parser.case_field_counts, [5, 5, 5, 5, 5])

    def test_license_number_is_not_published(self):
        self.assertNotIn("15101202611271621", self.html)
        self.assertNotIn("执业证号", self.html)

    def test_mobile_editorial_layout_contract(self):
        self.assertIn("premium-counsel-layout", self.parser.classes)

    def test_mobile_hero_prioritizes_the_lawyer(self):
        self.assertIn("hero--counsel-profile", self.parser.classes)
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
        self.assertEqual(
            [(photo["width"], photo["height"]) for photo in self.parser.practice_photos],
            [("1600", "1067"), ("1600", "1068"), ("1600", "1067")],
        )

    def test_page_removes_mechanical_identity_repetition(self):
        self.assertNotIn("footer-brand", self.parser.classes)
        self.assertNotIn("footer-nav", self.parser.classes)
        self.assertIn("footer-minimal", self.parser.classes)
        self.assertNotIn("<figcaption>", self.html)
        self.assertIn("黄绘莉律师｜四川观今律师事务所", self.html)
        self.assertIn("民商事争议解决", self.html)
        self.assertIn("专业方向与工作方法", self.html)


if __name__ == "__main__":
    unittest.main()
